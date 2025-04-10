import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_venn import venn3
import seaborn as sns

# Funkcja tworząca akronim z nazwy ścieżki
def shorten(name):
    return ''.join([word[0].upper() for word in name.strip().split()])

# Wczytanie wszystkich arkuszy
file_path = "/home/shimmy/Documents/bioinf/Omics25/zajecia4-5-6/Tabela 2.xlsx"
xlsx = pd.ExcelFile(file_path)
sheet_names = xlsx.sheet_names  # oryginalne nazwy

# Mapowanie: pełna nazwa → skrót
name_map = {sheet: shorten(sheet) for sheet in sheet_names}

# Słowniki na geny
all_genes = {}
sig_genes = {}

# Wczytanie danych z każdego arkusza
for sheet in sheet_names:
    df = pd.read_excel(file_path, sheet_name=sheet)
    df.columns = df.columns.str.strip()

    # Zakładamy kolejność kolumn: Gene, p-value, Log2FC
    df.columns = ['Gene', 'p-value', 'Log2FC']

    short_name = name_map[sheet]
    all_genes[short_name] = set(df['Gene'])
    sig_genes[short_name] = set(df[df['p-value'] < 0.05]['Gene'])

    # Raport
    print(f"\nŚcieżka: {sheet} ({short_name})")
    print(f"  Wszystkie geny: {len(all_genes[short_name])}")
    print(f"  Istotne geny (p < 0.05): {len(sig_genes[short_name])}")

# Lista skróconych nazw
short_names = list(name_map.values())

# Wykresy Venn (jeśli dokładnie 3 ścieżki)
if len(short_names) == 3:
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    venn3([all_genes[name] for name in short_names], set_labels=short_names)
    plt.title("Wszystkie geny")

    plt.subplot(1, 2, 2)
    venn3([sig_genes[name] for name in short_names], set_labels=short_names)
    plt.title("Geny istotne statystycznie (p < 0.05)")

    plt.tight_layout()
    plt.savefig('aaa.png')
    plt.show()
else:
    print("\n(Wykres Venn dostępny tylko dla dokładnie 3 ścieżek)")

# Macierz podobieństw (indeks Jaccarda)
def jaccard(set1, set2):
    return len(set1 & set2) / len(set1 | set2) if (set1 | set2) else 0

similarity_matrix = pd.DataFrame(index=short_names, columns=short_names)

for s1 in short_names:
    for s2 in short_names:
        similarity_matrix.loc[s1, s2] = jaccard(sig_genes[s1], sig_genes[s2])

similarity_matrix = similarity_matrix.astype(float)

# Heatmapa podobieństw
plt.figure(figsize=(6, 5))
sns.heatmap(similarity_matrix, annot=True, cmap="YlGnBu")
plt.title("Podobieństwo między ścieżkami (geny istotne)")
plt.savefig('bbb.png')
plt.show()

# Wylistowanie nazw istotnych genów dla każdej ścieżki
print("\n--- Istotne geny (p < 0.05) dla każdej ścieżki ---")
for short_name in short_names:
    genes = sorted(sig_genes[short_name])
    print(f"\n{short_name} ({[k for k, v in name_map.items() if v == short_name][0]}):")
    print(", ".join(genes) if genes else "Brak istotnych genów")

# --- Geny wspólne między ścieżkami (istotne statystycznie) ---
from itertools import combinations

print("\n--- Wspólne geny (istotne statystycznie, p < 0.05) między ścieżkami ---")
for combo in combinations(short_names, 2):
    common_genes = sig_genes[combo[0]] & sig_genes[combo[1]]
    path1_full = [k for k, v in name_map.items() if v == combo[0]][0]
    path2_full = [k for k, v in name_map.items() if v == combo[1]][0]
    
    print(f"\n{combo[0]} vs {combo[1]} ({path1_full} vs {path2_full}):")
    print(f"Liczba wspólnych genów: {len(common_genes)}")
    print(", ".join(sorted(common_genes)) if common_genes else "Brak wspólnych istotnych genów")

