"""
Anomaly Detection System
A security-focused machine learning pipeline for detecting anomalous patterns in structured data.

Author: Alliyaa
Date: January 2026
"""

import logging
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Tuple, Dict, Any
from datetime import datetime

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)
import matplotlib.pyplot as plt
import seaborn as sns

# Configure logging for reproducibility and debugging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("results/pipeline.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class SecureAnomalyDetector:
    """
    A secure, modular anomaly detection pipeline using Isolation Forest.

    Features:
    - Input validation and secure data handling
    - Reproducible experiments with random seed control
    - Comprehensive evaluation metrics
    - Modular design for easy extension
    """

    def __init__(self, contamination: float = 0.1, random_state: int = 42):
        """
        Initialize the anomaly detector.

        Args:
            contamination: Expected proportion of anomalies in the dataset
            random_state: Random seed for reproducibility
        """
        self.contamination = contamination
        self.random_state = random_state
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = None

        logger.info(
            f"Initialized SecureAnomalyDetector with contamination={contamination}"
        )

    def validate_input(self, data: pd.DataFrame) -> None:
        """
        Validate input data for security and correctness.

        Args:
            data: Input DataFrame to validate

        Raises:
            ValueError: If data validation fails
        """
        if data is None or data.empty:
            raise ValueError("Input data cannot be None or empty")

        if data.isnull().any().any():
            logger.warning("Data contains missing values. These will be handled.")

        if not all(data.dtypes.apply(lambda x: np.issubdtype(x, np.number))):
            raise ValueError("All features must be numeric for this implementation")

        logger.info(
            f"Data validation passed: {data.shape[0]} rows, {data.shape[1]} columns"
        )

    def preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess data with secure handling and cleaning.

        Args:
            data: Raw input DataFrame

        Returns:
            Cleaned and preprocessed DataFrame
        """
        logger.info("Starting data preprocessing...")

        # Validate input
        self.validate_input(data)

        # Handle missing values securely
        if data.isnull().any().any():
            missing_count = data.isnull().sum().sum()
            logger.warning(f"Handling {missing_count} missing values")
            data = data.fillna(data.median())

        # Remove duplicates
        initial_rows = len(data)
        data = data.drop_duplicates()
        if len(data) < initial_rows:
            logger.info(f"Removed {initial_rows - len(data)} duplicate rows")

        # Store feature names
        self.feature_names = data.columns.tolist()

        logger.info(f"Preprocessing complete: {data.shape}")
        return data

    def train(self, X_train: np.ndarray) -> None:
        """
        Train the Isolation Forest anomaly detection model.

        Args:
            X_train: Training features
        """
        logger.info("Training Isolation Forest model...")

        # Scale features for better performance
        X_train_scaled = self.scaler.fit_transform(X_train)

        # Initialize and train model
        self.model = IsolationForest(
            contamination=self.contamination,
            random_state=self.random_state,
            n_estimators=100,
            max_samples="auto",
            n_jobs=-1,  # Use all CPU cores
        )

        self.model.fit(X_train_scaled)
        logger.info("Model training complete")

    def predict(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Predict anomalies and anomaly scores.

        Args:
            X: Features to predict on

        Returns:
            Tuple of (predictions, anomaly_scores)
            predictions: 1 for normal, -1 for anomaly
            anomaly_scores: Higher scores indicate more anomalous
        """
        if self.model is None:
            raise RuntimeError("Model must be trained before prediction")

        X_scaled = self.scaler.transform(X)
        predictions = self.model.predict(X_scaled)
        anomaly_scores = -self.model.score_samples(X_scaled)  # Higher = more anomalous

        return predictions, anomaly_scores

    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, Any]:
        """
        Comprehensive model evaluation with multiple metrics.

        Args:
            X_test: Test features
            y_test: True labels (1 for normal, -1 for anomaly)

        Returns:
            Dictionary containing evaluation metrics
        """
        logger.info("Evaluating model performance...")

        # Get predictions
        predictions, anomaly_scores = self.predict(X_test)

        # Convert labels to binary (0 for normal, 1 for anomaly) for sklearn metrics
        y_test_binary = (y_test == -1).astype(int)
        predictions_binary = (predictions == -1).astype(int)

        # Calculate metrics
        metrics = {
            "precision": precision_score(y_test_binary, predictions_binary),
            "recall": recall_score(y_test_binary, predictions_binary),
            "f1_score": f1_score(y_test_binary, predictions_binary),
            "confusion_matrix": confusion_matrix(y_test_binary, predictions_binary),
            "anomaly_scores": anomaly_scores,
            "predictions": predictions,
        }

        # Log results
        logger.info(f"Precision: {metrics['precision']:.4f}")
        logger.info(f"Recall: {metrics['recall']:.4f}")
        logger.info(f"F1-Score: {metrics['f1_score']:.4f}")
        logger.info(
            f"\nClassification Report:\n{classification_report(y_test_binary, predictions_binary)}"
        )

        return metrics

    def visualize_results(
        self, metrics: Dict[str, Any], save_path: str = "results"
    ) -> None:
        """
        Generate comprehensive visualizations of model performance.

        Args:
            metrics: Dictionary of evaluation metrics
            save_path: Directory to save visualizations
        """
        logger.info("Generating visualizations...")

        # Create results directory if it doesn't exist
        Path(save_path).mkdir(parents=True, exist_ok=True)

        # Set style
        sns.set_style("whitegrid")

        # 1. Confusion Matrix
        plt.figure(figsize=(8, 6))
        sns.heatmap(
            metrics["confusion_matrix"],
            annot=True,
            fmt="d",
            cmap="Blues",
            xticklabels=["Normal", "Anomaly"],
            yticklabels=["Normal", "Anomaly"],
        )
        plt.title("Confusion Matrix", fontsize=14, fontweight="bold")
        plt.ylabel("True Label")
        plt.xlabel("Predicted Label")
        plt.tight_layout()
        plt.savefig(f"{save_path}/confusion_matrix.png", dpi=300)
        plt.close()

        # 2. Anomaly Score Distribution
        plt.figure(figsize=(10, 6))
        plt.hist(metrics["anomaly_scores"], bins=50, edgecolor="black", alpha=0.7)
        plt.axvline(
            metrics["anomaly_scores"].mean(),
            color="red",
            linestyle="--",
            label=f'Mean: {metrics["anomaly_scores"].mean():.3f}',
        )
        plt.title("Anomaly Score Distribution", fontsize=14, fontweight="bold")
        plt.xlabel("Anomaly Score (higher = more anomalous)")
        plt.ylabel("Frequency")
        plt.legend()
        plt.tight_layout()
        plt.savefig(f"{save_path}/anomaly_score_distribution.png", dpi=300)
        plt.close()

        # 3. Metrics Bar Chart
        fig, ax = plt.subplots(figsize=(8, 6))
        metric_names = ["Precision", "Recall", "F1-Score"]
        metric_values = [
            metrics["precision"],
            metrics["recall"],
            metrics["f1_score"],
        ]
        colors = ["#3498db", "#2ecc71", "#e74c3c"]

        bars = ax.bar(metric_names, metric_values, color=colors, edgecolor="black", alpha=0.8)
        ax.set_ylim([0, 1])
        ax.set_ylabel("Score", fontweight="bold")
        ax.set_title("Model Performance Metrics", fontsize=14, fontweight="bold")

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height,
                f"{height:.3f}",
                ha="center",
                va="bottom",
                fontweight="bold",
            )

        plt.tight_layout()
        plt.savefig(f"{save_path}/metrics_comparison.png", dpi=300)
        plt.close()

        logger.info(f"Visualizations saved to {save_path}/")


def generate_synthetic_dataset(
    n_samples: int = 10000,
    n_features: int = 10,
    contamination: float = 0.1,
    random_state: int = 42,
) -> Tuple[pd.DataFrame, np.ndarray]:
    """
    Generate a synthetic dataset for demonstration purposes.

    Simulates network traffic or transaction data with anomalies.

    Args:
        n_samples: Number of samples to generate
        n_features: Number of features
        contamination: Proportion of anomalies
        random_state: Random seed for reproducibility

    Returns:
        Tuple of (features_df, labels)
    """
    logger.info(
        f"Generating synthetic dataset: {n_samples} samples, {n_features} features"
    )

    np.random.seed(random_state)

    # Generate normal data
    n_normal = int(n_samples * (1 - contamination))
    n_anomalies = n_samples - n_normal

    # Normal samples: clustered around 0 with low variance
    normal_data = np.random.randn(n_normal, n_features) * 0.5

    # Anomalies: scattered with high variance or in different regions
    anomaly_data = np.random.randn(n_anomalies, n_features) * 3 + 5

    # Combine data
    X = np.vstack([normal_data, anomaly_data])
    y = np.array([1] * n_normal + [-1] * n_anomalies)

    # Shuffle
    shuffle_idx = np.random.permutation(n_samples)
    X = X[shuffle_idx]
    y = y[shuffle_idx]

    # Create DataFrame with meaningful feature names
    feature_names = [f"feature_{i+1}" for i in range(n_features)]
    df = pd.DataFrame(X, columns=feature_names)

    logger.info(f"Dataset generated: {n_normal} normal, {n_anomalies} anomalies")

    return df, y


def main():
    """
    Main execution pipeline demonstrating the complete anomaly detection workflow.
    """
    logger.info("=" * 50)
    logger.info("Starting Anomaly Detection Pipeline")
    logger.info("=" * 50)

    # Configuration
    RANDOM_STATE = 42
    CONTAMINATION = 0.1
    TEST_SIZE = 0.3

    try:
        # 1. Data Generation (in production, this would be data loading)
        logger.info("\n[STEP 1] Data Generation")
        X, y = generate_synthetic_dataset(
            n_samples=10000,
            n_features=10,
            contamination=CONTAMINATION,
            random_state=RANDOM_STATE,
        )

        # 2. Initialize detector
        logger.info("\n[STEP 2] Model Initialization")
        detector = SecureAnomalyDetector(
            contamination=CONTAMINATION, random_state=RANDOM_STATE
        )

        # 3. Preprocess data
        logger.info("\n[STEP 3] Data Preprocessing")
        X_processed = detector.preprocess_data(X)

        # 4. Train/test split
        logger.info("\n[STEP 4] Train/Test Split")
        X_train, X_test, y_train, y_test = train_test_split(
            X_processed,
            y,
            test_size=TEST_SIZE,
            random_state=RANDOM_STATE,
            stratify=y,
        )
        logger.info(f"Training set: {X_train.shape[0]} samples")
        logger.info(f"Test set: {X_test.shape[0]} samples")

        # 5. Train model
        logger.info("\n[STEP 5] Model Training")
        detector.train(X_train.values)

        # 6. Evaluate model
        logger.info("\n[STEP 6] Model Evaluation")
        metrics = detector.evaluate(X_test.values, y_test)

        # 7. Generate visualizations
        logger.info("\n[STEP 7] Visualization Generation")
        detector.visualize_results(metrics)

        # 8. Summary
        logger.info("\n" + "=" * 50)
        logger.info("PIPELINE EXECUTION COMPLETE")
        logger.info("=" * 50)
        logger.info(f"Final Metrics:")
        logger.info(f"  Precision: {metrics['precision']:.4f}")
        logger.info(f"  Recall: {metrics['recall']:.4f}")
        logger.info(f"  F1-Score: {metrics['f1_score']:.4f}")
        logger.info(f"\nResults saved to: results/")
        logger.info("=" * 50)

        return metrics

    except Exception as e:
        logger.error(f"Pipeline execution failed: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    main()# Black formatted
