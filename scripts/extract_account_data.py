#!/usr/bin/env python
import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


MEMO_FIELDS = [
    "account_id",
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
    "questions_or_unknowns",
    "notes",
]

WEEKDAY_ORDER = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
WEEKDAY_ALIASES = {
    "monday": "mon",
    "mon": "mon",
    "tuesday": "tue",
    "tue": "tue",
    "tues": "tue",
    "wednesday": "wed",
    "wed": "wed",
    "thursday": "thu",
    "thu": "thu",
    "thur": "thu",
    "thurs": "thu",
    "friday": "fri",
    "fri": "fri",
    "saturday": "sat",
    "sat": "sat",
    "sunday": "sun",
    "sun": "sun",
}


def _dedupe_preserve_order(items: List[str]) -> List[str]:
    seen = set()
    out: List[str] = []
    for x in items:
        s = str(x).strip()
        if not s or s in seen:
            continue
        seen.add(s)
        out.append(s)
    return out


def _split_listish(text: str) -> List[str]:
    """
    Split a natural-language list into items. Conservative: only splits on commas and 'or/and' tokens.
    """
    if not text:
        return []
    t = re.sub(r"\s+", " ", text).strip()
    # Normalize separators
    t = re.sub(r"\s+\b(or|and)\b\s+", ", ", t, flags=re.IGNORECASE)
    parts = [p.strip(" .;:-") for p in t.split(",")]
    parts = [p for p in parts if p]
    return _dedupe_preserve_order(parts)


def _parse_time_token(token: str) -> Optional[str]:
    """
    Parse times like '8am', '8:00 AM', '17:30' into HH:MM (24h). Returns None if not parseable.
    """
    if not token:
        return None
    t = token.strip().lower().replace(".", "")
    m = re.match(r"^(?P<h>\d{1,2})(:(?P<m>\d{2}))?\s*(?P<ampm>am|pm)?$", t)
    if not m:
        return None
    hour = int(m.group("h"))
    minute = int(m.group("m") or "00")
    ampm = m.group("ampm")
    if ampm:
        if hour == 12:
            hour = 0
        if ampm == "pm":
            hour += 12
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        return None
    return f"{hour:02d}:{minute:02d}"


def _parse_timezone(text: str) -> str:
    if not text:
        return ""
    lower = text.lower()
    # Return a short, common label if present; otherwise empty.
    if "pacific" in lower or re.search(r"\bpt\b", lower):
        return "PT"
    if "eastern" in lower or re.search(r"\bet\b", lower):
        return "ET"
    if "central" in lower or re.search(r"\bct\b", lower):
        return "CT"
    if "mountain" in lower or re.search(r"\bmt\b", lower):
        return "MT"
    return ""


def _parse_weekdays(text: str) -> List[str]:
    if not text:
        return []
    lower = text.lower().replace("–", "-").replace("—", "-")
    # Range form: mon-fri / monday through friday / monday to friday
    range_match = re.search(
        r"\b(?P<d1>mon(day)?|tue(s(day)?)?|wed(nesday)?|thu(r(s(day)?)?)?|fri(day)?|sat(urday)?|sun(day)?)\b"
        r"\s*(through|to|-)\s*"
        r"\b(?P<d2>mon(day)?|tue(s(day)?)?|wed(nesday)?|thu(r(s(day)?)?)?|fri(day)?|sat(urday)?|sun(day)?)\b",
        lower,
        flags=re.IGNORECASE,
    )
    if range_match:
        d1 = WEEKDAY_ALIASES.get(range_match.group("d1").lower(), "")
        d2 = WEEKDAY_ALIASES.get(range_match.group("d2").lower(), "")
        if d1 and d2 and d1 in WEEKDAY_ORDER and d2 in WEEKDAY_ORDER:
            i1 = WEEKDAY_ORDER.index(d1)
            i2 = WEEKDAY_ORDER.index(d2)
            if i1 <= i2:
                return WEEKDAY_ORDER[i1 : i2 + 1]
            # wrap-around ranges are rare; keep conservative and return empty
    # Explicit list: "Mon, Wed, Fri"
    hits = []
    for w, canon in WEEKDAY_ALIASES.items():
        if re.search(rf"\b{re.escape(w)}\b", lower):
            hits.append(canon)
    # Preserve order mon..sun for consistency
    return [d for d in WEEKDAY_ORDER if d in set(hits)]


def _parse_hours_from_text(text: str) -> Dict[str, Any]:
    """
    Returns structured business hours:
    {
      "days": ["mon", ...],
      "start": "HH:MM",
      "end": "HH:MM",
      "timezone": "PT",
      "raw": "<original>"
    }
    Any missing info remains empty.
    """
    raw = text or ""
    days = _parse_weekdays(raw)
    tz = _parse_timezone(raw)

    # Common patterns: "8am to 5pm", "8:00 AM - 5:00 PM"
    tm = re.search(
        r"(?P<t1>\d{1,2}(:\d{2})?\s*(am|pm)?)\s*(to|-)\s*(?P<t2>\d{1,2}(:\d{2})?\s*(am|pm)?)",
        raw,
        flags=re.IGNORECASE,
    )
    start = end = ""
    if tm:
        start = _parse_time_token(tm.group("t1")) or ""
        end = _parse_time_token(tm.group("t2")) or ""

    return {"days": days, "start": start, "end": end, "timezone": tz, "raw": raw}


def parse_business_hours_text(text: str) -> Dict[str, Any]:
    """
    Public helper for normalizing form-provided business hours strings.
    """
    return _parse_hours_from_text(text)

def read_transcript(path: Path) -> List[str]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return lines


def guess_company_name(lines: List[str]) -> str:
    """
    Heuristic: look for lines like:
    - "Company: Acme Dental"
    - "This is Acme Dental"
    - "Welcome to Acme Dental"
    """
    company_patterns = [
        r"company\s*[:\-]\s*(.+)$",
        r"this is\s+(.+)$",
        r"welcome to\s+(.+)$",
    ]
    for line in lines:
        lower = line.lower()
        for pat in company_patterns:
            m = re.search(pat, lower, flags=re.IGNORECASE)
            if m:
                start = m.start(1)
                return line[start:].strip(". ")
    return ""


def extract_business_hours(lines: List[str]) -> Dict[str, Any]:
    """
    Look for keywords like 'business hours', 'office hours', 'open from'.
    Returns a free-text summary line.
    """
    # Prefer lines that actually include days/times (to avoid matching generic phrases like
    # "scheduled during business hours").
    weekday_words = [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
        "mon",
        "tue",
        "wed",
        "thu",
        "fri",
        "sat",
        "sun",
    ]
    time_markers = ["am", "pm", "a.m", "p.m", ":", "00"]

    def has_day_or_time(s: str) -> bool:
        lower = s.lower()
        return any(w in lower for w in weekday_words) or any(t in lower for t in time_markers) or bool(
            re.search(r"\b\d{1,2}\b", lower)
        )

    # Strong candidates
    for line in lines:
        lower = line.lower()
        if any(k in lower for k in ["we're open", "we are open", "open from", "hours are", "business hours are"]):
            if has_day_or_time(line):
                return _parse_hours_from_text(line.strip())

    # Secondary candidates: explicit "business hours:" / "office hours:" lines (only if they include days/times)
    for line in lines:
        lower = line.lower()
        if any(k in lower for k in ["business hours", "office hours"]):
            if has_day_or_time(line):
                return _parse_hours_from_text(line.strip())

    # As a last resort, use regex over the joined text, but still require day/time
    joined = " ".join(lines)
    patterns = [
        r"((business hours|office hours)\s*(are|:)[^.]*\.)",
        r"((we[’']?re open|we are open|open from)[^.]*\.)",
    ]
    for pat in patterns:
        m = re.search(pat, joined, flags=re.IGNORECASE)
        if m and has_day_or_time(m.group(1)):
            return _parse_hours_from_text(m.group(1).strip())

    return {"days": [], "start": "", "end": "", "timezone": "", "raw": ""}


def extract_office_address(lines: List[str]) -> str:
    """
    Heuristics:
    - Prefer explicit "Address:" / "Office Address:" lines.
    - Otherwise, look for lines that resemble a street address (starts with a number and contains a common suffix).
    - Avoid false positives like "first" matching "st".
    """
    for line in lines:
        m = re.match(r"^\s*(office\s+address|address)\s*:\s*(.+)\s*$", line, flags=re.IGNORECASE)
        if m:
            return m.group(2).strip()

    # Look for numeric-leading address patterns with suffix words
    suffix_re = re.compile(
        r"\b(street|st\.|st|road|rd\.|rd|avenue|ave\.|ave|boulevard|blvd\.|blvd|suite|ste\.|ste|floor)\b",
        flags=re.IGNORECASE,
    )
    for line in lines:
        if not re.match(r"^\s*\d{1,6}\s+\S+", line):
            continue
        if suffix_re.search(line):
            return line.strip()
    return ""


def extract_services_supported(lines: List[str]) -> str:
    """
    Look for lines mentioning 'we handle', 'we can help with', 'services we provide', etc.
    Returns a free-text summary.
    """
    patterns = [
        r"(services (we|that we) (provide|offer)[^.]*\.)",
        r"(we (handle|take care of|support)[^.]*\.)",
        r"(we can help with[^.]*\.)",
    ]
    joined = " ".join(lines)
    for pat in patterns:
        m = re.search(pat, joined, flags=re.IGNORECASE)
        if m:
            return m.group(1).strip()
    for line in lines:
        if any(kw in line.lower() for kw in ["services we", "we handle", "we support", "we can help"]):
            return line.strip()
    return ""


def extract_emergency_definition(lines: List[str]) -> List[str]:
    patterns = [
        r"(an emergency (is|would be)[^.]*\.)",
        r"(we consider (it )?an emergency[^.]*\.)",
    ]
    joined = " ".join(lines)
    for pat in patterns:
        m = re.search(pat, joined, flags=re.IGNORECASE)
        if m:
            s = m.group(1).strip()
            # Try to isolate the "is ..." clause
            rhs = re.split(r"\bis\b", s, maxsplit=1, flags=re.IGNORECASE)
            if len(rhs) == 2:
                return _split_listish(rhs[1])
            return _split_listish(s)
    for line in lines:
        if "emergency" in line.lower() and ("consider" in line.lower() or "define" in line.lower()):
            rhs = re.split(r"\bis\b", line, maxsplit=1, flags=re.IGNORECASE)
            if len(rhs) == 2:
                return _split_listish(rhs[1])
            return _split_listish(line.strip())
    return []


def extract_routing_rules(lines: List[str]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Try to separate emergency vs non-emergency routing instructions.
    """
    emergency_lines: List[str] = []
    non_emergency_lines: List[str] = []
    for line in lines:
        lower = line.lower()
        is_non_emergency = any(k in lower for k in ["non-emergency", "non emergency", "not an emergency"])
        has_routing_word = any(k in lower for k in ["route", "transfer", "forward", "call", "phone tree"])

        if is_non_emergency and has_routing_word:
            non_emergency_lines.append(line.strip())
            continue

        # Emergency should match "emergency" or "emergencies" (but not "non-emergency")
        if re.search(r"\bemergenc(y|ies)\b", lower) and not is_non_emergency and has_routing_word:
            emergency_lines.append(line.strip())
    emergency_raw = " ".join(emergency_lines).strip()
    non_emergency_raw = " ".join(non_emergency_lines).strip()
    return (
        {"raw": emergency_raw, "steps": emergency_lines},
        {"raw": non_emergency_raw, "steps": non_emergency_lines},
    )


def extract_call_transfer_rules(lines: List[str]) -> Dict[str, Any]:
    patterns = [
        r"(transfer (the )?call[^.]*\.)",
        r"(you should transfer[^.]*\.)",
        r"(when you transfer[^.]*\.)",
    ]
    joined = " ".join(lines)
    for pat in patterns:
        m = re.search(pat, joined, flags=re.IGNORECASE)
        if m:
            raw = m.group(1).strip()
            return _parse_transfer_rules(raw)
    for line in lines:
        if "transfer" in line.lower() and "call" in line.lower():
            return _parse_transfer_rules(line.strip())
    return {"raw": "", "timeout_seconds": None, "retries": None, "what_to_say_if_fails": ""}


def _parse_transfer_rules(text: str) -> Dict[str, Any]:
    raw = text or ""
    timeout = None
    m = re.search(r"\bafter\s+(\d{1,4})\s*seconds?\b", raw, flags=re.IGNORECASE)
    if m:
        try:
            timeout = int(m.group(1))
        except ValueError:
            timeout = None
    retry = None
    rm = re.search(r"\b(\d{1,2})\s*retries?\b", raw, flags=re.IGNORECASE)
    if rm:
        try:
            retry = int(rm.group(1))
        except ValueError:
            retry = None
    return {"raw": raw, "timeout_seconds": timeout, "retries": retry, "what_to_say_if_fails": ""}


def parse_transfer_rules_text(text: str) -> Dict[str, Any]:
    """
    Public helper for normalizing form-provided transfer rules strings.
    """
    return _parse_transfer_rules(text)


def compute_questions_or_unknowns(memo: Dict[str, Any]) -> List[str]:
    """
    Compute questions/unknowns purely from the current memo state.
    This prevents stale questions persisting after onboarding overrides.
    """
    q: List[str] = []
    company_name = (memo.get("company_name") or "").strip() if isinstance(memo.get("company_name"), str) else ""
    if not company_name:
        q.append("Missing company name (not found or unclear in transcript).")

    bh = memo.get("business_hours")
    if isinstance(bh, dict):
        if not (bh.get("raw") or bh.get("days") or bh.get("start") or bh.get("end")):
            q.append("Missing business hours (not found or unclear in transcript).")
        if (bh.get("raw") or bh.get("days") or bh.get("start") or bh.get("end")) and not bh.get("timezone"):
            q.append("Business hours timezone missing or unclear.")
    else:
        if not bh:
            q.append("Missing business hours (not found or unclear in transcript).")

    if not (memo.get("office_address") or "").strip():
        q.append("Missing office address (not found or unclear in transcript).")

    services = memo.get("services_supported")
    if not (isinstance(services, list) and len(services) > 0):
        q.append("Missing services supported (not found or unclear in transcript).")

    emergency_def = memo.get("emergency_definition")
    if not (isinstance(emergency_def, list) and len(emergency_def) > 0):
        q.append("Missing emergency definition (not found or unclear in transcript).")

    er = memo.get("emergency_routing_rules")
    if isinstance(er, dict):
        if not (er.get("raw") or ""):
            q.append("Missing emergency routing rules (not found or unclear in transcript).")
    elif not er:
        q.append("Missing emergency routing rules (not found or unclear in transcript).")

    ner = memo.get("non_emergency_routing_rules")
    if isinstance(ner, dict):
        if not (ner.get("raw") or ""):
            q.append("Missing non-emergency routing rules (not found or unclear in transcript).")
    elif not ner:
        q.append("Missing non-emergency routing rules (not found or unclear in transcript).")

    ctr = memo.get("call_transfer_rules")
    if isinstance(ctr, dict):
        if not (ctr.get("raw") or ""):
            q.append("Missing call transfer rules (not found or unclear in transcript).")
    elif not ctr:
        q.append("Missing call transfer rules (not found or unclear in transcript).")

    if not (memo.get("integration_constraints") or "").strip():
        q.append("Missing integration constraints (not found or unclear in transcript).")

    if not (memo.get("after_hours_flow_summary") or "").strip():
        q.append("Missing after-hours flow summary (not found or unclear in transcript).")

    if not (memo.get("office_hours_flow_summary") or "").strip():
        q.append("Missing office-hours flow summary (not found or unclear in transcript).")

    return _dedupe_preserve_order(q)


def extract_integration_constraints(lines: List[str]) -> str:
    """
    Look for mentions of tools: 'EHR', 'CRM', 'calendar', 'no access to', 'only use', etc.
    """
    indicators = [
        "servicetrade",
        "service trade",
        "integration",
        "api",
        "crm",
        "calendar",
        "google calendar",
        "outlook",
        "emr",
        "ehr",
        "sync",
        "create job",
        "create jobs",
        "dispatch software",
    ]
    candidates = [l for l in lines if any(k in l.lower() for k in indicators)]
    if not candidates:
        return ""
    # Combine first few lines into a summary
    return " ".join(candidates[:3]).strip()


def extract_flow_summaries(lines: List[str]) -> Tuple[str, str]:
    """
    Look for 'during business hours', 'after hours', 'if they call after hours', etc.
    """
    office_lines = []
    after_hours_lines = []
    for line in lines:
        lower = line.lower()
        if any(k in lower for k in ["during business hours", "during office hours", "when we're open"]):
            office_lines.append(line.strip())
        if any(k in lower for k in ["after hours", "outside business hours", "when we are closed"]):
            after_hours_lines.append(line.strip())
    return " ".join(office_lines).strip(), " ".join(after_hours_lines).strip()


def build_memo(account_id: str, transcript_path: Path) -> Dict:
    lines = read_transcript(transcript_path)

    company_name = guess_company_name(lines)
    business_hours = extract_business_hours(lines)
    office_address = extract_office_address(lines)
    services_supported_raw = extract_services_supported(lines)
    services_supported = _split_listish(services_supported_raw)
    emergency_definition = extract_emergency_definition(lines)
    emergency_routing_rules, non_emergency_routing_rules = extract_routing_rules(lines)
    call_transfer_rules = extract_call_transfer_rules(lines)
    integration_constraints = extract_integration_constraints(lines)
    office_hours_flow_summary, after_hours_flow_summary = extract_flow_summaries(lines)

    questions_or_unknowns: List[str] = []
    notes: List[str] = []

    # Any field (except account_id) that's empty becomes an entry in questions_or_unknowns
    memo = {
        "account_id": account_id,
        "company_name": company_name,
        "business_hours": business_hours,
        "office_address": office_address,
        "services_supported": services_supported,
        "emergency_definition": emergency_definition,
        "emergency_routing_rules": emergency_routing_rules,
        "non_emergency_routing_rules": non_emergency_routing_rules,
        "call_transfer_rules": call_transfer_rules,
        "integration_constraints": integration_constraints,
        "after_hours_flow_summary": after_hours_flow_summary,
        "office_hours_flow_summary": office_hours_flow_summary,
        "questions_or_unknowns": [],
        "notes": notes,
    }

    memo["questions_or_unknowns"] = compute_questions_or_unknowns(memo)

    # Ensure all required keys exist
    for field in MEMO_FIELDS:
        if field not in memo:
            # Default empty types
            if field in ("questions_or_unknowns", "notes"):
                memo[field] = []
            elif field in ("services_supported", "emergency_definition"):
                memo[field] = []
            elif field == "business_hours":
                memo[field] = {"days": [], "start": "", "end": "", "timezone": "", "raw": ""}
            elif field in ("emergency_routing_rules", "non_emergency_routing_rules"):
                memo[field] = {"raw": "", "steps": []}
            elif field == "call_transfer_rules":
                memo[field] = {"raw": "", "timeout_seconds": None, "retries": None, "what_to_say_if_fails": ""}
            else:
                memo[field] = ""

    return memo


def infer_account_id_from_path(path: Path) -> str:
    """
    By convention, assume the parent directory name is the account_id:
    demo_calls/<account_id>/chat.txt
    onboarding_calls/<account_id>/chat.txt
    """
    return path.parent.name


def main():
    parser = argparse.ArgumentParser(
        description="Extract structured account memo JSON from a transcript."
    )
    parser.add_argument(
        "--transcript",
        required=True,
        help="Path to chat.txt transcript.",
    )
    parser.add_argument(
        "--account-id",
        help="Account ID. If omitted, parent directory name of transcript is used.",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Where to write memo.json",
    )
    args = parser.parse_args()

    transcript_path = Path(args.transcript).resolve()
    if not transcript_path.is_file():
        raise FileNotFoundError(f"Transcript not found: {transcript_path}")

    account_id = args.account_id or infer_account_id_from_path(transcript_path)
    memo = build_memo(account_id, transcript_path)

    output_path = Path(args.output).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(memo, f, indent=2, ensure_ascii=False)

    print(f"Wrote memo JSON for account '{account_id}' to {output_path}")


if __name__ == "__main__":
    main()