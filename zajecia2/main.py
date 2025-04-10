'''
    oszacować jakość - prosta analiza PCA po skalowaniu, żeby znaleźć outliery

    Jak się zachowuje blank - PCA, jaka jest odpowiedź sprzętu dla blank w stosunku do średniej dla tkanek

    Jak zachowują sie próbki Quality Control (QC) (Czy są w jednym miejscu)

    Wizualizacja, aby wskazać jakość lub jej brak

    Zastanowić się co usunąć a co nie żeby poprawić jakość
'''

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def pca_analysis(data, labels):
    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(data)
    pca_df = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])
    pca_df['label'] = labels  # Dodanie etykiet
    return pca_df

def scale_data(data):
    scaler = StandardScaler()
    return scaler.fit_transform(data)

def load_data(path, sheet_name):
    return pd.read_excel(path, sheet_name=sheet_name)

def Quality1(path: str):
    # Load data
    data = load_data(path, sheet_name='Arkusz1')
    labels = data['Group']  # Pobranie etykiet z kolumny 'Group'
    data = data.iloc[:, 2:]  # Usunięcie dwóch pierwszych kolumn

    # Scale data
    data = scale_data(data)

    # Check if data is scaled properly
    if not np.isclose(data.mean(), 0, atol=1e-6) or not np.isclose(data.std(), 1, atol=1e-6):
        exit('Data is not scaled properly')
    else:
        print('Data is scaled properly')

    pca_df = pca_analysis(data, labels)

    # Podział na kategorie
    categories = {
        'Male': pca_df[labels.str.startswith('M')],
        'Female': pca_df[labels.str.startswith('F')],
        'Blank': pca_df[labels == 'Blank'],
        'QC': pca_df[labels == 'QC']
    }

    # Wizualizacja wyników PCA
    plt.figure(figsize=(8, 8))
    colors = {'Male': 'blue', 'Female': 'red', 'Blank': 'green', 'QC': 'purple'}
    markers = {'Male': '.', 'Female': '.', 'Blank': 's', 'QC': '^'}  # Kwadrat dla Blank, trójkąt dla QC
    
    for label, subset in categories.items():
        plt.scatter(subset['PC1'], subset['PC2'], label=label, alpha=0.6, color=colors[label], marker=markers[label])
    
    plt.axhline(y = 0, color='grey', linestyle='--', alpha=0.6)
    plt.axvline(x = 0, color='grey', linestyle='--', alpha=0.6)
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.title("PCA of Metabolomics Data")
    plt.legend()
    plt.savefig('/home/shimmy/Documents/bioinf/Omics25/zajecia2/q1.png')
    plt.show()

def Quality2(path: str):
    # Load data
    data = load_data(path, sheet_name='Arkusz2')
    labels = data['Group']  # Pobranie etykiet z kolumny 'Group'
    data = data.iloc[:, 2:]  # Usunięcie dwóch pierwszych kolumn

    # Scale data
    data = scale_data(data)

    # Check if data is scaled properly
    if not np.isclose(data.mean(), 0, atol=1e-6) or not np.isclose(data.std(), 1, atol=1e-6):
        exit('Data is not scaled properly')
    else:
        print('Data is scaled properly')

    pca_df = pca_analysis(data, labels)

    # Podział na kategorie
    categories = {
        'Male': pca_df[labels.str.startswith('M')],
        'Female': pca_df[labels.str.startswith('F')],
        'Blank': pca_df[labels == 'Blank'],
        'QC': pca_df[labels == 'QC']
    }

    # Wizualizacja wyników PCA
    plt.figure(figsize=(8, 8))
    colors = {'Male': 'blue', 'Female': 'red', 'Blank': 'green', 'QC': 'purple'}
    markers = {'Male': '.', 'Female': '.', 'Blank': 's', 'QC': '^'}  # Kwadrat dla Blank, trójkąt dla QC
    
    for label, subset in categories.items():
        plt.scatter(subset['PC1'], subset['PC2'], label=label, alpha=0.6, color=colors[label], marker=markers[label])
    
    plt.axhline(y = 0, color='grey', linestyle='--', alpha=0.6)
    plt.axvline(x = 0, color='grey', linestyle='--', alpha=0.6)
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.title("PCA of Metabolomics Data - Quality2")
    plt.legend()
    plt.savefig('/home/shimmy/Documents/bioinf/Omics25/zajecia2/q2.png')
    plt.show()

if __name__=="__main__":
    Q1_PATH = '/home/shimmy/Documents/bioinf/Omics25/zajecia2/Metabolomika_Quality1.xlsx'
    Q2_PATH = '/home/shimmy/Documents/bioinf/Omics25/zajecia2/Metabolomika_Quality2.xlsx'

    Quality1(path=Q1_PATH)
    Quality2(path=Q2_PATH)
