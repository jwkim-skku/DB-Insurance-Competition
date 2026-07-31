import unittest

from src.merton import calibrate_merton


class MertonCalibrationTests(unittest.TestCase):
    def test_solution_is_economically_valid(self) -> None:
        result = calibrate_merton(
            equity_value=750.0,
            debt=500.0,
            equity_volatility=0.42,
            risk_free_rate=0.025,
        )
        self.assertTrue(result.converged)
        self.assertGreater(result.asset_value, 750.0)
        self.assertGreater(result.asset_volatility, 0.0)
        self.assertGreaterEqual(result.default_probability, 0.0)
        self.assertLessEqual(result.default_probability, 1.0)

    def test_more_debt_increases_default_probability(self) -> None:
        low_debt = calibrate_merton(750.0, 300.0, 0.42, 0.025)
        high_debt = calibrate_merton(750.0, 900.0, 0.42, 0.025)
        self.assertGreater(
            high_debt.default_probability, low_debt.default_probability
        )

    def test_invalid_inputs_raise(self) -> None:
        with self.assertRaises(ValueError):
            calibrate_merton(0.0, 500.0, 0.42, 0.025)


if __name__ == "__main__":
    unittest.main()
