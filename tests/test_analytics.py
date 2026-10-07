import unittest
from modules.analytics import (
    get_summary_stats, donations_by_cause, donations_by_source,
    donations_by_month
)


class TestAnalytics(unittest.TestCase):
    def setUp(self):
        self.donations = [
            {
                "donation_id": "DN1", "donor_id": "D1", "date": "2026-10-01",
                "amount": "1000", "cause": "Education",
                "source": "Individual", "payment_mode": "UPI", "description": ""
            },
            {
                "donation_id": "DN2", "donor_id": "D2", "date": "2026-10-02",
                "amount": "3000", "cause": "Healthcare",
                "source": "Organization", "payment_mode": "Bank Transfer", "description": ""
            },
        ]

    def test_summary(self):
        stats = get_summary_stats(self.donations)
        self.assertEqual(stats["count"], 2)
        self.assertEqual(stats["total"], 4000.0)
        self.assertEqual(stats["maximum"], 3000.0)

    def test_grouping(self):
        cause = donations_by_cause(self.donations)
        source = donations_by_source(self.donations)
        month = donations_by_month(self.donations)

        self.assertEqual(float(cause["Healthcare"]), 3000.0)
        self.assertEqual(float(source["Individual"]), 1000.0)
        self.assertEqual(float(month["2026-10"]), 4000.0)


if __name__ == "__main__":
    unittest.main()
