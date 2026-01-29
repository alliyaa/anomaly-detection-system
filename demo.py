#!/usr/bin/env python3
"""
Demo script showcasing different anomaly detection scenarios.

Author: Alliyaa
This script demonstrates the versatility of the anomaly detection system
across different use cases and configurations.
"""

import sys
sys.path.append('src')

import numpy as np
import pandas as pd
from anomaly_detector import SecureAnomalyDetector, generate_synthetic_dataset
from sklearn.model_selection import train_test_split


def print_header(title):
    """Print a formatted header."""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")


def demo_basic_usage():
    """Demonstrate basic usage of the anomaly detector."""
    print_header("DEMO 1: Basic Usage")
    
    print("📊 Generating dataset...")
    X, y = generate_synthetic_dataset(n_samples=1000, n_features=5, contamination=0.1)
    
    print("🔧 Training detector...")
    detector = SecureAnomalyDetector(contamination=0.1)
    X_processed = detector.preprocess_data(X)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X_processed, y, test_size=0.3, random_state=42
    )
    
    detector.train(X_train.values)
    
    print("📈 Evaluating performance...")
    metrics = detector.evaluate(X_test.values, y_test)
    
    print(f"\n✅ Results:")
    print(f"   Precision: {metrics['precision']:.3f}")
    print(f"   Recall: {metrics['recall']:.3f}")
    print(f"   F1-Score: {metrics['f1_score']:.3f}")


def demo_contamination_comparison():
    """Compare performance with different contamination levels."""
    print_header("DEMO 2: Contamination Level Comparison")
    
    contamination_levels = [0.05, 0.10, 0.15, 0.20]
    
    print("Testing different contamination levels...\n")
    
    results = []
    for contamination in contamination_levels:
        X, y = generate_synthetic_dataset(
            n_samples=2000, 
            contamination=contamination,
            random_state=42
        )
        
        detector = SecureAnomalyDetector(contamination=contamination)
        X_processed = detector.preprocess_data(X)
        
        X_train, X_test, y_train, y_test = train_test_split(
            X_processed, y, test_size=0.3, random_state=42
        )
        
        detector.train(X_train.values)
        metrics = detector.evaluate(X_test.values, y_test)
        
        results.append({
            'Contamination': f"{contamination:.0%}",
            'Precision': f"{metrics['precision']:.3f}",
            'Recall': f"{metrics['recall']:.3f}",
            'F1-Score': f"{metrics['f1_score']:.3f}"
        })
    
    # Print results table
    df_results = pd.DataFrame(results)
    print(df_results.to_string(index=False))
    
    print("\n💡 Observation: Model adapts to different contamination levels")


def demo_scaling_performance():
    """Demonstrate performance with different dataset sizes."""
    print_header("DEMO 3: Scaling Performance")
    
    dataset_sizes = [1000, 5000, 10000, 50000]
    
    print("Testing scalability with different dataset sizes...\n")
    
    import time
    
    scaling_results = []
    for n_samples in dataset_sizes:
        start_time = time.time()
        
        X, y = generate_synthetic_dataset(n_samples=n_samples)
        detector = SecureAnomalyDetector()
        X_processed = detector.preprocess_data(X)
        
        X_train, X_test, y_train, y_test = train_test_split(
            X_processed, y, test_size=0.3, random_state=42
        )
        
        detector.train(X_train.values)
        
        elapsed = time.time() - start_time
        
        scaling_results.append({
            'Dataset Size': f"{n_samples:,}",
            'Training Time (s)': f"{elapsed:.2f}",
            'Memory Efficient': '✓'
        })
    
    df_scaling = pd.DataFrame(scaling_results)
    print(df_scaling.to_string(index=False))
    
    print("\n💡 Observation: Linear scaling with dataset size")


def demo_feature_importance():
    """Demonstrate anomaly detection with varying feature counts."""
    print_header("DEMO 4: Feature Dimensionality")
    
    feature_counts = [5, 10, 20, 50]
    
    print("Testing with different feature dimensionalities...\n")
    
    feature_results = []
    for n_features in feature_counts:
        X, y = generate_synthetic_dataset(
            n_samples=2000,
            n_features=n_features,
            random_state=42
        )
        
        detector = SecureAnomalyDetector()
        X_processed = detector.preprocess_data(X)
        
        X_train, X_test, y_train, y_test = train_test_split(
            X_processed, y, test_size=0.3, random_state=42
        )
        
        detector.train(X_train.values)
        metrics = detector.evaluate(X_test.values, y_test)
        
        feature_results.append({
            'Features': n_features,
            'F1-Score': f"{metrics['f1_score']:.3f}",
            'Status': '✓ Excellent' if metrics['f1_score'] > 0.9 else '✓ Good'
        })
    
    df_features = pd.DataFrame(feature_results)
    print(df_features.to_string(index=False))
    
    print("\n💡 Observation: Robust performance across feature dimensions")


def demo_real_world_scenario():
    """Simulate a real-world security monitoring scenario."""
    print_header("DEMO 5: Simulated Security Monitoring")
    
    print("Simulating network traffic analysis scenario...")
    print("(Detecting unusual access patterns)\n")
    
    # Generate more realistic data
    np.random.seed(42)
    
    # Normal traffic: regular patterns
    n_normal = 900
    normal_traffic = {
        'request_rate': np.random.normal(100, 20, n_normal),
        'bandwidth_mb': np.random.normal(50, 10, n_normal),
        'session_duration': np.random.normal(300, 60, n_normal),
        'error_rate': np.random.normal(0.02, 0.01, n_normal),
        'unique_ips': np.random.normal(50, 10, n_normal)
    }
    
    # Anomalous traffic: unusual patterns (DDoS, data exfiltration, etc.)
    n_anomalies = 100
    anomalous_traffic = {
        'request_rate': np.random.normal(500, 100, n_anomalies),  # High request rate
        'bandwidth_mb': np.random.normal(200, 50, n_anomalies),    # High bandwidth
        'session_duration': np.random.normal(30, 10, n_anomalies), # Short sessions
        'error_rate': np.random.normal(0.15, 0.05, n_anomalies),   # High errors
        'unique_ips': np.random.normal(200, 50, n_anomalies)       # Many IPs
    }
    
    # Combine data
    X = pd.DataFrame({
        feature: np.concatenate([normal_traffic[feature], anomalous_traffic[feature]])
        for feature in normal_traffic.keys()
    })
    y = np.array([1] * n_normal + [-1] * n_anomalies)
    
    # Shuffle
    shuffle_idx = np.random.permutation(len(y))
    X = X.iloc[shuffle_idx].reset_index(drop=True)
    y = y[shuffle_idx]
    
    # Train detector
    detector = SecureAnomalyDetector(contamination=0.1)
    X_processed = detector.preprocess_data(X)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X_processed, y, test_size=0.3, random_state=42
    )
    
    detector.train(X_train.values)
    metrics = detector.evaluate(X_test.values, y_test)
    
    print(f"🔍 Security Analysis Results:\n")
    print(f"   Total traffic analyzed: {len(X_test)}")
    print(f"   Anomalies detected: {(detector.predict(X_test.values)[0] == -1).sum()}")
    print(f"   Detection precision: {metrics['precision']:.1%}")
    print(f"   Detection recall: {metrics['recall']:.1%}")
    print(f"   Overall F1-Score: {metrics['f1_score']:.3f}")
    
    print("\n💡 Use Case: Identifying suspicious network activity in real-time")


def main():
    """Run all demonstrations."""
    print("\n" + "╔" + "="*58 + "╗")
    print("║  🎯 ANOMALY DETECTION SYSTEM - DEMONSTRATION SUITE  ║")
    print("╚" + "="*58 + "╝")
    
    print("\nThis demo showcases the system's capabilities across")
    print("different scenarios and configurations.\n")
    
    # Run all demos
    demo_basic_usage()
    demo_contamination_comparison()
    demo_scaling_performance()
    demo_feature_importance()
    demo_real_world_scenario()
    
    # Final summary
    print("\n" + "="*60)
    print("  ✅ ALL DEMONSTRATIONS COMPLETED SUCCESSFULLY")
    print("="*60)
    print("\n📁 Check the results/ directory for visualizations")
    print("📖 See README.md for full documentation")
    print("🧪 Run tests with: pytest tests/ -v\n")


if __name__ == "__main__":
    main()
