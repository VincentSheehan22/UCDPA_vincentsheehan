from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error as MSE


def implement_decision_tree(X, y, SEED):
    # Define test and training data for DecisionTreeRegressor.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=SEED)

    # Instantiate machine learning model - DecisionTreeRegressor.
    dt = DecisionTreeRegressor(max_depth=4, min_samples_leaf=0.14, random_state=SEED)

    # Perform k-fold cross-validation to determine bias and variance.
    MSE_CV = - cross_val_score(dt, X_train, y_train, cv=10,
                               scoring="neg_mean_squared_error",
                               n_jobs=-1)

    # Fit model to training data
    dt.fit(X_train, y_train)

    # Predict the labels of the test and training sets.
    y_pred_train = dt.predict(X_train)
    y_pred_test = dt.predict(X_test)

    print(f"CV MSE: {MSE_CV.mean()}")
    print(f"Train MSE: {MSE(y_train, y_pred_train)}")
    print(f"Test MSE: {MSE(y_test, y_pred_test)}")

    RMSE_CV = (MSE_CV.mean()) ** (1 / 2)
    print(f"RMSE_CV: {RMSE_CV}")

    RMSE_train = (MSE(y_train, y_pred_train) ** (1 / 2))
    print(f"RMSE_train: {RMSE_train}")

    RMSE_test = (MSE(y_test, y_pred_test) ** (1 / 2))
    print(f"RMSE_test: {RMSE_test}\n")
