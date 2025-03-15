import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def heatmap(data_path):
    try:
        df = pd.read_csv(data_path)
        
        if 'knight' in df.columns:
            df['knight'] = df['knight'].apply(lambda x: 0 if x == 'Jedi' else 1)
        
        corr_matrix = df.corr()
        
        plt.figure(figsize=(10, 8))
        
        sns.heatmap(corr_matrix, annot=False)
        
        plt.title('Correlation Coefficient Heatmap')
        plt.tight_layout()
        plt.show()
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    heatmap("../Train_knight.csv")
