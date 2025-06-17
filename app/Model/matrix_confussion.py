import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

# Data label berdasarkan penjelasanmu
y_true = (
    ['TIDAK BANJIR'] * (469 + 98) +  # TN + FP
    ['BANJIR'] * (14 + 47)            # FN + TP
)

y_pred = (
    ['TIDAK BANJIR'] * 469 +   # TN
    ['BANJIR'] * 98 +         # FP
    ['TIDAK BANJIR'] * 14 +    # FN
    ['BANJIR'] * 47            # TP
)

# Label kelas
labels = ['TIDAK BANJIR', 'BANJIR']

# Buat confusion matrix
cm = confusion_matrix(y_true, y_pred, labels=labels)

# Visualisasi confusion matrix
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)

plt.xlabel('Predicted label')
plt.ylabel('True label')
plt.title('Confusion Matrix Prediksi Banjir')
plt.show()