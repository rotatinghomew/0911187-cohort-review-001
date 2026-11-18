"""确定培养复盘的人群边界。"""


def select_students(records, admission_source=None, entry_month=None):
    selected = []
    for record in records:
        if admission_source is not None and record.get("admission_source") != admission_source:
            continue
        if entry_month is not None and record.get("entry_month") != entry_month:
            continue
        selected.append(record)
    return selected
