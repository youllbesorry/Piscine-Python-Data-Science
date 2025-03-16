import pandas as pd
import numpy as np
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.preprocessing import StandardScaler

def calculate_vif(data):
    data_copy = data.copy()

    X = data_copy.drop('knight', axis=1)

    scaler = StandardScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)

    vif_tolerance = pd.DataFrame()
    vif_tolerance["Variable"] = X_scaled.columns
    vif_tolerance["VIF"] = [variance_inflation_factor(X_scaled.values, i) 
                           for i in range(X_scaled.shape[1])]
    vif_tolerance["Tolérance"] = 1 / vif_tolerance["VIF"]

    vif_tolerance = vif_tolerance.sort_values('VIF', ascending=False)
    return vif_tolerance

def select_features(data):
    while True:
        vif = calculate_vif(data)
        if vif["VIF"].max() < 5:
            break
        worst_feature = vif.iloc[0]["Variable"]
        data = data.drop(worst_feature, axis=1)
    return data

def main():
    df = pd.read_csv("../Train_knight.csv")
    
    vif_initial = calculate_vif(df)
    print(vif_initial.to_string(index=False))
    
    best_features = select_features(df)

    final_vif = calculate_vif(best_features)
    print("\n\nVIF under 5 :\n", final_vif.to_string(index=False))

if __name__ == "__main__":
    main()