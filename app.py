import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, classification_report
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Prediksi Risiko Stres Mahasiswa",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #6c757d;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    .stButton>button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    .result-box {
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        text-align: center;
    }
    .result-sehat {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
    }
    .result-stres {
        background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and preprocess the dataset"""
    df = pd.read_csv('dataset.csv', sep=';')
    return df

@st.cache_resource
def train_model(df):
    """Train the Random Forest model"""
    # Prepare features
    numeric_features = ['Umur', 'Jam Belajar per Hari', 'Jam Tidur per Hari', 'Jumlah Tugas Besar per Minggu']
    categorical_features = ['Gender', 'Jurusan/Program Studi', 'Frekuensi Olahraga', 'Pemasukan Keluarga', 'Status Hubungan']
    
    # Prepare data
    X = df.drop('Label', axis=1)
    # Drop IPK as it has inconsistent format in the dataset
    if 'IPK' in X.columns:
        X = X.drop('IPK', axis=1)
    y = df['Label']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Create preprocessor
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', 'passthrough', numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ],
        remainder='drop'
    )
    
    # Create pipeline
    model = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(
            n_estimators=200,
            max_depth=4,
            random_state=42,
            n_jobs=-1
        ))
    ])
    
    # Train model
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='weighted')
    cm = confusion_matrix(y_test, y_pred)
    
    return model, accuracy, f1, cm, X_test, y_test

def main():
    # Header
    st.markdown('<h1 class="main-header">🧠 Prediksi Risiko Stres Mahasiswa</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Sistem prediksi berbasis Random Forest untuk membantu mengidentifikasi risiko stres pada mahasiswa</p>', unsafe_allow_html=True)
    
    # Load data and train model
    try:
        df = load_data()
        model, accuracy, f1, cm, X_test, y_test = train_model(df)
    except FileNotFoundError:
        st.error("⚠️ File dataset.csv tidak ditemukan. Pastikan file dataset berada di direktori yang sama dengan aplikasi.")
        return
    except Exception as e:
        st.error(f"⚠️ Terjadi kesalahan: {str(e)}")
        return
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/brain.png", width=80)
        st.markdown("### 📊 Navigasi")
        page = st.radio(
            "Pilih Halaman:",
            ["🏠 Beranda", "🔮 Prediksi", "📈 Analisis Data", "📊 Performa Model"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown("### ℹ️ Tentang Aplikasi")
        st.info("""
        Aplikasi ini menggunakan algoritma **Random Forest** untuk memprediksi risiko stres pada mahasiswa berdasarkan berbagai faktor seperti:
        - Demografi
        - Kebiasaan belajar
        - Pola tidur
        - Aktivitas fisik
        - Faktor sosial
        """)
    
    # Pages
    if page == "🏠 Beranda":
        show_home_page(df, accuracy, f1)
    elif page == "🔮 Prediksi":
        show_prediction_page(df, model)
    elif page == "📈 Analisis Data":
        show_analysis_page(df)
    elif page == "📊 Performa Model":
        show_model_performance(accuracy, f1, cm)

def show_home_page(df, accuracy, f1):
    """Display home page with overview"""
    st.markdown("## 📋 Ringkasan Dataset")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Total Data", f"{len(df):,}")
    with col2:
        st.metric("🎯 Akurasi Model", f"{accuracy*100:.1f}%")
    with col3:
        sehat_count = len(df[df['Label'] == 'Sehat'])
        st.metric("✅ Data Sehat", f"{sehat_count:,}")
    with col4:
        stres_count = len(df[df['Label'] == 'Risiko Stres'])
        st.metric("⚠️ Data Risiko Stres", f"{stres_count:,}")
    
    st.markdown("---")
    
    # Distribution charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Distribusi Label")
        label_counts = df['Label'].value_counts()
        fig = px.pie(
            values=label_counts.values, 
            names=label_counts.index,
            color_discrete_sequence=['#38ef7d', '#f45c43'],
            hole=0.4
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(size=14)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 👤 Distribusi Gender")
        gender_counts = df['Gender'].value_counts()
        fig = px.pie(
            values=gender_counts.values, 
            names=gender_counts.index,
            color_discrete_sequence=['#667eea', '#764ba2'],
            hole=0.4
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(size=14)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Sample data
    st.markdown("### 📄 Contoh Data")
    st.dataframe(df.head(10), use_container_width=True)

def show_prediction_page(df, model):
    """Display prediction page"""
    st.markdown("## 🔮 Prediksi Risiko Stres")
    st.markdown("Isi formulir di bawah ini untuk memprediksi risiko stres berdasarkan profil Anda.")
    
    # Get unique values for dropdowns
    jurusan_list = df['Jurusan/Program Studi'].unique().tolist()
    
    # Input form
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 👤 Data Demografi")
        gender = st.selectbox("Gender", ["Laki-laki", "Perempuan"])
        umur = st.slider("Umur", 18, 25, 20)
        jurusan = st.selectbox("Jurusan/Program Studi", jurusan_list)
        status_hubungan = st.selectbox("Status Hubungan", ["Jomblo", "Dalam hubungan"])
        
        st.markdown("#### 💰 Status Ekonomi")
        pemasukan = st.selectbox("Pemasukan Keluarga", ["Rendah", "Sedang", "Tinggi"])
    
    with col2:
        st.markdown("#### 📚 Kebiasaan Belajar & Tidur")
        jam_belajar = st.slider("Jam Belajar per Hari", 1, 7, 4)
        jam_tidur = st.slider("Jam Tidur per Hari", 3, 9, 6)
        tugas_besar = st.slider("Jumlah Tugas Besar per Minggu", 0, 5, 2)
        
        st.markdown("#### 🏃 Aktivitas Fisik")
        olahraga = st.selectbox("Frekuensi Olahraga", ["Jarang", "Kadang", "Sering"])
    
    st.markdown("---")
    
    # Predict button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        predict_btn = st.button("🔍 Prediksi Risiko Stres", use_container_width=True)
    
    if predict_btn:
        # Prepare input data
        input_data = pd.DataFrame({
            'Gender': [gender],
            'Umur': [umur],
            'Jurusan/Program Studi': [jurusan],
            'Jam Belajar per Hari': [jam_belajar],
            'Jam Tidur per Hari': [jam_tidur],
            'Jumlah Tugas Besar per Minggu': [tugas_besar],
            'Frekuensi Olahraga': [olahraga],
            'Pemasukan Keluarga': [pemasukan],
            'Status Hubungan': [status_hubungan]
        })
        
        # Make prediction
        prediction = model.predict(input_data)[0]
        proba = model.predict_proba(input_data)[0]
        
        st.markdown("---")
        st.markdown("### 📊 Hasil Prediksi")
        
        if prediction == "Sehat":
            st.markdown("""
            <div class="result-box result-sehat">
                <h2>✅ SEHAT</h2>
                <p style="font-size: 1.2rem;">Berdasarkan analisis, Anda memiliki risiko stres yang rendah!</p>
            </div>
            """, unsafe_allow_html=True)
            st.balloons()
        else:
            st.markdown("""
            <div class="result-box result-stres">
                <h2>⚠️ RISIKO STRES</h2>
                <p style="font-size: 1.2rem;">Berdasarkan analisis, Anda memiliki potensi risiko stres. Pertimbangkan untuk berkonsultasi dengan konselor.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Show probability
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Probabilitas Sehat", f"{proba[1]*100:.1f}%" if model.classes_[1] == "Sehat" else f"{proba[0]*100:.1f}%")
        with col2:
            st.metric("Probabilitas Risiko Stres", f"{proba[0]*100:.1f}%" if model.classes_[0] == "Risiko Stres" else f"{proba[1]*100:.1f}%")
        
        # Recommendations
        st.markdown("### 💡 Rekomendasi")
        if prediction == "Risiko Stres":
            st.warning("""
            Berikut beberapa saran untuk mengurangi risiko stres:
            - 😴 **Tidur yang cukup** (7-9 jam per hari)
            - 🏃 **Olahraga teratur** (minimal 3x seminggu)
            - 📚 **Atur waktu belajar** dengan baik
            - 🧘 **Praktikkan teknik relaksasi** seperti meditasi
            - 👥 **Jaga hubungan sosial** dengan teman dan keluarga
            - 📞 **Konsultasi dengan konselor** jika diperlukan
            """)
        else:
            st.success("""
            Pertahankan pola hidup sehat Anda:
            - ✅ Tetap jaga pola tidur yang baik
            - ✅ Lanjutkan aktivitas fisik rutin
            - ✅ Kelola waktu dengan bijak
            - ✅ Pertahankan hubungan sosial yang positif
            """)

def show_analysis_page(df):
    """Display data analysis page"""
    st.markdown("## 📈 Analisis Data")
    
    # Tabs for different analyses
    tab1, tab2, tab3 = st.tabs(["📊 Distribusi", "🔗 Korelasi", "📋 Statistik"])
    
    with tab1:
        st.markdown("### Distribusi Fitur berdasarkan Label")
        
        # Select feature
        numeric_cols = ['Umur', 'Jam Belajar per Hari', 'Jam Tidur per Hari', 'Jumlah Tugas Besar per Minggu']
        selected_feature = st.selectbox("Pilih Fitur", numeric_cols)
        
        # Box plot
        fig = px.box(
            df, 
            x='Label', 
            y=selected_feature, 
            color='Label',
            color_discrete_map={'Sehat': '#38ef7d', 'Risiko Stres': '#f45c43'}
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(size=14)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Histogram
        fig2 = px.histogram(
            df, 
            x=selected_feature, 
            color='Label',
            barmode='overlay',
            color_discrete_map={'Sehat': '#38ef7d', 'Risiko Stres': '#f45c43'},
            opacity=0.7
        )
        fig2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(size=14)
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    with tab2:
        st.markdown("### Analisis Kategorikal")
        
        categorical_cols = ['Jurusan/Program Studi', 'Frekuensi Olahraga', 'Pemasukan Keluarga', 'Status Hubungan', 'Gender']
        selected_cat = st.selectbox("Pilih Kategori", categorical_cols)
        
        # Grouped bar chart
        grouped = df.groupby([selected_cat, 'Label']).size().reset_index(name='Count')
        fig = px.bar(
            grouped, 
            x=selected_cat, 
            y='Count', 
            color='Label',
            barmode='group',
            color_discrete_map={'Sehat': '#38ef7d', 'Risiko Stres': '#f45c43'}
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(size=14),
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("### Statistik Deskriptif")
        
        # Filter by label
        label_filter = st.selectbox("Filter berdasarkan Label", ["Semua", "Sehat", "Risiko Stres"])
        
        if label_filter == "Semua":
            display_df = df
        else:
            display_df = df[df['Label'] == label_filter]
        
        # Show statistics
        numeric_cols = ['Umur', 'Jam Belajar per Hari', 'Jam Tidur per Hari', 'Jumlah Tugas Besar per Minggu']
        st.dataframe(display_df[numeric_cols].describe(), use_container_width=True)

def show_model_performance(accuracy, f1, cm):
    """Display model performance page"""
    st.markdown("## 📊 Performa Model Random Forest")
    
    # Metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Metrik Evaluasi")
        
        # Gauge chart for accuracy
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = accuracy * 100,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Akurasi (%)", 'font': {'size': 24}},
            gauge = {
                'axis': {'range': [None, 100], 'tickwidth': 1},
                'bar': {'color': "#667eea"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 50], 'color': '#f45c43'},
                    {'range': [50, 75], 'color': '#ffd93d'},
                    {'range': [75, 100], 'color': '#38ef7d'}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 4},
                    'thickness': 0.75,
                    'value': accuracy * 100
                }
            }
        ))
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            font={'color': "white", 'family': "Arial"}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.metric("F1-Score (Weighted)", f"{f1*100:.1f}%")
    
    with col2:
        st.markdown("### 📉 Confusion Matrix")
        
        # Confusion matrix heatmap
        labels = ['Risiko Stres', 'Sehat']
        fig = px.imshow(
            cm,
            labels=dict(x="Prediksi", y="Aktual", color="Jumlah"),
            x=labels,
            y=labels,
            color_continuous_scale='Purples',
            text_auto=True
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(size=14)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Model explanation
    st.markdown("---")
    st.markdown("### 🧠 Tentang Model")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### Parameter Model
        | Parameter | Nilai |
        |-----------|-------|
        | Algoritma | Random Forest |
        | Jumlah Trees | 200 |
        | Max Depth | 4 |
        | Random State | 42 |
        | Test Size | 20% |
        """)
    
    with col2:
        st.markdown("""
        #### Fitur yang Digunakan
        - **Numerik**: Umur, Jam Belajar, Jam Tidur, Jumlah Tugas
        - **Kategorikal**: Gender, Jurusan, Frekuensi Olahraga, Pemasukan Keluarga, Status Hubungan
        """)

if __name__ == "__main__":
    main()
