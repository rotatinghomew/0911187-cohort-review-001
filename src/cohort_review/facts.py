"""培养档案的读取、稳定身份检查与字段归一化。"""

import json
from pathlib import Path


def load_records(path):
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("记录文件必须包含数组")
    records = []
    seen = set()
    for position, record in enumerate(payload):
        if not isinstance(record, dict) or not record.get("student_id"):
            raise ValueError(f"第 {position + 1} 条档案缺少 student_id")
        student_id = str(record["student_id"])
        if student_id in seen:
            raise ValueError(f"重复学生标识：{student_id}")
        seen.add(student_id)
        if not record.get("entry_date") or not record.get("admission_source"):
            raise ValueError(f"学生 {student_id} 缺少入组日期或招生来源")
        stages = record.get("stages", [])
        if not isinstance(stages, list):
            raise ValueError(f"学生 {student_id} 的 stages 必须是数组")
        records.append({**record, "student_id": student_id, "stages": [dict(stage) for stage in stages]})
    return records
