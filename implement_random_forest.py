from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import numpy as np
from sklearn.metrics import mean_squared_error as MSE
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def implement_random_forest(X, y, SEED, target):
    # Implement ensembling with RandomForestRegressor.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=SEED)

    rf = RandomForestRegressor(n_estimators=400, min_samples_leaf=0.12, random_state=SEED)

    rf.fit(X_train, np.ravel(y_train))      # Using np.ravel() to convert from column-vector to 1d array, as prompted by
                                            # DataConversionWarning.
    y_pred = rf.predict(X_test)

    RMSE_rf_test = (MSE(y_test, y_pred) ** (1 / 2))
    print(f"RMSE_test_rf: {RMSE_rf_test}")

    # Plot feature importances.
    importances = pd.Series(data=rf.feature_importances_,
                            index=pd.Series(["GP", "G", "A", "P", "+/-", "PIM", "P/GP", "EVG", "EVP", "PPG", "PPP",
                                             "SHG", "SHP", "OTG", "GWG", "S", "S%"]))

    importances_sorted = importances.sort_values()

    importances_sorted.plot(kind='barh', color='lightgreen')
    plt.title(f'Feature Importance in Prediction of {target}')
    plt.show()

    return rf
