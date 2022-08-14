from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import numpy as np
from sklearn.metrics import mean_squared_error as MSE
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def implement_random_forest(X, y, SEED, df_X, target):
    """Use a RandomForest Regressor model to predict target variable y , based on feature matrix X.

    Takes below parameters and implements RandomForset Regression. Displays RMSE of the prediction, and generates bar
    chart of feature importance. The plot is saved to file and displayed on screen. The RF regression model is returned.
    :param X: feature matrix, numpy ndaarray object
    :param y: target, numpy ndarrray  object
    :param SEED: seed for random number generation
    :param df_X: X as DataFrame object
    :param target: target name, string
    :return: RandomForestRegressor object
    """
    # Implement ensembling with RandomForestRegressor.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=SEED)

    rf = RandomForestRegressor(n_estimators=400, min_samples_leaf=0.12, random_state=SEED)

    rf.fit(X_train, np.ravel(y_train))      # Using np.ravel() to convert from column-vector to 1d array, as prompted by
                                            # DataConversionWarning.
    y_pred = rf.predict(X_test)

    RMSE_rf_test = (MSE(y_test, y_pred) ** (1 / 2))
    print(f"RMSE_test_rf: {RMSE_rf_test}", "\n")

    # Plot feature importances.
    importances = pd.Series(data=rf.feature_importances_,
                            index=df_X.columns)

    importances_sorted = importances.sort_values()

    importances_sorted.plot(kind='barh')
    plt.title(f'Feature Importance in Prediction of {target} - Untuned Random Forest')
    plt.savefig(f"Feature Importance in Prediction of {target} - Untuned Random Forest.png")
    plt.show()

    return rf
