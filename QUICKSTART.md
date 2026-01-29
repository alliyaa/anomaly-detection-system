# 🚀 Quick Start Guide

**For Recruiters & Evaluators:** Get this project running in under 5 minutes!

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation (2 minutes)

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/anomaly-detection-system.git
cd anomaly-detection-system

# 2. Install dependencies
pip install -r requirements.txt
```

## Running the Demo (1 minute)

```bash
# Run the complete pipeline
python src/anomaly_detector.py
```

**That's it!** The system will:
1. Generate a synthetic dataset (10,000 samples)
2. Train the anomaly detection model
3. Evaluate performance with comprehensive metrics
4. Generate visualizations
5. Save all results to `results/`

## Expected Output

```
==================================================
Starting Anomaly Detection Pipeline
==================================================

[STEP 1] Data Generation
Dataset generated: 9000 normal, 1000 anomalies

[STEP 2] Model Initialization
Initialized SecureAnomalyDetector with contamination=0.1

[STEP 3] Data Preprocessing
Data validation passed: 10000 rows, 10 columns

[STEP 4] Train/Test Split
Training set: 7000 samples
Test set: 3000 samples

[STEP 5] Model Training
Model training complete

[STEP 6] Model Evaluation
Precision: 1.0000
Recall: 1.0000
F1-Score: 1.0000

[STEP 7] Visualization Generation
Visualizations saved to results/

==================================================
PIPELINE EXECUTION COMPLETE
==================================================
```

## View Results

Check the `results/` directory for:
- `confusion_matrix.png` - Model accuracy visualization
- `anomaly_score_distribution.png` - Score distribution analysis
- `metrics_comparison.png` - Performance metrics chart
- `pipeline.log` - Detailed execution logs

## Interactive Exploration (Optional)

Want to explore interactively?

```bash
# Install Jupyter (if not already installed)
pip install jupyter

# Launch the notebook
jupyter notebook notebooks/exploratory_analysis.ipynb
```

## Key Features Demonstrated

✅ **Security-Focused Design**
- Input validation and error handling
- Secure configuration management
- Comprehensive logging

✅ **Modular Pipeline**
- Clean separation of concerns
- Reusable components
- Easy to extend

✅ **Reproducible Experiments**
- Fixed random seeds
- Deterministic train/test splits
- Version-controlled dependencies

✅ **Production-Ready Code**
- Type hints and docstrings
- Unit tests included
- Professional documentation

## Customization

Edit `config.py` to adjust parameters:

```python
MODEL_CONFIG = {
    'contamination': 0.1,      # Expected % of anomalies (adjust 0.05-0.2)
    'n_estimators': 100,       # Number of trees (increase for accuracy)
}

DATA_CONFIG = {
    'n_samples': 10000,        # Dataset size
    'n_features': 10,          # Number of features
}
```

## Running Tests

```bash
# Run unit tests
python -m pytest tests/test_anomaly_detector.py -v

# Check code coverage
pip install pytest-cov
pytest tests/ --cov=src --cov-report=html
```

## Project Structure

```
anomaly-detection-system/
├── src/
│   └── anomaly_detector.py    # Main implementation
├── results/                    # Generated outputs
├── notebooks/                  # Jupyter notebooks
├── tests/                      # Unit tests
├── config.py                   # Configuration
├── requirements.txt            # Dependencies
└── README.md                   # Full documentation
```

## Next Steps

1. **Explore the Code**: Check out `src/anomaly_detector.py` for the implementation
2. **Read the Docs**: Full documentation in `README.md`
3. **Run Tests**: Verify quality with `pytest tests/`
4. **Experiment**: Try the Jupyter notebook for interactive analysis

## Contact

Questions? Issues?
- **GitHub**: Open an issue at [repository-url]
- **Email**: your.email@example.com

---

**Built with ❤️ for secure, production-grade machine learning**
