from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.metrics import mean_squared_error as MSE
import pandas as pd
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt
import seaborn as sns

def tune_random_forest(rf, X, y, SEED, df_X, target):
    """Perform hyperparameter tuning on a RnadomForestRegreesor model.

    Takes below parameters as input. Tunes hyperparameters of model per GridSearchCV. Prints best parameters, and best
    model. Predicts with the best model, and prints RMSE of prediction. Bar chart of feature importances is saved to
    file and displayed on screen. Returns best model as determined by hyperparameter tuning with GridSearchCV.
    :param rf: RandomForest Regressor model
    :param X: feature matrix, numpy ndarray
    :param y: target, numpy ndarray
    :param SEED: seed for random number generation
    :param df_X: X as pandas DataFrame object
    :param target: taget name, string
    :return: best RF Regressor model determined by hyperparameter tuning
    """
    # Hyperparameter tuning
    print("Getting RandomForestRegressor hyperparamters...\n", rf.get_params(), "\n")

    print("Tuning hyperparameters with GridSearchCV...\n")
    params_rf = {'n_estimators': [300, 400, 500],
                 'max_depth': [4, 6, 8],
                 'min_samples_leaf': [0.1, 0.2],
                 'max_features': ['log2', 'sqrt']}

    grid_rf = GridSearchCV(estimator=rf,
                           param_grid=params_rf,
                           cv=3,
                           scoring='neg_mean_squared_error',
                           verbose=1,
                           n_jobs=-1)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=SEED)

    grid_rf.fit(X_train, np.ravel(y_train))

    best_hyperparams = grid_rf.best_params_
    print('Getting best hyperparameters...\n', best_hyperparams, "\n")

    # Extract the best model from 'grid_rf'
    best_model = grid_rf.best_estimator_
    print('Getting best model...\n', best_model, "\n")

    # Predict the test set labels.
    print("Predicting test set labels with best model...\n")
    y_pred = best_model.predict(X_test)

    # Evaluate the test set RMSE
    rmse_test_rf_tuned = MSE(y_test, y_pred)**(1/2)

    # Print the test set RMSE
    print(f'RMSE_test_rf_tuned: {rmse_test_rf_tuned}', "\n")

    # Plot feature importances.
    importances = pd.Series(data=best_model.feature_importances_,
                            index=df_X.columns)

    importances_sorted = importances.sort_values()

    importances_sorted.plot(kind='barh')
    plt.title(f"Feature Importance in Prediction of {target} - Tuned Random Forest")
    plt.savefig(f"Feature Importance in Prediction of {target} - Tuned Random Forest")
    plt.show()

    return best_model
