# 🚀 Panduan Deploy ke Streamlit Cloud

Panduan lengkap untuk deploy aplikasi **Prediksi Risiko Stres Mahasiswa** ke Streamlit Cloud secara gratis.

---

## 📋 Prasyarat

Sebelum deploy, pastikan Anda sudah memiliki:

- ✅ Akun GitHub (jika belum punya, buat di [github.com](https://github.com))
- ✅ Repository GitHub untuk proyek ini (sudah di-push)
- ✅ Akun Streamlit Cloud (gratis, bisa login dengan GitHub)

---

## 🔧 Persiapan Deployment

### 1. Pastikan File Penting Ada

Cek file-file berikut di repository Anda:

```
✅ requirements.txt       # Dependencies
✅ app/app.py            # Main application
✅ data/raw/dataset.csv  # Dataset
✅ models/*.pkl          # Model files (jika sudah di-train)
```

### 2. Update `.gitignore` (Opsional)

Jika model files terlalu besar (>100MB), jangan push ke GitHub. Sebagai gantinya, aplikasi akan train model otomatis saat pertama kali deploy.

**File `.gitignore` yang sudah ada:**
```gitignore
# Models (Keep them if small, but often ignored if large)
# models/*.pkl

# Data (Often ignored if large)
# data/raw/*.csv
```

> **Catatan**: Jika dataset.csv dan model.pkl di-ignore, aplikasi akan otomatis train model saat startup (bisa memakan waktu 1-2 menit pertama kali).

### 3. Buat File Konfigurasi Streamlit (Opsional)

Buat folder `.streamlit/` dan file `config.toml` untuk konfigurasi tambahan:

```bash
mkdir .streamlit
```

**File: `.streamlit/config.toml`**
```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
port = 8501
enableCORS = false
```

---

## 🌐 Deploy ke Streamlit Cloud

### Langkah 1: Push ke GitHub

Jika belum di-push, jalankan:

```bash
# Initialize git (jika belum)
git init

# Add semua file
git add .

# Commit
git commit -m "Initial commit - Ready for deployment"

# Add remote repository
git remote add origin https://github.com/ridlofw/resiko-stress-random-forest.git

# Push
git push -u origin main
```

### Langkah 2: Login ke Streamlit Cloud

1. Buka **[share.streamlit.io](https://share.streamlit.io)**
2. Klik **"Sign up"** atau **"Continue with GitHub"**
3. Authorize Streamlit Cloud untuk akses repository GitHub Anda

### Langkah 3: Deploy Aplikasi

1. **Klik "New app"** di dashboard Streamlit Cloud

2. **Isi form deployment:**
   ```
   Repository:  ridlofw/resiko-stress-random-forest
   Branch:      main
   Main file:   app/app.py
   ```

3. **Advanced settings** (opsional):
   - **Python version**: 3.9 atau 3.10
   - **Secrets**: Jika ada API keys (tidak ada untuk project ini)

4. **Klik "Deploy!"**

### Langkah 4: Tunggu Deployment

Streamlit Cloud akan:
- ✅ Clone repository Anda
- ✅ Install dependencies dari `requirements.txt`
- ✅ Run aplikasi Anda
- ✅ Generate URL public (contoh: `https://ridlofw-resiko-stress-random-forest-app-app-xyz123.streamlit.app`)

**Waktu deploy:** ~2-5 menit (tergantung ukuran dependencies)

---

## 🔍 Monitoring & Troubleshooting

### Melihat Logs

Di dashboard Streamlit Cloud:
1. Klik aplikasi Anda
2. Klik **"Manage app"**
3. Lihat tab **"Logs"** untuk debug

### Common Issues & Solutions

#### ❌ Error: "ModuleNotFoundError"

**Penyebab**: Dependency tidak ada di `requirements.txt`

**Solusi**:
```bash
# Generate requirements dari environment
pip freeze > requirements.txt

# Atau tambahkan manual
echo "missing-package>=1.0.0" >> requirements.txt
```

Lalu commit dan push:
```bash
git add requirements.txt
git commit -m "Update requirements"
git push
```

Streamlit Cloud akan otomatis re-deploy.

#### ❌ Error: "FileNotFoundError: dataset.csv"

**Penyebab**: File dataset tidak ada di repository

**Solusi**: Pastikan `data/raw/dataset.csv` ada dan di-commit:
```bash
git add data/raw/dataset.csv
git commit -m "Add dataset"
git push
```

#### ❌ Error: Model file terlalu besar

**Penyebab**: GitHub limit 100MB per file

**Solusi 1** - Git LFS (Large File Storage):
```bash
# Install Git LFS
git lfs install

# Track model files
git lfs track "models/*.pkl"

# Commit .gitattributes
git add .gitattributes
git commit -m "Add Git LFS tracking"
git push
```

**Solusi 2** - Train on deployment:
Aplikasi sudah support ini! Model akan otomatis train jika file tidak ditemukan.

#### ⚠️ Warning: App sleeping

**Penyebab**: Streamlit Cloud (Free tier) akan sleep setelah tidak ada aktivitas

**Solusi**: 
- Upgrade ke paid tier untuk 24/7 uptime
- Atau biarkan (akan wake up otomatis saat user mengakses)

---

## 🔐 Environment Variables (Jika Diperlukan)

Jika aplikasi Anda butuh credentials/secrets:

1. Di Streamlit Cloud dashboard, klik **"⚙️ Settings"**
2. Pilih **"Secrets"**
3. Tambahkan secrets dalam format TOML:

```toml
# .streamlit/secrets.toml format
API_KEY = "your-api-key-here"
DATABASE_URL = "your-db-url"
```

4. Akses di code:
```python
import streamlit as st
api_key = st.secrets["API_KEY"]
```

> **Note**: Project ini tidak membutuhkan secrets.

---

## 📊 Update Aplikasi Setelah Deploy

Setiap kali Anda push ke GitHub, Streamlit Cloud akan **otomatis re-deploy**:

```bash
# Edit code
nano app/app.py

# Commit & push
git add .
git commit -m "Update: fix typo"
git push
```

Deploy otomatis dalam ~1-2 menit!

---

## 🎯 Custom Domain (Opsional)

Streamlit Cloud memberikan URL default seperti:
```
https://ridlofw-resiko-stress-random-forest-app-app-xyz123.streamlit.app
```

Untuk **custom domain** (misal: `stress-predictor.yourdomain.com`):

1. Upgrade ke **Streamlit Cloud Teams** ($250/bulan)
2. Atau gunakan **reverse proxy** gratis (Cloudflare, dll)

---

## ✅ Checklist Deployment

Sebelum deploy, pastikan:

- [ ] Repository sudah public/private di GitHub
- [ ] File `requirements.txt` lengkap dan benar
- [ ] Path file menggunakan relative path (bukan absolute)
- [ ] Dataset dan model ada di repository (atau train otomatis)
- [ ] Test aplikasi local dengan `streamlit run app/app.py`
- [ ] Commit semua perubahan
- [ ] Push ke GitHub

---

## 🌟 Best Practices

1. **Gunakan `.streamlit/config.toml`** untuk customization
2. **Tambahkan `.streamlit/secrets.toml`** ke `.gitignore` (jangan push secrets!)
3. **Optimize model size** - compress jika perlu
4. **Cache data loading** - gunakan `@st.cache_data` (sudah diimplementasi)
5. **Monitor logs** - cek regular untuk errors
6. **Version control** - gunakan semantic versioning (v1.0.0, v1.1.0, dll)

---

## 📱 Share Aplikasi

Setelah deploy berhasil, share URL ke:
- ✅ LinkedIn
- ✅ Portfolio website
- ✅ Email dosen/pembimbing
- ✅ WhatsApp grup

**Example announcement:**
```
🚀 Excited to share my latest project!

"Prediksi Risiko Stres Mahasiswa" - A machine learning web app 
to predict student stress risk using Random Forest.

🔗 Try it: https://your-app-url.streamlit.app
💻 Code: https://github.com/ridlofw/resiko-stress-random-forest

#MachineLearning #Streamlit #DataScience
```

---

## 🔗 Resources

- **Streamlit Docs**: [docs.streamlit.io](https://docs.streamlit.io)
- **Deployment Guide**: [docs.streamlit.io/streamlit-community-cloud](https://docs.streamlit.io/streamlit-community-cloud)
- **Community Forum**: [discuss.streamlit.io](https://discuss.streamlit.io)
- **GitHub**: [github.com/streamlit](https://github.com/streamlit)

---

## 💡 Next Steps

Setelah deploy berhasil:

1. ✅ Test aplikasi di production URL
2. ✅ Share dengan teman untuk feedback
3. ✅ Monitor usage dan errors
4. ✅ Iterasi dan improve berdasarkan feedback
5. ✅ Tambahkan ke portfolio/CV

---

## 📞 Butuh Bantuan?

- 💬 Streamlit Community Forum
- 📧 Email support Streamlit
- 🐛 GitHub Issues di repository Anda

---

<p align="center">
  <strong>🎉 Selamat! Aplikasi Anda sudah live di internet!</strong>
</p>
