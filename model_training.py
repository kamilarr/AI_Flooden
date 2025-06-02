import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib

# 1. Baca file Excel
df = pd.read_excel("dataset_fix.xlsx")  # Ganti dengan nama file Excel kamu

# 2. Pilih fitur (X) dan target (y)
X = df[['Tn', 'Tx', 'Tavg', 'RH_avg', 'RR', 'ss', 'ff_x', 'ddd_x', 'ff_avg', 'cat_ddd', 'category_region']]
y = df['flood']  # Label 1 jika banjir, 0 jika tidak

# 3. Bersihkan data kosong
df.dropna(inplace=True)

# 4. Latih model decision tree
model = DecisionTreeClassifier()
model.fit(X, y)

# 5. Simpan model
joblib.dump(model, 'model_banjir.pkl')
print("Model berhasil disimpan!")
