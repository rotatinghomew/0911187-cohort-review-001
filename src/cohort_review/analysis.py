"""按培养队列分析研究方向形成时间与阶段资料覆盖。"""

from collections import defaultdict
from .cohorts import select_students


def summarize(records, cohort_field="admission_source", admission_source=None, entry_month=None):
    records = select_students(records, admission_source, entry_month)
    groups = defaultdict(list)
    for record in records:
        group = record.get(cohort_field)
        if not group:
            continue
        groups[str(group)].append(record)
    result = {}
    for group, members in sorted(groups.items()):
        elapsed = []
        stage_observed = 0
        stage_expected = 0
        for member in members:
            for stage in member.get("stages", []):
                stage_expected += 1
                if stage.get("status") == "observed":
                    stage_observed += 1
            stable = member.get("stable_direction_date")
            if stable and member.get("entry_date"):
                elapsed.append((stable, member["entry_date"]))
        result[group] = {
            "students": len(members),
            "direction_observed": len(elapsed),
            "direction_unobserved": len(members) - len(elapsed),
            "median_days_to_direction": _median_days(elapsed),
            "stage_records": stage_expected,
            "stage_records_observed": stage_observed,
            "stage_coverage": stage_observed / stage_expected if stage_expected else None,
        }
    return result


def _median_days(values):
    from datetime import date

    days = sorted((date.fromisoformat(end) - date.fromisoformat(start)).days for end, start in values)
    if not days:
        return None
    middle = len(days) // 2
    if len(days) % 2:
        return days[middle]
    return (days[middle - 1] + days[middle]) / 2
