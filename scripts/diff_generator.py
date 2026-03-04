#!/usr/bin/env python
import argparse
import json
import difflib
from pathlib import Path
from typing import Any, Dict


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def dict_diff(v1: Dict[str, Any], v2: Dict[str, Any], title: str) -> str:
    """
    Produce a markdown diff summary between two dicts as a markdown section.
    """
    lines = [f"### {title}", ""]
    all_keys = sorted(set(v1.keys()) | set(v2.keys()))
    for key in all_keys:
        old = v1.get(key)
        new = v2.get(key)
        if old == new:
            continue

        lines.append(f"- **{key}** changed:")

        if isinstance(old, (list, dict)) or isinstance(new, (list, dict)):
            old_str = json.dumps(old, indent=2, ensure_ascii=False)
            new_str = json.dumps(new, indent=2, ensure_ascii=False)
        else:
            old_str = "" if old is None else str(old)
            new_str = "" if new is None else str(new)

        diff = difflib.unified_diff(
            old_str.splitlines(),
            new_str.splitlines(),
            lineterm="",
            fromfile="v1",
            tofile="v2",
        )
        lines.append("```diff")
        for dline in diff:
            lines.append(dline)
        lines.append("```")
        lines.append("")

    if len(lines) == 2:
        lines.append("_No differences detected._")
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a markdown changelog from v1/v2 memo and agent specs."
    )
    parser.add_argument("--v1-memo", required=True, help="Path to v1 memo.json")
    parser.add_argument("--v2-memo", required=True, help="Path to v2 memo.json")
    parser.add_argument("--v1-agent", required=True, help="Path to v1 agent.json")
    parser.add_argument("--v2-agent", required=True, help="Path to v2 agent.json")
    parser.add_argument("--output", required=True, help="Where to write changelog.md")
    args = parser.parse_args()

    v1_memo_path = Path(args.v1_memo).resolve()
    v2_memo_path = Path(args.v2_memo).resolve()
    v1_agent_path = Path(args.v1_agent).resolve()
    v2_agent_path = Path(args.v2_agent).resolve()

    v1_memo = load_json(v1_memo_path)
    v2_memo = load_json(v2_memo_path)
    v1_agent = load_json(v1_agent_path)
    v2_agent = load_json(v2_agent_path)

    sections = [
        "# Changelog",
        "",
        dict_diff(v1_memo, v2_memo, "Account Memo Changes"),
        dict_diff(v1_agent, v2_agent, "Agent Spec Changes"),
    ]
    content = "\n".join(sections).strip() + "\n"

    output_path = Path(args.output).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")

    print(f"Wrote changelog to {output_path}")


if __name__ == "__main__":
    main()