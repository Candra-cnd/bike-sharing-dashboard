# Bike Sharing Data Analysis Dashboard

## Setup Environment - Anaconda
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt

## Setup Environment - Standar Pythin (venv)
python -m venv env
source env/bin/activate     # Untuk Mac/Linux
env\Scripts\activate        # Untuk Windows
pip install -r requirements.txt

## Setup Environment - Shell/Terminal (Direct Install)
pip install -r requirements.txt

## Run Streamlit App
streamlit run dashboard/dashboard.py

---
### Atribusi Dataset (Portofolio)
Proyek ini adalah *submission* akhir untuk kelas **Belajar Fundamental Analisis Data** di Dicoding. Proyek ini menganalisis dataset penyewaan sepeda **Bike Sharing Dataset** untuk memahami pola permintaan berdasarkan waktu, hari kerja, dan kondisi cuaca. Hasil analisis disajikan dalam bentuk *dashboard* interaktif menggunakan Streamlit. Dataset yang digunakan dari [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/bike+sharing+dataset), dikembangkan oleh Hadi Fanee-T. Digunakan untuk keperluan pembelajaran dan portofolio.
