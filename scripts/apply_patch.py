#!/usr/bin/env python
import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from extract_account_data import (
    build_memo as build_memo_from_transcript,
    parse_business_hours_text,
    parse_transfer_rules_text,
    compute_questions_or_unknowns,
)


def _dedupe_preserve_order(items: List[str]) -> List[str]:
    seen = set()
    out: List[str] = []
    for x in items:
        s = str(x)
        if s in seen:
            continue
        seen.add(s)
        out.append(s)
    return out


def _is_meaningful(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return any(_is_meaningful(v) for v in value)
    if isinstance(value, dict):
        return any(_is_meaningful(v) for v in value.values())
    return True


def _merge_dict_nonempty(base: Dict[str, Any], updates: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
    """
    Merge dict by overriding only keys where update value is meaningful.
    Returns (merged, override_notes[])
    """
    merged = dict(base or {})
    notes: List[str] = []
    for k, v in (updates or {}).items():
        if not _is_meaningful(v):
            continue
        prev = merged.get(k)
        if _is_meaningful(prev) and prev != v:
            notes.append(f"'{k}' overridden: previous={prev!r}, new={v!r}")
        merged[k] = v
    return merged, notes


def merge_memos(base: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge onboarding memo into base memo.

    - For scalar fields: if updates[field] is non-empty and different, override base.
    - questions_or_unknowns: concatenate arrays, plus entries for fields that are still empty.
    - notes: concatenate arrays.
    - Never fabricate values: only use what exists in base or updates.
    """
    merged = dict(base)

    merge_fields = [
        "company_name",
        "business_hours",
        "office_address",
        "services_supported",
        "emergency_definition",
        "emergency_routing_rules",
        "non_emergency_routing_rules",
        "call_transfer_rules",
        "integration_constraints",
        "after_hours_flow_summary",
        "office_hours_flow_summary",
    ]

    for field in merge_fields:
        new_val = updates.get(field)
        if not _is_meaningful(new_val):
            continue

        old_val = merged.get(field)

        # Dicts: merge key-by-key (do not wipe unrelated fields)
        if isinstance(old_val, dict) and isinstance(new_val, dict):
            merged_dict, key_notes = _merge_dict_nonempty(old_val, new_val)
            if key_notes:
                base_notes = merged.get("notes") or []
                if not isinstance(base_notes, list):
                    base_notes = [str(base_notes)]
                for kn in key_notes:
                    base_notes.append(f"Onboarding override for '{field}': {kn}.")
                merged["notes"] = base_notes
            merged[field] = merged_dict
            continue

        # Lists: onboarding overrides list if non-empty
        if isinstance(new_val, list):
            if _is_meaningful(old_val) and old_val != new_val:
                base_notes = merged.get("notes") or []
                if not isinstance(base_notes, list):
                    base_notes = [str(base_notes)]
                base_notes.append(
                    f"Onboarding override for '{field}': previous value={old_val!r}, new value={new_val!r}."
                )
                merged["notes"] = base_notes
            merged[field] = new_val
            continue

        # Strings/others: override directly
        if isinstance(new_val, str):
            new_val = new_val.strip()
        if _is_meaningful(old_val) and old_val != new_val:
            base_notes = merged.get("notes") or []
            if not isinstance(base_notes, list):
                base_notes = [str(base_notes)]
            base_notes.append(
                f"Onboarding override for '{field}': previous value={old_val!r}, new value={new_val!r}."
            )
            merged["notes"] = base_notes
        merged[field] = new_val

    # questions_or_unknowns and notes as lists
    base_questions = base.get("questions_or_unknowns") or []
    update_questions = updates.get("questions_or_unknowns") or []
    base_notes = base.get("notes") or []
    update_notes = updates.get("notes") or []

    # Ensure list types
    if not isinstance(base_questions, list):
        base_questions = [str(base_questions)]
    if not isinstance(update_questions, list):
        update_questions = [str(update_questions)]
    if not isinstance(base_notes, list):
        base_notes = [str(base_notes)]
    if not isinstance(update_notes, list):
        update_notes = [str(update_notes)]

    merged_questions: List[str] = base_questions + update_questions
    merged_notes: List[str] = base_notes + update_notes

    # After merging scalar fields, any remaining empties get new unknown entries
    for field in merge_fields:
        if not _is_meaningful(merged.get(field)):
            label = field.replace("_", " ")
            msg = f"Still missing {label} after onboarding transcript."
            if msg not in merged_questions:
                merged_questions.append(msg)

    merged["questions_or_unknowns"] = merged_questions
    merged["notes"] = merged_notes

    # Preserve account_id from base
    merged["account_id"] = base.get("account_id", updates.get("account_id", ""))

    # Refresh auto-generated unknowns based on current merged memo,
    # while preserving any custom questions that don't match our auto patterns.
    existing = merged.get("questions_or_unknowns") or []
    if not isinstance(existing, list):
        existing = [str(existing)]
    preserved = [
        str(x)
        for x in existing
        if isinstance(x, str)
        and not (
            x.startswith("Missing ")
            or x.startswith("Still missing ")
            or x.startswith("Business hours timezone missing or unclear.")
        )
    ]
    merged["questions_or_unknowns"] = _dedupe_preserve_order(preserved + compute_questions_or_unknowns(merged))
    merged["notes"] = _dedupe_preserve_order(merged.get("notes") or [])
    return merged


def merge_structured_form(base: Dict[str, Any], form: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge a structured onboarding form into an existing memo.

    - Non-empty form values override existing memo values.
    - Conflicts (base value != form value) are recorded in notes.
    - No new fields are invented beyond keys that already exist in the memo.
    """
    merged = dict(base)

    notes = merged.get("notes") or []
    if not isinstance(notes, list):
        notes = [str(notes)]

    for field, form_value in form.items():
        if field not in merged:
            # Ignore unknown fields to avoid silently changing schema.
            continue

        new_val = form_value.strip() if isinstance(form_value, str) else form_value
        if not _is_meaningful(new_val):
            continue

        # Normalize known schema fields if form supplies strings
        if field == "business_hours" and isinstance(new_val, str):
            new_val = parse_business_hours_text(new_val)
        if field == "call_transfer_rules" and isinstance(new_val, str):
            new_val = parse_transfer_rules_text(new_val)
        if field in ("emergency_routing_rules", "non_emergency_routing_rules") and isinstance(new_val, str):
            new_val = {"raw": new_val.strip(), "steps": [new_val.strip()]}

        previous = merged.get(field)
        if previous == new_val:
            continue

        # Dict merge (form fills in only provided keys)
        if isinstance(previous, dict) and isinstance(new_val, dict):
            merged_dict, key_notes = _merge_dict_nonempty(previous, new_val)
            if key_notes:
                notes.append(
                    f"Structured form override for '{field}': " + "; ".join(key_notes) + "."
                )
            merged[field] = merged_dict
            continue

        # Record conflict if there was a previous non-empty value
        if _is_meaningful(previous):
            notes.append(
                f"Structured form override for '{field}': "
                f"previous value={previous!r}, new value={new_val!r}."
            )

        merged[field] = new_val

    merged["notes"] = _dedupe_preserve_order(notes if isinstance(notes, list) else [str(notes)])
    merged["questions_or_unknowns"] = _dedupe_preserve_order(
        compute_questions_or_unknowns(merged) + (merged.get("questions_or_unknowns") or [])
    )
    return merged


def main():
    parser = argparse.ArgumentParser(
        description="Apply onboarding transcript updates to an existing memo.json."
    )
    parser.add_argument("--base-memo", required=True, help="Path to base v1 memo.json")
    parser.add_argument(
        "--onboarding-transcript",
        required=True,
        help="Path to onboarding chat.txt transcript",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Where to write updated memo.json (v2)",
    )
    parser.add_argument(
        "--onboarding-form",
        help="Optional path to structured onboarding form JSON to merge on top of transcripts.",
    )
    args = parser.parse_args()

    base_memo_path = Path(args.base_memo).resolve()
    if not base_memo_path.is_file():
        raise FileNotFoundError(f"Base memo not found: {base_memo_path}")

    onboarding_transcript_path = Path(args.onboarding_transcript).resolve()
    if not onboarding_transcript_path.is_file():
        raise FileNotFoundError(f"Onboarding transcript not found: {onboarding_transcript_path}")

    base_memo = json.loads(base_memo_path.read_text(encoding="utf-8"))
    account_id = base_memo.get("account_id") or onboarding_transcript_path.parent.name

    onboarding_memo = build_memo_from_transcript(account_id, onboarding_transcript_path)
    merged_memo = merge_memos(base_memo, onboarding_memo)

    # Optional structured form merge
    if args.onboarding_form:
        form_path = Path(args.onboarding_form).resolve()
        if not form_path.is_file():
            raise FileNotFoundError(f"Onboarding form not found: {form_path}")
        form_data = json.loads(form_path.read_text(encoding="utf-8"))
        merged_memo = merge_structured_form(merged_memo, form_data)

    output_path = Path(args.output).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(merged_memo, f, indent=2, ensure_ascii=False)

    print(f"Wrote merged v2 memo for account '{account_id}' to {output_path}")


if __name__ == "__main__":
    main()