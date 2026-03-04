#!/usr/bin/env python
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple


def _load_tasks(path: Path) -> List[Dict[str, Any]]:
    if not path.is_file():
        return []
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return []


def _write_tasks(path: Path, tasks: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(tasks, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def upsert_task(tasks_path: Path, account_id: str, stage: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Zero-cost "task tracker" mock.
    Writes/updates a task record in outputs/tasks.json keyed by (account_id, stage).
    """
    tasks = _load_tasks(tasks_path)
    key = f"{account_id}:{stage}"

    existing_idx = None
    for i, t in enumerate(tasks):
        if t.get("task_key") == key:
            existing_idx = i
            break

    record = {
        "task_key": key,
        "account_id": account_id,
        "stage": stage,
        "status": payload.get("status", "open"),
        "summary": payload.get("summary", ""),
        "links": payload.get("links", {}),
        "metadata": payload.get("metadata", {}),
    }

    if existing_idx is None:
        tasks.append(record)
    else:
        tasks[existing_idx] = record

    _write_tasks(tasks_path, tasks)
    return record

