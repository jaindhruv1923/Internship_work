#!/usr/bin/env python3
"""
Unit Test Suite for Bayesian & Statistical Retention Analytics Engine
Tests ROC-AUC, Brier score, sigmoid calibration, Precision@K, and feature attribution
"""

import os
import sys
import unittest
import math

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
import analytics_engine

class TestAnalyticsEngine(unittest.TestCase):
    def test_sigmoid_numerical_stability(self):
        self.assertEqual(analytics_engine.sigmoid(100.0), 1.0)
        self.assertEqual(analytics_engine.sigmoid(-100.0), 0.0)
        self.assertAlmostEqual(analytics_engine.sigmoid(0.0), 0.5, places=4)

    def test_bayesian_dropout_probability_monotonicity(self):
        low_risk = {"academics": 5.0, "fees": 0.0, "gates": 0.0, "hostel": 0.0, "chc": 0.0}
        high_risk = {"academics": 92.0, "fees": 90.0, "gates": 100.0, "hostel": 95.0, "chc": 25.0}

        p_low = analytics_engine.compute_bayesian_dropout_probability(low_risk)
        p_high = analytics_engine.compute_bayesian_dropout_probability(high_risk)

        self.assertTrue(p_low < 0.10, f"Expected low risk < 0.10, got {p_low}")
        self.assertTrue(p_high > 0.85, f"Expected high risk > 0.85, got {p_high}")

    def test_roc_auc_perfect_discrimination(self):
        # Perfectly separable scores
        scores = [10.0, 20.0, 30.0, 80.0, 90.0]
        labels = [0, 0, 0, 1, 1]
        auc = analytics_engine.evaluate_roc_auc(scores, labels)
        self.assertEqual(auc, 1.0)

    def test_roc_auc_imperfect_discrimination(self):
        scores = [10.0, 60.0, 30.0, 80.0, 50.0]
        labels = [0, 0, 0, 1, 1]
        auc = analytics_engine.evaluate_roc_auc(scores, labels)
        self.assertTrue(0.70 <= auc <= 1.0, f"Expected reasonable AUC, got {auc}")

    def test_brier_calibration_score(self):
        # Perfect predictions
        brier_perfect = analytics_engine.evaluate_brier_score([1.0, 0.0], [1, 0])
        self.assertEqual(brier_perfect, 0.0)

        # Realistic probabilities
        brier_real = analytics_engine.evaluate_brier_score([0.9, 0.1], [1, 0])
        self.assertAlmostEqual(brier_real, 0.01, places=3)

    def test_precision_at_k(self):
        scores = [95.0, 85.0, 70.0, 40.0, 20.0]
        labels = [1, 1, 0, 0, 0]
        self.assertEqual(analytics_engine.evaluate_precision_at_k(scores, labels, k=1), 1.0)
        self.assertEqual(analytics_engine.evaluate_precision_at_k(scores, labels, k=2), 1.0)
        self.assertAlmostEqual(analytics_engine.evaluate_precision_at_k(scores, labels, k=4), 0.5, places=2)

    def test_feature_attribution_sum_100(self):
        sub_scores = {"academics": 92.2, "fees": 90.8, "gates": 100.0, "hostel": 95.0, "chc": 25.0}
        attribution = analytics_engine.calculate_feature_attribution(sub_scores)
        total = sum(attribution.values())
        self.assertAlmostEqual(total, 100.0, delta=1.0)
        # Academic should be a major driver
        self.assertTrue(attribution["academics"] > 20.0)

if __name__ == "__main__":
    unittest.main()

