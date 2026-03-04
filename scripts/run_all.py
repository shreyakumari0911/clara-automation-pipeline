#!/usr/bin/env python
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import List

from extract_account_data import build_memo as build_memo_from_transcript
from generate_agent_prompt import build_agent_spec
from apply_patch import merge_memos, merge_structured_form
from task_tracker_mock import upsert_task


class RunLogger:
    def __init__(self, global_log_path: Path):
        self.global_log_path = global_log_path
        self.global_log_path.parent.mkdir(parents=True, exist_ok=True)
        self.global_log_path.write_text("", encoding="utf-8")

    def _ts(self) -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    def _write(self, path: Path, level: str, msg: str) -> None:
        line = f"{self._ts()} [{level}] {msg}\n"
        with path.open("a", encoding="utf-8") as f:
            f.write(line)

    def info(self, msg: str) -> None:
        print(f"[INFO] {msg}")
        self._write(self.global_log_path, "INFO", msg)

    def warn(self, msg: str) -> None:
        print(f"[WARN] {msg}")
        self._write(self.global_log_path, "WARN", msg)

    def error(self, msg: str) -> None:
        print(f"[ERROR] {msg}")
        self._write(self.global_log_path, "ERROR", msg)


def find_accounts(root: Path) -> List[str]:
    """
    Return list of account IDs inferred from subdirectories under demo_calls/.
    """
    if not root.is_dir():
        return []
    return sorted([p.name for p in root.iterdir() if p.is_dir()])


def run_for_account(
    account_id: str,
    demo_root: Path,
    onboarding_root: Path,
    outputs_root: Path,
    logger: RunLogger,
) -> None:
    demo_transcript = demo_root / account_id / "chat.txt"
    if not demo_transcript.is_file():
        logger.warn(f"Skipping account '{account_id}' – missing demo transcript at {demo_transcript}")
        return

    account_dir = outputs_root / "accounts" / account_id
    v1_dir = account_dir / "v1"
    v2_dir = account_dir / "v2"
    account_log_path = account_dir / "pipeline.log"
    account_dir.mkdir(parents=True, exist_ok=True)
    account_log_path.write_text("", encoding="utf-8")

    def account_info(msg: str) -> None:
        logger.info(f"{account_id}: {msg}")
        with account_log_path.open("a", encoding="utf-8") as f:
            f.write(f"{datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} [INFO] {msg}\n")

    def account_warn(msg: str) -> None:
        logger.warn(f"{account_id}: {msg}")
        with account_log_path.open("a", encoding="utf-8") as f:
            f.write(f"{datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} [WARN] {msg}\n")

    # v1
    v1_dir.mkdir(parents=True, exist_ok=True)
    memo_v1_path = v1_dir / "memo.json"
    agent_v1_path = v1_dir / "agent.json"

    account_info("Generating v1 from demo transcript")
    memo_v1 = build_memo_from_transcript(account_id, demo_transcript)
    memo_v1_path.write_text(json.dumps(memo_v1, indent=2, ensure_ascii=False), encoding="utf-8")

    agent_v1 = build_agent_spec(memo_v1, version="1")
    agent_v1_path.write_text(json.dumps(agent_v1, indent=2, ensure_ascii=False), encoding="utf-8")

    # Create/update a tracking item (mock task tracker)
    upsert_task(
        outputs_root / "tasks.json",
        account_id=account_id,
        stage="demo_processed",
        payload={
            "status": "open",
            "summary": f"Demo processed for {account_id}; v1 memo/agent generated.",
            "links": {
                "memo_v1": str(memo_v1_path.relative_to(outputs_root)),
                "agent_v1": str(agent_v1_path.relative_to(outputs_root)),
            },
        },
    )

    # v2 (if onboarding exists)
    onboarding_transcript = onboarding_root / account_id / "chat.txt"
    if not onboarding_transcript.is_file():
        account_info("No onboarding transcript found. Only v1 generated.")
        return

    account_info("Found onboarding transcript – generating v2 and changelog")
    v2_dir.mkdir(parents=True, exist_ok=True)
    memo_v2_path = v2_dir / "memo.json"
    agent_v2_path = v2_dir / "agent.json"
    changelog_path = v2_dir / "changelog.md"

    memo_onboarding = build_memo_from_transcript(account_id, onboarding_transcript)
    memo_v2 = merge_memos(memo_v1, memo_onboarding)

    # Optional structured onboarding form alongside call transcript
    form_path = onboarding_root / account_id / "form.json"
    if form_path.is_file():
        account_info("Found structured onboarding form – merging on top of transcripts")
        form_data = json.loads(form_path.read_text(encoding="utf-8"))
        memo_v2 = merge_structured_form(memo_v2, form_data)
    memo_v2_path.write_text(json.dumps(memo_v2, indent=2, ensure_ascii=False), encoding="utf-8")

    agent_v2 = build_agent_spec(memo_v2, version="2")
    agent_v2_path.write_text(json.dumps(agent_v2, indent=2, ensure_ascii=False), encoding="utf-8")

    # Generate changelog using in-process diff logic similar to diff_generator
    from diff_generator import dict_diff  # local import to avoid circulars

    changelog_sections = [
        "# Changelog",
        "",
        dict_diff(memo_v1, memo_v2, "Account Memo Changes"),
        dict_diff(agent_v1, agent_v2, "Agent Spec Changes"),
    ]
    changelog_content = "\n".join(changelog_sections).strip() + "\n"
    changelog_path.write_text(changelog_content, encoding="utf-8")

    account_info("Generated v2 memo, agent, and changelog")

    upsert_task(
        outputs_root / "tasks.json",
        account_id=account_id,
        stage="onboarding_processed",
        payload={
            "status": "open",
            "summary": f"Onboarding processed for {account_id}; v2 memo/agent generated with changelog.",
            "links": {
                "memo_v2": str(memo_v2_path.relative_to(outputs_root)),
                "agent_v2": str(agent_v2_path.relative_to(outputs_root)),
                "changelog": str(changelog_path.relative_to(outputs_root)),
            },
        },
    )


def main():
    parser = argparse.ArgumentParser(
        description="Batch process all demo and onboarding transcripts into structured outputs."
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Repository root (defaults to current directory).",
    )
    parser.add_argument(
        "--demo-dir",
        default="demo_calls",
        help="Relative path to demo calls directory.",
    )
    parser.add_argument(
        "--onboarding-dir",
        default="onboarding_calls",
        help="Relative path to onboarding calls directory.",
    )
    parser.add_argument(
        "--outputs-dir",
        default="outputs",
        help="Relative path to outputs directory.",
    )
    args = parser.parse_args()

    repo_root = Path(args.root).resolve()
    demo_root = repo_root / args.demo_dir
    onboarding_root = repo_root / args.onboarding_dir
    outputs_root = repo_root / args.outputs_dir
    outputs_root.mkdir(parents=True, exist_ok=True)
    logger = RunLogger(outputs_root / "pipeline.log")

    accounts = find_accounts(demo_root)
    if not accounts:
        logger.warn(f"No accounts found under {demo_root}. Nothing to do.")
        return

    logger.info(f"Found accounts: {', '.join(accounts)}")
    if len(accounts) < 5:
        logger.warn(
            f"Dataset currently has {len(accounts)} demo accounts. Assignment expects 5 demo + 5 onboarding pairs; "
            "pipeline supports any count."
        )

    for account_id in accounts:
        run_for_account(account_id, demo_root, onboarding_root, outputs_root, logger)

    logger.info("Done.")


if __name__ == "__main__":
    main()