# Machine Learning Pipeline with Feature Engineering

# Description
Build an end-to-end ML pipeline that ingests raw data, handles
missing values, engineers features, trains multiple models, tunes
hyperparameters, and evaluates with cross-validation.

# Prerequisites:
- pandasfor data manipulation
- numpyfor numerical operations
- scikit-learn (pipelines, transformers, model selection)
- Feature engineering techniques (binning, one-hot encoding, scaling)
- Cross-validation and hyperparameter tuning ( GridSearchCV )
- Evaluation metrics (accuracy, precision, recall, F1, ROC-AUC)

# Use-Case:
- Load raw customer data (usage logs, billing, support tickets)
- Impute missing values and remove outliers
- Engineer derived features (e.g., avg_monthly_spend , days_since_last_login )
- Train and compare Logistic Regression, Random Forest, XGBoost, SVM
- Select best model based on F1 score
- Output feature importance rankings and save the trained model