from flask import Flask, render_template, request
import joblib

app = Flask(__name__)

# Load model yang sudah dilatih
model = joblib.load("model_banjir.pkl")

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        try:
            # Ambil semua input dari form sesuai fitur model
            fields = ['Tn', 'Tx', 'Tavg', 'RH_avg', 'RR', 'ss', 'ff_x', 'ddd_x', 'ff_avg', 'cat_ddd', 'category_region']
            data = [float(request.form[field]) for field in fields]

            # Prediksi banjir
            pred = model.predict([data])[0]
            result = "💧 POTENSI BANJIR TERDETEKSI!" if pred == 1 else "✅ TIDAK ADA POTENSI BANJIR."
        except Exception as e:
            result = f"Terjadi error: {e}"

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)