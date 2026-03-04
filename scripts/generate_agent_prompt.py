#!/usr/bin/env python
import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


def load_memo(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _as_text(value: Any, label: str) -> str:
    """
    Render memo values to prompt-safe text without inventing data.
    """
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        items = [str(x).strip() for x in value if str(x).strip()]
        if not items:
            return ""
        return "\n".join(f"- {x}" for x in items)
    if isinstance(value, dict):
        # Common patterns used in this pipeline:
        # - business_hours: {raw, days, start, end, timezone}
        # - routing rules: {raw, steps}
        if "raw" in value and isinstance(value.get("raw"), str) and value.get("raw").strip():
            return value.get("raw").strip()
        # Try a compact description for business_hours if raw missing
        if set(value.keys()) >= {"days", "start", "end", "timezone"}:
            days = value.get("days") or []
            start = value.get("start") or ""
            end = value.get("end") or ""
            tz = value.get("timezone") or ""
            parts: List[str] = []
            if days:
                parts.append("days=" + ",".join([str(d) for d in days]))
            if start and end:
                parts.append(f"hours={start}-{end}")
            if tz:
                parts.append(f"timezone={tz}")
            return "; ".join(parts).strip()
        # Fallback: JSON dump
        return json.dumps(value, indent=2, ensure_ascii=False)
    return str(value).strip()


def build_system_prompt(memo: Dict[str, Any]) -> str:
    """
    Construct a deterministic, template-based system prompt without hallucinating.
    Missing data is explicitly called out as unknown.
    """
    company_name = memo.get("company_name") or memo.get("account_id") or "the account"
    business_hours = memo.get("business_hours", "")
    after_hours_flow = memo.get("after_hours_flow_summary", "")
    office_hours_flow = memo.get("office_hours_flow_summary", "")
    emergency_def = memo.get("emergency_definition", "")
    emergency_routing = memo.get("emergency_routing_rules", "")
    non_emergency_routing = memo.get("non_emergency_routing_rules", "")
    call_transfer_rules = memo.get("call_transfer_rules", "")
    questions = memo.get("questions_or_unknowns") or []

    def or_unknown(label: str, value: str) -> str:
        if value:
            return value
        return f"[UNKNOWN: {label} – if caller asks, say you do not have this information yet and collect it for a human follow-up.]"

    prompt_parts = []

    prompt_parts.append(
        f"You are an AI voice agent answering calls for {company_name}. "
        "You must only use information explicitly provided below. "
        "If you are unsure or information is missing, you must transparently say so and follow the fallback instructions."
    )

    # Business hours call flow (strict step list from assignment)
    prompt_parts.append("\n=== Business Hours Call Flow ===")
    prompt_parts.append(
        "Business hours description:\n"
        f"{or_unknown('business hours', _as_text(business_hours, 'business_hours'))}"
    )
    prompt_parts.append(
        "During business hours, follow **exactly** this sequence. Do not skip steps, "
        "and do not add new ones:\n"
        "1. Greeting: Greet the caller on behalf of the business and state that you are an AI assistant.\n"
        "2. Ask purpose: Ask the caller for the reason for their call.\n"
        "3. Collect name and number: Collect the caller's name and callback phone number early in the call.\n"
        "4. Determine routing: Based only on the rules below and the memo:\n"
        f"   - Office-hours flow summary: {or_unknown('office hours call flow summary', _as_text(office_hours_flow, 'office_hours_flow_summary'))}\n"
        "   - Do not guess routes that are not specified.\n"
        "5. Transfer or route: If routing requires a live person, follow the transfer protocol section.\n"
        "6. Fallback if transfer fails: If the transfer fails, drops, or no one answers, follow the "
        "'Transfer Failure Handling' section.\n"
        "7. Ask if they need anything else.\n"
        "8. Close the call politely if they do not need anything else."
    )

    # After-hours call flow (strict step list from assignment)
    prompt_parts.append("\n=== After-Hours Call Flow ===")
    prompt_parts.append(
        "After-hours flow description:\n"
        f"{or_unknown('after-hours flow summary', _as_text(after_hours_flow, 'after_hours_flow_summary'))}"
    )
    prompt_parts.append(
        "During after-hours, follow **exactly** this sequence. Do not skip steps, "
        "and do not add new ones:\n"
        "1. Greeting: Greet the caller on behalf of the business and clarify that it is after hours.\n"
        "2. Ask purpose: Ask the caller for the reason for their call.\n"
        "3. Confirm emergency: Determine whether the call is an emergency using the emergency definition "
        "and routing rules below.\n"
        "4. If emergency:\n"
        "   - Immediately collect the caller's name, callback number, and service address/location.\n"
        "   - Follow the emergency routing rules.\n"
        "5. Attempt transfer: If routing requires a live person, follow the transfer protocol.\n"
        "6. If transfer fails: Apologize briefly, assure the caller that a human will follow up as soon as possible, "
        "and capture all necessary details.\n"
        "7. If non-emergency: Collect relevant details and confirm that a human will follow up during business hours.\n"
        "8. Ask if they need anything else.\n"
        "9. Close the call politely."
    )

    # Emergency handling
    prompt_parts.append("\n=== Emergency Handling ===")
    prompt_parts.append(
        "Definition / examples of emergencies:\n"
        f"{or_unknown('emergency definition', _as_text(emergency_def, 'emergency_definition'))}"
    )
    prompt_parts.append(
        "Routing rules for emergencies:\n"
        f"{or_unknown('emergency routing rules', _as_text(emergency_routing, 'emergency_routing_rules'))}"
    )
    prompt_parts.append(
        "Routing rules for non-emergencies:\n"
        f"{or_unknown('non-emergency routing rules', _as_text(non_emergency_routing, 'non_emergency_routing_rules'))}"
    )

    # Call transfer protocol
    prompt_parts.append("\n=== Call Transfer Protocol ===")
    prompt_parts.append(
        f"{or_unknown('call transfer rules', _as_text(call_transfer_rules, 'call_transfer_rules'))}"
    )
    prompt_parts.append(
        "If you initiate a transfer, clearly tell the caller who you are transferring to and why."
    )

    # Transfer failure handling
    prompt_parts.append("\n=== Transfer Failure Handling ===")
    prompt_parts.append(
        "If a transfer fails, drops, or no one answers:\n"
        "- Return to the caller.\n"
        "- Apologize briefly for the issue.\n"
        "- Offer to take a detailed message including name, callback number, reason for calling, and any constraints.\n"
        "- Clearly state what will happen next (for example: 'A staff member will call you back as soon as possible during business hours.').\n"
        "- Never promise an exact callback time unless explicitly provided in the memo."
    )

    # Caller closing procedure
    prompt_parts.append("\n=== Caller Closing Procedure ===")
    prompt_parts.append(
        "When ending any call:\n"
        "- Confirm you have captured all key details accurately.\n"
        "- Summarize next steps in one or two sentences.\n"
        "- Ask if the caller needs anything else.\n"
        "- Thank the caller on behalf of the business.\n"
        "- End the call politely."
    )

    # Questions / unknowns
    prompt_parts.append("\n=== Known Questions or Unknowns ===")
    if questions:
        prompt_parts.append(
            "The following items are not yet clearly defined from the account materials. "
            "If they come up, collect information and flag for human review, and do NOT guess:"
        )
        for q in questions:
            prompt_parts.append(f"- {q}")
    else:
        prompt_parts.append(
            "There are currently no tracked unknowns, but you still must not invent new facts."
        )

    return "\n".join(prompt_parts).strip()


def build_agent_spec(memo: Dict[str, Any], version: str) -> Dict[str, Any]:
    account_id = memo.get("account_id", "unknown_account")
    company_name = memo.get("company_name") or account_id

    agent_name = f"{company_name} – Clara Answers Agent v{version}"

    agent_spec = {
        "agent_name": agent_name,
        "voice_style": "professional, calm, concise, and empathetic",
        "system_prompt": build_system_prompt(memo),
        "key_variables": {
            "account_id": account_id,
            "company_name": company_name,
            "business_hours": memo.get("business_hours", {}),
            "office_address": memo.get("office_address", ""),
            "timezone": (memo.get("business_hours") or {}).get("timezone") if isinstance(memo.get("business_hours"), dict) else "",
            "emergency_routing": memo.get("emergency_routing_rules", {}),
        },
        "tool_invocation_placeholders": {
            "capture_message": {
                "description": "Store caller details for human follow-up (internal only).",
                "inputs": ["caller_name", "callback_number", "reason", "address_or_location", "urgency"],
            },
            "handoff_to_dispatch": {
                "description": "Initiate a transfer/handoff to dispatch per routing rules (internal only).",
                "inputs": ["routing_target", "reason"],
            },
        },
        "call_transfer_protocol": memo.get("call_transfer_rules", {}),
        "fallback_protocol": (
            "If required information is missing or unclear based on the memo, "
            "politely tell the caller that you do not have that information yet, "
            "collect relevant details, and clearly state that a human staff member will follow up."
        ),
        "version": f"v{version}",
    }
    return agent_spec


def main():
    parser = argparse.ArgumentParser(
        description="Generate Retell Agent Draft Spec JSON from an account memo."
    )
    parser.add_argument("--memo", required=True, help="Path to memo.json")
    parser.add_argument(
        "--version",
        required=True,
        help="Version label (e.g., 1 or 2). Will be formatted as v<version>.",
    )
    parser.add_argument("--output", required=True, help="Path to write agent.json")
    args = parser.parse_args()

    memo_path = Path(args.memo).resolve()
    if not memo_path.is_file():
        raise FileNotFoundError(f"Memo not found: {memo_path}")

    memo = load_memo(memo_path)
    agent_spec = build_agent_spec(memo, args.version)

    output_path = Path(args.output).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(agent_spec, f, indent=2, ensure_ascii=False)

    print(f"Wrote agent spec (v{args.version}) to {output_path}")


if __name__ == "__main__":
    main()