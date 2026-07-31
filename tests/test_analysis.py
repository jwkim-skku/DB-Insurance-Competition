import unittest

import numpy as np

from src.analysis import fit_models, prepare_panel


class PublicAnalysisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.panel = prepare_panel()
        cls.models = fit_models(cls.panel)

    def test_lagged_panel_shape(self) -> None:
        self.assertEqual(len(self.panel), 108)
        self.assertEqual(self.panel["firm_id"].nunique(), 12)

    def test_public_sample_contains_two_positive_risk_estimates(self) -> None:
        model = self.models["dual_pricing"]
        self.assertGreater(model.params["lag_pd_z"], 0.0)
        self.assertGreater(model.params["carbon_z"], 0.0)

    def test_moderation_model_is_numerically_finite(self) -> None:
        model = self.models["esg_moderation"]
        self.assertTrue(np.isfinite(model.params["lag_pd_z:esg_z"]))


if __name__ == "__main__":
    unittest.main()
