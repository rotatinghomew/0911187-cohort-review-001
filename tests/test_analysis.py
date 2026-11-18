import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cohort_review.analysis import summarize
from cohort_review.reports import build_report


class CohortReviewTests(unittest.TestCase):
    def setUp(self):
        self.records = [
            {
                "student_id": "s-1",
                "entry_date": "2025-09-01",
                "admission_source": "推免",
                "stable_direction_date": "2026-03-01",
                "stages": [{"name": "开题", "status": "observed"}, {"name": "中期", "status": "pending"}],
            },
            {
                "student_id": "s-2",
                "entry_date": "2025-09-01",
                "admission_source": "推免",
                "stable_direction_date": None,
                "stages": [{"name": "开题", "status": "pending"}],
            },
            {
                "student_id": "s-3",
                "entry_date": "2025-10-01",
                "admission_source": "统考",
                "stable_direction_date": "2026-02-01",
                "stages": [],
            },
        ]

    def test_missing_direction_is_not_zero_duration(self):
        groups = summarize(self.records)
        self.assertEqual(groups["推免"]["direction_unobserved"], 1)
        self.assertEqual(groups["推免"]["direction_observed"], 1)
        self.assertEqual(groups["推免"]["median_days_to_direction"], 181)

    def test_stage_coverage_is_separate_from_direction_outcome(self):
        groups = summarize(self.records)
        self.assertEqual(groups["推免"]["stage_coverage"], 1 / 3)
        self.assertIsNone(groups["统考"]["stage_coverage"])

    def test_report_binds_results_to_source_revision(self):
        report = build_report(self.records, source_revision="archive-7")
        self.assertEqual(report["source_revision"], "archive-7")
        self.assertEqual(report["groups"]["统考"]["students"], 1)

    def test_cohort_filter_changes_denominator_before_stage_coverage(self):
        groups = summarize(self.records, admission_source="推免")
        self.assertEqual(set(groups), {"推免"})
        self.assertEqual(groups["推免"]["students"], 2)


if __name__ == "__main__":
    unittest.main()
