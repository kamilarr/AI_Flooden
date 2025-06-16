import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.metrics import accuracy_score, confusion_matrix
import joblib
import graphviz
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Baca dataset CSV (ubah koma ke titik dan abaikan baris kosong)
df = pd.read_csv("app/Data/dataset_flooden.csv", delimiter=';', decimal=',')

# 2. Buang baris yang mengandung missing values (NA)
df = df.dropna()

# 3. Definisikan semua fitur dan fitur penting
all_features = ["Tn", "Tx", "Tavg", "RH_avg", "RR", "ss", "ff_x", "ddd_x", "ff_avg", "cat_ddd", "category_region"]
important_features = ["RR", "RH_avg", "Tavg"]
target = "flood"

# 4. Korelasi (untuk eksplorasi)
plt.figure(figsize=(12, 8))
sns.heatmap(df[all_features + [target]].corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Matrix")
plt.tight_layout()
plt.show()

# ===============================
# 5A. Model dengan semua fitur
# ===============================
X_all = df[all_features]
y_all = df[target]
X_train_all, X_test_all, y_train_all, y_test_all = train_test_split(X_all, y_all, test_size=0.2, random_state=42)

model_all = DecisionTreeClassifier(random_state=42, max_depth=6, min_samples_split=3, class_weight='balanced')
model_all.fit(X_train_all, y_train_all)

y_pred_all = model_all.predict(X_test_all)
acc_all = accuracy_score(y_test_all, y_pred_all)

# Simpan model semua fitur
joblib.dump(model_all, "flooden_model_all.pkl")

# ===============================
# 5B. Model dengan 3 fitur penting
# ===============================
X_imp = df[important_features]
y_imp = df[target]
X_train_imp, X_test_imp, y_train_imp, y_test_imp = train_test_split(X_imp, y_imp, test_size=0.2, random_state=42)

model_imp = DecisionTreeClassifier(random_state=42, max_depth=6, min_samples_split=3, class_weight='balanced')
model_imp.fit(X_train_imp, y_train_imp)

y_pred_imp = model_imp.predict(X_test_imp)
acc_imp = accuracy_score(y_test_imp, y_pred_imp)


# Simpan model 3 fitur
joblib.dump(model_imp, "flooden_model_important.pkl")

# ===============================
# 6. Visualisasi tree model penting
# ===============================
dot_data = export_graphviz(model_imp, out_file=None,
                           feature_names=important_features,
                           class_names=["Aman", "Banjir"],
                           filled=True, rounded=True,
                           special_characters=True)

graph = graphviz.Source(dot_data)
graph.render("flooden_tree_important")
graph.view()

dot_data = export_graphviz(model_all, out_file=None,
                           feature_names=all_features,
                           class_names=["Aman", "Banjir"],
                           filled=True, rounded=True,
                           special_characters=True)

graph = graphviz.Source(dot_data)
graph.render("flooden_tree")
graph.view()

from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score

# Evaluasi untuk model dengan semua fitur
print("\n======== Evaluasi Model dengan Semua Fitur ========")
print("|| Akurasi model:", accuracy_score(y_test_all, y_pred_all))
print("|| Confusion Matrix (semua fitur):\n", confusion_matrix(y_test_all, y_pred_all))
print("|| Precision :", precision_score(y_test_all, y_pred_all))
print("|| Recall    :", recall_score(y_test_all, y_pred_all))
print("|| F1-score  :", f1_score(y_test_all, y_pred_all))
print("|| ROC AUC   :", roc_auc_score(y_test_all, model_all.predict_proba(X_test_all)[:, 1]))
print("===================================================")

# Evaluasi untuk model dengan 3 fitur penting
print("\n====== Evaluasi Model dengan 3 Fitur Penting ======")
print("|| Akurasi model:", accuracy_score(y_test_imp, y_pred_imp))
print("|| Confusion Matrix (3 fitur):\n", confusion_matrix(y_test_imp, y_pred_imp))
print("|| Precision :", precision_score(y_test_imp, y_pred_imp))
print("|| Recall    :", recall_score(y_test_imp, y_pred_imp))
print("|| F1-score  :", f1_score(y_test_imp, y_pred_imp))
print("|| ROC AUC   :", roc_auc_score(y_test_imp, model_imp.predict_proba(X_test_imp)[:, 1]))
print("===================================================")

