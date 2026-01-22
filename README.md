# 🧠 Prediksi Risiko Stres Mahasiswa

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.2%2B-orange)
![License](https://img.shields.io/badge/License-MIT-green)

Sistem prediksi risiko stres mahasiswa menggunakan algoritma **Random Forest** dengan antarmuka web interaktif berbasis **Streamlit**. Aplikasi ini membantu mengidentifikasi risiko stres pada mahasiswa S1 berdasarkan berbagai faktor demografi, akademik, dan gaya hidup.

---

## 📋 Deskripsi Proyek

Aplikasi ini dirancang untuk membantu **mahasiswa S1 (maksimal 25 tahun)** dalam mengidentifikasi risiko stres secara dini melalui prediksi berbasis machine learning. Dengan memasukkan data seperti pola tidur, jam belajar, IPK, dan faktor lainnya, sistem akan memberikan prediksi apakah mahasiswa termasuk kategori **Sehat** atau **Risiko Stres**, dilengkapi dengan rekomendasi personal untuk meningkatkan kesehatan mental.

### 🎯 Tujuan
- Deteksi dini risiko stres mahasiswa
- Memberikan rekomendasi kesehatan berbasis data
- Membantu mahasiswa memahami faktor-faktor yang mempengaruhi kesehatan mental

### ⚠️ Disclaimer
> **PENTING**: Hasil prediksi aplikasi ini **BUKAN diagnosis medis**. Untuk masalah kesehatan mental yang serius, konsultasikan dengan profesional kesehatan atau konselor.

---

## ✨ Fitur Utama

| Fitur | Deskripsi |
|-------|-----------|
| 🏠 **Dashboard Beranda** | Ringkasan dataset dengan visualisasi distribusi label dan gender |
| 🔮 **Prediksi Batch** | Prediksi hingga **5 data sekaligus** dengan form yang mudah digunakan |
| 📊 **Visualisasi Interaktif** | Grafik dinamis menggunakan Plotly untuk analisis data |
| 📈 **Analisis Performa Model** | Confusion matrix, accuracy, F1-score, dan feature importance |
| 💡 **Rekomendasi Personal** | Saran kesehatan yang disesuaikan dengan profil dan hasil prediksi |
| 📥 **Export Hasil** | Download kartu hasil prediksi dalam format PNG |
| 🔄 **Reset Form** | Tombol reset untuk membersihkan form input dengan cepat |

---

## 📊 Dataset & Model

### Dataset
- **Total Records**: 3,000 data mahasiswa
- **Fitur**: 11 kolom (5 numerik, 5 kategorikal, 1 target)
- **Target**: 
  - `Sehat`: 1,803 data (60.1%)
  - `Risiko Stres`: 1,197 data (39.9%)

### Fitur Input

#### Fitur Numerik
- **Umur** (18-25 tahun)
- **Jam Belajar per Hari** (1-7 jam)
- **Jam Tidur per Hari** (3-9 jam)
- **IPK** (0.0-4.0)
- **Jumlah Tugas Besar per Minggu** (0-5 tugas)

#### Fitur Kategorikal
- **Gender**: Laki-laki, Perempuan
- **Jurusan/Program Studi**: 7 jurusan (Teknik Informatika, Hukum, Kedokteran, dll.)
- **Frekuensi Olahraga**: Jarang, Kadang, Sering
- **Pemasukan Keluarga**: Rendah, Sedang, Tinggi
- **Status Hubungan**: Jomblo, Dalam hubungan

### Model Machine Learning

- **Algoritma**: Random Forest Classifier
- **Hyperparameters**:
  - `n_estimators`: 200
  - `max_depth`: 4
  - `random_state`: 42
- **Preprocessing**:
  - Normalisasi fitur numerik (Z-score normalization)
  - One-Hot Encoding untuk fitur kategorikal
  - Pembersihan data IPK (handling format comma/dot)

---

## 🛠️ Tech Stack

| Kategori | Teknologi |
|----------|-----------|
| **Bahasa** | Python 3.8+ |
| **UI Framework** | Streamlit 1.28+ |
| **Machine Learning** | Scikit-learn 1.2+ |
| **Data Processing** | Pandas, NumPy |
| **Visualisasi** | Plotly 5.15+ |
| **Image Processing** | Pillow 10.0+ |

---

## 📁 Struktur Proyek

```
resiko-stress-random-forest/
│
├── app/                          # Aplikasi Streamlit
│   ├── app.py                    # Main application file
│   ├── pages/                    # Halaman-halaman aplikasi
│   │   ├── home.py              # Dashboard beranda
│   │   ├── prediction.py        # Halaman prediksi
│   │   ├── analysis.py          # Analisis data
│   │   └── model_performance.py # Performa model
│   └── styles/                   # Custom CSS styles
│       └── custom_styles.py
│
├── data/                         # Data storage
│   └── raw/
│       └── dataset.csv          # Dataset utama (3000 records)
│
├── models/                       # Model terlatih
│   ├── best_model.pkl           # Random Forest model
│   └── preprocessing_stats.pkl  # Stats untuk normalisasi
│
├── notebooks/                    # Jupyter Notebooks
│   ├── 01_EDA.ipynb            # Exploratory Data Analysis
│   └── 02_modeling.ipynb        # Model training & evaluation
│
├── src/                         # Source code modules
│   ├── data_preprocessing.py    # Data cleaning & preprocessing
│   ├── model_training.py        # Model training pipeline
│   └── utils.py                 # Utility functions (certificate generation)
│
├── reports/                      # Laporan & visualisasi
│
├── requirements.txt              # Python dependencies
├── save_model.py                # Script untuk save/retrain model
└── README.md                    # Dokumentasi ini
```

---

## 🚀 Instalasi

### Prasyarat
- Python 3.8 atau lebih tinggi
- pip (Python package manager)
- Git (untuk clone repository)

### Langkah Instalasi

1. **Clone repository**
   ```bash
   git clone https://github.com/ridlofw/resiko-stress-random-forest.git
   cd resiko-stress-random-forest
   ```

2. **Buat virtual environment** (Opsional, tapi sangat disarankan)
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Dependencies

```txt
streamlit>=1.28.0      # Web framework untuk aplikasi
pandas>=1.5.0          # Data manipulation
numpy>=1.23.0          # Numerical computing
scikit-learn>=1.2.0    # Machine learning
plotly>=5.15.0         # Interactive visualizations
Pillow>=10.0.0         # Image processing (certificate generation)
```

---

## 💻 Cara Menjalankan

### Menjalankan Aplikasi Web

```bash
streamlit run app/app.py
```

Aplikasi akan terbuka di browser pada `http://localhost:8501`

### Training Ulang Model

Jika Anda ingin melatih ulang model dengan data baru:

```bash
python save_model.py
```

Model baru akan disimpan di folder `models/`:
- `best_model.pkl` - Model Random Forest
- `preprocessing_stats.pkl` - Statistik untuk normalisasi

### Eksplorasi dengan Jupyter Notebook

```bash
jupyter notebook notebooks/01_EDA.ipynb
```

Atau gunakan Google Colab untuk membuka notebook.

---

## 📖 Panduan Penggunaan

### 1. 🏠 Halaman Beranda
- Lihat **ringkasan dataset** (total data, data sehat, data risiko stres)
- **Akurasi model** ditampilkan di metrics
- **Visualisasi distribusi** label dan gender dalam bentuk pie chart
- **Tabel preview** 10 data pertama

### 2. 🔮 Halaman Prediksi

#### Langkah-langkah:
1. Pilih **jumlah data** yang ingin diprediksi (1-5)
2. Isi form untuk setiap data:
   - Data personal (Nama, Gender, Umur, Jurusan, Status Hubungan)
   - Data akademik (IPK, Jam Belajar, Jumlah Tugas)
   - Data gaya hidup (Jam Tidur, Frekuensi Olahraga, Pemasukan Keluarga)
3. Klik **"🔍 Prediksi Sekarang"**
4. Lihat hasil prediksi dengan:
   - **Status**: Sehat ✅ atau Risiko Stres ⚠️
   - **Probabilitas** untuk masing-masing kategori
   - **Rekomendasi personal** berdasarkan hasil
5. **Download kartu hasil** dalam format PNG

#### Fitur Tambahan:
- **Reset Form**: Klik tombol "🔄 Reset Form" untuk membersihkan semua input
- **Batch Processing**: Prediksi beberapa mahasiswa sekaligus

### 3. 📈 Halaman Analisis Data
- Eksplorasi distribusi fitur-fitur dalam dataset
- Visualisasi interaktif untuk setiap variabel
- Analisis korelasi antar fitur

### 4. 📊 Halaman Performa Model
- **Confusion Matrix**: Visualisasi performa klasifikasi
- **Metrics**: Accuracy, Precision, Recall, F1-Score
- **Feature Importance**: Fitur mana yang paling berpengaruh pada prediksi

---

## 📈 Performa Model

Model Random Forest yang digunakan memiliki performa sebagai berikut:

- **Accuracy**: ~85-90% (pada test set)
- **F1-Score**: ~85-90% (weighted average)
- **Training Method**: 80/20 train-test split dengan random_state=42

### Confusion Matrix (Contoh)
```
                Predicted
                Sehat   Risiko Stres
Actual Sehat      360        40
       Risiko     50        150
```

### Feature Importance (Top 5)
1. Jam Tidur per Hari
2. IPK
3. Jumlah Tugas Besar per Minggu
4. Jam Belajar per Hari
5. Frekuensi Olahraga

---

## 🔬 Metodologi

### Preprocessing
1. **Cleaning**: Membersihkan format IPK (comma to dot conversion)
2. **Normalization**: Z-score normalization untuk fitur numerik
3. **Encoding**: One-Hot Encoding untuk fitur kategorikal
4. **Train-Test Split**: 80% training, 20% testing

### Model Training
- **Algorithm**: RandomForestClassifier dari scikit-learn
- **Pipeline**: Preprocessing + Model dalam satu pipeline
- **Cross-validation**: Menggunakan stratified split untuk balanced classes

---

## 🌐 Deploy ke Streamlit Cloud

Aplikasi ini dapat di-deploy ke **Streamlit Cloud** secara **gratis**!

### Quick Start Deploy

1. **Push repository ke GitHub**
2. **Login ke [share.streamlit.io](https://share.streamlit.io)**
3. **Klik "New app"** dan isi:
   - Repository: `ridlofw/resiko-stress-random-forest`
   - Branch: `main`
   - Main file: `app/app.py`
4. **Deploy!** ✨

**URL contoh**: `https://your-app-name.streamlit.app`

### 📖 Panduan Lengkap

Untuk panduan deployment detail dengan troubleshooting, lihat **[DEPLOYMENT.md](DEPLOYMENT.md)**

Topics covered:
- ✅ Persiapan repository
- ✅ Konfigurasi Streamlit Cloud
- ✅ Troubleshooting common errors
- ✅ Custom domain setup
- ✅ Best practices

---

## 🤝 Kontribusi

Kontribusi sangat diterima! Jika Anda ingin berkontribusi:

1. Fork repository ini
2. Buat branch fitur baru (`git checkout -b feature/amazing-feature`)
3. Commit perubahan (`git commit -m 'Add amazing feature'`)
4. Push ke branch (`git push origin feature/amazing-feature`)
5. Buat Pull Request

---

## 📝 Lisensi

Project ini dilisensikan di bawah [MIT License](LICENSE).

---

## 👨‍💻 Author

**Ridlo Firmansyah**
- GitHub: [@ridlofw](https://github.com/ridlofw)
- Repository: [resiko-stress-random-forest](https://github.com/ridlofw/resiko-stress-random-forest)

---

## 📞 Kontak & Dukungan

Jika Anda memiliki pertanyaan atau menemukan bug, silakan:
- Buat [Issue](https://github.com/ridlofw/resiko-stress-random-forest/issues) di GitHub
- Hubungi melalui email atau media sosial

---

## 🙏 Acknowledgments

- Dataset untuk keperluan edukasi dan penelitian
- Komunitas open source Python & Streamlit
- Scikit-learn untuk library machine learning yang powerful

---

<p align="center">
  <strong>⚡ Dibuat dengan ❤️ menggunakan Python & Streamlit</strong>
</p>

<p align="center">
  <sub>Jangan lupa berikan ⭐ jika project ini bermanfaat!</sub>
</p>
