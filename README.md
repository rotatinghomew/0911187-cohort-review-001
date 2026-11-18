# 培养队列复盘

本地分析研究生的入组批次、招生来源、阶段资料覆盖与研究方向形成时间。学生档案的 `student_id` 是稳定标识；`entry_date`、`admission_source`、`stable_direction_date` 描述当前记录，`stages` 中的 `pending` 表示尚未观察到，不代表没有进展。

## 数据约定

输入为 UTF-8 JSON 数组。日期采用 ISO 8601 格式。分析分别报告观察到方向形成的学生、尚无该日期的学生以及培养阶段记录覆盖率；缺少阶段记录时覆盖率为 `null`，不会把未观察到解释为零。项目当前只生成基于给定档案修订号的报告，不保存历史复盘档案。

## 运行与测试

需要 Python 3.11 或更新版本，不依赖外部服务。执行 `PYTHONPATH=src python -m unittest discover -s tests -v` 运行测试。示例资料见 `examples/sample.json`；`cohort_review.facts.load_records` 读取档案，`cohort_review.analysis.summarize` 计算分层指标，`cohort_review.reports.build_report` 绑定来源修订号。

## 目录

- `src/cohort_review/facts.py`：学生档案读取与身份校验。
- `src/cohort_review/cohorts.py`：培养复盘的人群筛选。
- `src/cohort_review/analysis.py`：队列阶段覆盖和方向形成时间。
- `src/cohort_review/reports.py`：带来源修订号的分析结果。
- `examples/`：本地合成数据。
- `tests/`：输入边界与当前业务口径测试。
