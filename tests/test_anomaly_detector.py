"""
Unit tests for the Anomaly Detection System.

Run with: pytest tests/test_anomaly_detector.py -v
"""

import unittest
import numpy as np
import pandas as pd
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from anomaly_detector import SecureAnomalyDetector, generate_synthetic_dataset


class TestSecureAnomalyDetector(unittest.TestCase):
    """Test cases for SecureAnomalyDetector class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.detector = SecureAnomalyDetector(contamination=0.1, random_state=42)
        self.X, self.y = generate_synthetic_dataset(
            n_samples=1000, 
            n_features=5,
            contamination=0.1,
            random_state=42
        )
    
    def test_initialization(self):
        """Test detector initialization."""
        self.assertEqual(self.detector.contamination, 0.1)
        self.assertEqual(self.detector.random_state, 42)
        self.assertIsNone(self.detector.model)
    
    def test_validate_input_valid_data(self):
        """Test input validation with valid data."""
        try:
            self.detector.validate_input(self.X)
        except ValueError:
            self.fail("validate_input() raised ValueError unexpectedly!")
    
    def test_validate_input_empty_data(self):
        """Test input validation with empty data."""
        empty_df = pd.DataFrame()
        with self.assertRaises(ValueError):
            self.detector.validate_input(empty_df)
    
    def test_validate_input_none_data(self):
        """Test input validation with None."""
        with self.assertRaises(ValueError):
            self.detector.validate_input(None)
    
    def test_preprocess_data(self):
        """Test data preprocessing."""
        processed = self.detector.preprocess_data(self.X)
        
        # Check shape is preserved
        self.assertEqual(processed.shape, self.X.shape)
        
        # Check no missing values
        self.assertFalse(processed.isnull().any().any())
        
        # Check feature names are stored
        self.assertIsNotNone(self.detector.feature_names)
        self.assertEqual(len(self.detector.feature_names), self.X.shape[1])
    
    def test_train(self):
        """Test model training."""
        X_processed = self.detector.preprocess_data(self.X)
        self.detector.train(X_processed.values)
        
        # Check model is created
        self.assertIsNotNone(self.detector.model)
        
        # Check scaler is fitted
        self.assertTrue(hasattr(self.detector.scaler, 'mean_'))
    
    def test_predict(self):
        """Test prediction functionality."""
        X_processed = self.detector.preprocess_data(self.X)
        self.detector.train(X_processed.values[:800])
        
        predictions, scores = self.detector.predict(X_processed.values[800:])
        
        # Check output shapes
        self.assertEqual(len(predictions), 200)
        self.assertEqual(len(scores), 200)
        
        # Check predictions are binary
        self.assertTrue(set(predictions).issubset({1, -1}))
        
        # Check scores are numeric
        self.assertTrue(np.all(np.isfinite(scores)))
    
    def test_evaluate(self):
        """Test model evaluation."""
        X_processed = self.detector.preprocess_data(self.X)
        self.detector.train(X_processed.values[:800])
        
        metrics = self.detector.evaluate(
            X_processed.values[800:],
            self.y[800:]
        )
        
        # Check all metrics are present
        self.assertIn('precision', metrics)
        self.assertIn('recall', metrics)
        self.assertIn('f1_score', metrics)
        self.assertIn('confusion_matrix', metrics)
        
        # Check metrics are in valid range
        self.assertGreaterEqual(metrics['precision'], 0)
        self.assertLessEqual(metrics['precision'], 1)
        self.assertGreaterEqual(metrics['recall'], 0)
        self.assertLessEqual(metrics['recall'], 1)


class TestDataGeneration(unittest.TestCase):
    """Test cases for data generation function."""
    
    def test_generate_synthetic_dataset(self):
        """Test synthetic dataset generation."""
        X, y = generate_synthetic_dataset(
            n_samples=1000,
            n_features=5,
            contamination=0.1,
            random_state=42
        )
        
        # Check shapes
        self.assertEqual(X.shape[0], 1000)
        self.assertEqual(X.shape[1], 5)
        self.assertEqual(len(y), 1000)
        
        # Check contamination ratio
        anomaly_ratio = (y == -1).sum() / len(y)
        self.assertAlmostEqual(anomaly_ratio, 0.1, places=2)
        
        # Check data types
        self.assertIsInstance(X, pd.DataFrame)
        self.assertIsInstance(y, np.ndarray)
    
    def test_reproducibility(self):
        """Test that results are reproducible with same seed."""
        X1, y1 = generate_synthetic_dataset(n_samples=500, random_state=42)
        X2, y2 = generate_synthetic_dataset(n_samples=500, random_state=42)
        
        pd.testing.assert_frame_equal(X1, X2)
        np.testing.assert_array_equal(y1, y2)


if __name__ == '__main__':
    unittest.main()
