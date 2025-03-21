from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
import pandas as pd
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, plot_tree
import sys


def transform_data(data):
    data_transformed = data.copy()

    if 'knight' in data_transformed.columns:
        data_transformed['knight'] = data_transformed['knight'].apply(
            lambda x: 1 if x == 'Jedi' else 0)

        X = data_transformed.drop('knight', axis=1)
        y = data_transformed['knight']

        scaler = StandardScaler()
        X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)

        result = X_scaled.copy()
        result['knight'] = y

        X = result.iloc[:, :-1].values
        Y = result.iloc[:, -1].values

        return result, X, Y
    else:
        scaler = StandardScaler()
        X_scaled = pd.DataFrame(scaler.fit_transform(data_transformed), 
                               columns=data_transformed.columns)

        X = X_scaled.values
        return X_scaled, X, None

def Tree(train_data):
    data_transformed, X, y = transform_data(train_data)

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42)

    model = DecisionTreeClassifier(random_state=1)
    model.fit(X_train, y_train)

    y_pred_val = model.predict(X_val)
    f1 = f1_score(y_val, y_pred_val)
    print(f'Validation F1 Score: {(f1 * 100):.2f}%')

    Visualize(data_transformed, model)

    return model

def predict_test_data(model, test_data):
    _, X_test, _ = transform_data(test_data)

    y_pred = model.predict(X_test)

    predictions = ['Jedi' if pred == 1 else 'Sith' for pred in y_pred]

    with open('predictions.txt', 'w') as f:
        for prediction in predictions:
            f.write(f"{prediction}\n")

    return predictions

def Visualize(data, model):
    plt.figure(figsize=(15, 10))
    plot_tree(model, filled=True, feature_names=data.columns[:-1].tolist(),
            class_names=[str(c) for c in model.classes_], rounded=True)
    plt.show()

def main():
    if (len(sys.argv) != 3):
        print("Usage: python Tree.py <train_file.csv> <test_file.csv>")
        return

    train_data = pd.read_csv(sys.argv[1])

    model = Tree(train_data)

    test_data = pd.read_csv(sys.argv[2])

    predict_test_data(model, test_data)

if __name__ == "__main__":
    main()