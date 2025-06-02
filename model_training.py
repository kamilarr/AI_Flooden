import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.metrics import accuracy_score, confusion_matrix
import joblib
import graphviz

# 1. Baca dataset
df = pd.read_excel("dataset_fix.xlsx") 

# 2. Pilih fitur dan target
features = ["Tn", "Tx", "Tavg", "RH_avg", "RR", "ss", "ff_x", "ddd_x", "ff_avg", "cat_ddd", "category_region"]
target = "flood"

X = df[features]
y = df[target]

# 3. Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Latih model
model = DecisionTreeClassifier(
    random_state=42,
    max_depth=6,
    min_samples_split=3,
    class_weight='balanced'
)
model.fit(X_train, y_train)

# 5. Evaluasi
y_pred = model.predict(X_test)
print("Akurasi:", accuracy_score(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# 6. Simpan model
joblib.dump(model, "flooden_model.pkl")
print("Model saved as flooden_model.pkl")

# 7. Visualisasi dengan Graphviz
dot_data = export_graphviz(model, out_file=None, 
                           feature_names=features,
                           class_names=["Aman", "Banjir"],  
                           filled=True, rounded=True,
                           special_characters=True)

graph = graphviz.Source(dot_data)
graph.render("flooden_tree")  
graph.view()  # Opens the rendered tree in the default viewer
