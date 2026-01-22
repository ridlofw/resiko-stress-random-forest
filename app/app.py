import streamlit as st
import sys
from pathlib import Path
import pickle
import os

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from src.data_preprocessing import load_data, preprocess_data
from src.model_training import train_model
from styles.custom_styles import get_custom_css
from pages.home import show_home_page
from pages.prediction import show_prediction_page
from pages.analysis import show_analysis_page
from pages.model_performance import show_model_performance

# Page configuration
st.set_page_config(
    page_title="Prediksi Risiko Stres Mahasiswa",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# Apply custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

@st.cache_resource
def load_and_train():
    """Load data and train model (or load from file if exists)"""
    # Get absolute paths
    base_dir = Path(__file__).parent.parent
    dataset_path = base_dir / 'data' / 'raw' / 'dataset.csv'
    
    df = load_data(str(dataset_path))
    
    # Check if saved model exists
    model_path = str(base_dir / 'models' / 'best_model.pkl')
    stats_path = str(base_dir / 'models' / 'preprocessing_stats.pkl')
    
    if os.path.exists(model_path) and os.path.exists(stats_path):
        print("[INFO] Loading model from file...")
        
        try:
            # Load model
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            
            # Load stats
            with open(stats_path, 'rb') as f:
                stats = pickle.load(f)
            
            # Get test data for evaluation metrics
            from sklearn.model_selection import train_test_split
            from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
            
            processed_df = preprocess_data(df)
            X = processed_df.drop('Label', axis=1)
            y = processed_df['Label']
            _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred, average='weighted')
            cm = confusion_matrix(y_test, y_pred)
            
            print("[SUCCESS] Model loaded from file!")
            return df, model, accuracy, f1, cm, X_test, y_test, stats
            
        except Exception as e:
            print(f"[WARNING] Error loading model: {e}")
            print("[INFO] Training new model instead...")
            # If loading fails, train new model
            model, accuracy, f1, cm, X_test, y_test, stats = train_model(df)
            return df, model, accuracy, f1, cm, X_test, y_test, stats
    
    else:
        print("[INFO] No saved model found. Training new model...")
        model, accuracy, f1, cm, X_test, y_test, stats = train_model(df)
        return df, model, accuracy, f1, cm, X_test, y_test, stats

def main():
    # Header
    st.markdown('<h1 class="main-header">🧠 Prediksi Risiko Stres Mahasiswa</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Sistem prediksi berbasis Random Forest untuk membantu mengidentifikasi risiko stres pada mahasiswa</p>', unsafe_allow_html=True)
    
    # Load data and train model
    try:
        df, model, accuracy, f1, cm, X_test, y_test, stats = load_and_train()
    except FileNotFoundError:
        st.error("⚠️ File dataset.csv tidak ditemukan. Pastikan file dataset berada di folder data/raw/")
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
        - IPK
        - Aktivitas fisik
        - Faktor sosial
        """)
    
    # Pages
    if page == "🏠 Beranda":
        show_home_page(df, accuracy, f1)
    elif page == "🔮 Prediksi":
        show_prediction_page(df, model, stats)
    elif page == "📈 Analisis Data":
        show_analysis_page(df)
    elif page == "📊 Performa Model":
        show_model_performance(accuracy, f1, cm, model)

if __name__ == "__main__":
    main()