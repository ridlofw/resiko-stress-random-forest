import streamlit as st
import pandas as pd
from src.utils import generate_certificate_image

def show_prediction_page(df, model, stats):
    st.markdown("## 🔮 Prediksi Risiko Stres")

    st.warning("""
    ⚠️ **DISCLAIMER**
    
    Aplikasi ini diperuntukkan **Mahasiswa S1**
    dengan rentang umur **maksimal 25 tahun**.
    
    Hasil prediksi **bukan diagnosis medis**.
    """)

    # Initialize reset counter
    if "reset_counter" not in st.session_state:
        st.session_state.reset_counter = 0
    
    if "show_result" not in st.session_state:
        st.session_state.show_result = False

    jurusan_list = df['Jurusan/Program Studi'].unique().tolist()
    
    # Use reset_counter in key to force widget recreation
    reset_key = st.session_state.reset_counter

    jumlah_data = st.selectbox(
        "Jumlah data yang ingin diprediksi (maksimal 5)",
        [1, 2, 3, 4, 5],
        key=f"jumlah_data_{reset_key}"
    )

    data_batch = []

    for i in range(jumlah_data):
        st.markdown(f"### 👤 Data ke-{i+1}")
        col1, col2 = st.columns(2)

        with col1:
            nama = st.text_input("Nama Lengkap", "Mahasiswa", key=f"n{i}_{reset_key}")
            gender = st.selectbox("Gender", ["Laki-laki", "Perempuan"], key=f"g{i}_{reset_key}")
            umur = st.slider("Umur", 18, 25, 20, key=f"u{i}_{reset_key}")
            jurusan = st.selectbox("Jurusan", jurusan_list, key=f"j{i}_{reset_key}")
            status = st.selectbox("Status Hubungan", ["Jomblo", "Dalam hubungan"], key=f"s{i}_{reset_key}")
            pemasukan = st.selectbox("Pemasukan Keluarga", ["Rendah", "Sedang", "Tinggi"], key=f"p{i}_{reset_key}")

        with col2:
            ipk = st.slider("IPK", 0.0, 4.0, 3.0, 0.01, key=f"ipk{i}_{reset_key}")
            belajar = st.slider("Jam Belajar per Hari", 1, 7, 4, key=f"b{i}_{reset_key}")
            tidur = st.slider("Jam Tidur per Hari", 3, 9, 6, key=f"t{i}_{reset_key}")
            tugas = st.slider("Jumlah Tugas Besar per Minggu", 0, 5, 2, key=f"tb{i}_{reset_key}")
            olahraga = st.selectbox("Frekuensi Olahraga", ["Jarang", "Kadang", "Sering"], key=f"o{i}_{reset_key}")

        data_batch.append({
            "Nama": nama,
            "Gender": gender,
            "Umur": umur,
            "Jurusan/Program Studi": jurusan,
            "Status Hubungan": status,
            "Pemasukan Keluarga": pemasukan,
            "IPK": ipk,
            "Jam Belajar": belajar,
            "Jam Tidur": tidur,
            "Jumlah Tugas": tugas,
            "Olahraga": olahraga
        })

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔍 Prediksi Sekarang", use_container_width=True):
            # Save current input data to session state
            st.session_state.prediction_data = data_batch.copy()
            st.session_state.show_result = True
            st.rerun()

    with col2:
        if st.button("🔄 Reset Form", use_container_width=True):
            # Increment reset counter to force widget recreation
            st.session_state.reset_counter += 1
            st.session_state.show_result = False
            if 'prediction_data' in st.session_state:
                del st.session_state.prediction_data
            st.success("✅ Form berhasil direset!")
            st.rerun()

    # Only show results if prediction button was clicked
    if st.session_state.show_result and 'prediction_data' in st.session_state:
        for idx, data in enumerate(st.session_state.prediction_data):
            st.markdown("---")
            st.markdown(f"## 📊 Hasil Prediksi Data ke-{idx+1}")

            input_df = pd.DataFrame({
                "Gender": [data["Gender"]],
                "Umur": [data["Umur"]],
                "Jurusan/Program Studi": [data["Jurusan/Program Studi"]],
                "Jam Belajar per Hari": [(data["Jam Belajar"] - stats['mean']['Jam Belajar per Hari']) / stats['std']['Jam Belajar per Hari']],
                "Jam Tidur per Hari": [(data["Jam Tidur"] - stats['mean']['Jam Tidur per Hari']) / stats['std']['Jam Tidur per Hari']],
                "IPK": [(data["IPK"] - stats['mean']['IPK']) / stats['std']['IPK']],
                "Jumlah Tugas Besar per Minggu": [(data["Jumlah Tugas"] - stats['mean']['Jumlah Tugas Besar per Minggu']) / stats['std']['Jumlah Tugas Besar per Minggu']],
                "Frekuensi Olahraga": [data["Olahraga"]],
                "Pemasukan Keluarga": [data["Pemasukan Keluarga"]],
                "Status Hubungan": [data["Status Hubungan"]]
            })

            pred = model.predict(input_df)[0]
            proba = model.predict_proba(input_df)[0]

            sehat_idx = list(model.classes_).index("Sehat")
            stres_idx = list(model.classes_).index("Risiko Stres")

            if pred == "Sehat":
                st.markdown("""
                <div class="result-box result-sehat">
                    <h2>✅ SEHAT</h2>
                    <p>Risiko stres rendah</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="result-box result-stres">
                    <h2>⚠️ RISIKO STRES</h2>
                    <p>Berpotensi mengalami stres</p>
                </div>
                """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            col1.metric("Probabilitas Sehat", f"{proba[sehat_idx]*100:.1f}%")
            col2.metric("Probabilitas Risiko Stres", f"{proba[stres_idx]*100:.1f}%")

            # Generate personalized recommendations based on input data
            recommendations = []
            
            # Check sleep hours
            if data["Jam Tidur"] < 6:
                recommendations.append(f"⏰ **Tingkatkan jam tidur** dari {data['Jam Tidur']} jam menjadi 7-9 jam per hari untuk pemulihan optimal")
            elif data["Jam Tidur"] > 9:
                recommendations.append(f"⏰ **Kurangi jam tidur** dari {data['Jam Tidur']} jam menjadi 7-9 jam (tidur berlebihan bisa menurunkan produktivitas)")
            
            # Check study hours
            if data["Jam Belajar"] > 6:
                recommendations.append(f"📚 **Atur ulang waktu belajar** - {data['Jam Belajar']} jam terlalu lama. Fokus pada kualitas, bukan kuantitas (4-5 jam efektif lebih baik)")
            elif data["Jam Belajar"] < 2:
                recommendations.append(f"📚 **Tambah waktu belajar** dari {data['Jam Belajar']} jam menjadi minimal 3-4 jam per hari")
            
            # Check exercise
            if data["Olahraga"] == "Jarang":
                recommendations.append("🏃 **Mulai olahraga rutin** minimal 3x seminggu (30 menit) untuk mengurangi stres dan meningkatkan fokus")
            
            # Check GPA
            if data["IPK"] < 2.5:
                recommendations.append(f"📈 **Tingkatkan strategi belajar** - IPK {data['IPK']:.2f} perlu perhatian khusus. Pertimbangkan belajar kelompok atau konsultasi dosen")
            
            # Check workload
            if data["Jumlah Tugas"] >= 4:
                recommendations.append(f"📝 **Kelola beban tugas** - {data['Jumlah Tugas']} tugas besar per minggu sangat tinggi. Buat prioritas dan deadline yang realistis")
            
            # Check relationship status for stress context
            if data["Status Hubungan"] == "Dalam hubungan" and pred == "Risiko Stres":
                recommendations.append("💑 **Balance kehidupan pribadi** - Komunikasikan kebutuhan waktu belajar dengan pasangan")
            
            if pred == "Risiko Stres":
                if recommendations:
                    st.warning("💡 **Rekomendasi Personal untuk Anda:**\n\n" + "\n".join([f"- {rec}" for rec in recommendations]))
                else:
                    st.warning("""
                    💡 **Rekomendasi Umum**
                    - Jaga pola tidur 7-9 jam
                    - Kelola waktu dengan baik
                    - Lakukan aktivitas relaksasi
                    - Konsultasi dengan konselor jika diperlukan
                    """)
            else:
                positive_tips = []
                if data["Jam Tidur"] >= 7 and data["Jam Tidur"] <= 9:
                    positive_tips.append(f"✅ Pola tidur Anda ({data['Jam Tidur']} jam) sudah ideal!")
                if data["Olahraga"] in ["Kadang", "Sering"]:
                    positive_tips.append(f"✅ Kebiasaan olahraga '{data['Olahraga']}' sangat baik!")
                if data["IPK"] >= 3.0:
                    positive_tips.append(f"✅ IPK {data['IPK']:.2f} menunjukkan performa akademik yang baik!")
                
                tips_text = "\n".join([f"- {tip}" for tip in positive_tips]) if positive_tips else ""
                
                st.success(f"""
                💡 **Pertahankan Pola Hidup Sehat!**
                
{tips_text}

**Saran untuk tetap optimal:**
- Jaga konsistensi pola tidur dan belajar
- Tetap aktif bergerak dan berolahraga
- Luangkan waktu untuk hobi dan relaksasi
                """)

            # Generate image for download
            img_bytes = generate_certificate_image(
                data["Nama"], 
                pred, 
                proba[sehat_idx]*100, 
                proba[stres_idx]*100, 
                data
            )
            
            st.download_button(
                label="📥 Download Kartu Hasil (PNG)",
                data=img_bytes,
                file_name=f"Hasil_Prediksi_{data['Nama']}.png",
                mime="image/png",
                key=f"dl_{idx}"
            )