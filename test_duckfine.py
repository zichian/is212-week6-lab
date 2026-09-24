import unittest

from duckfine import DuckFine


class TestDuckFine(unittest.TestCase):
    def test_initial_state(self):
        fine = DuckFine("M-101")

        self.assertEqual(fine.member_id, "M-101")
        self.assertEqual(fine.total_owed, 0.0)

    def test_charge_negative_days_raises_value_error(self):
        fine = DuckFine("M-101")

        with self.assertRaises(ValueError):
            fine.charge(-1)

    def test_charge_within_grace_period_has_no_fee(self):
        fine = DuckFine("M-101")

        fee = fine.charge(2)

        self.assertEqual(fee, 0.0)
        self.assertEqual(fine.total_owed, 0.0)

    def test_charge_after_grace_period_uses_daily_fee(self):
        fine = DuckFine("M-101")

        fee = fine.charge(5)

        self.assertEqual(fee, 1.5)
        self.assertEqual(fine.total_owed, 1.5)

    def test_deluxe_charge_doubles_and_caps_fee(self):
        fine = DuckFine("M-101")

        fee = fine.charge(20, deluxe=True)

        self.assertEqual(fee, 5.0)
        self.assertEqual(fine.total_owed, 5.0)

    def test_total_owed_accumulates_across_charges(self):
        fine = DuckFine("M-101")

        first_fee = fine.charge(3)
        second_fee = fine.charge(6, deluxe=True)

        self.assertEqual(first_fee, 0.5)
        self.assertEqual(second_fee, 4.0)
        self.assertEqual(fine.total_owed, 4.5)


if __name__ == "__main__":
    unittest.main()
