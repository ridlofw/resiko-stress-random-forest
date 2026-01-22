import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

def show_model_performance(accuracy, f1, cm, model):
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
    
    # Feature Importance
    st.markdown("---")
    st.markdown("### 🔍 Fitur Paling Berpengaruh")
    
    try:
        # Get feature importance from the Random Forest model
        importances = model.named_steps['classifier'].feature_importances_
        
        # Get feature names after preprocessing
        feature_names = model.named_steps['preprocessor'].get_feature_names_out()
        
        # Create a dictionary of feature importance
        import pandas as pd
        importance_df = pd.DataFrame({
            'Feature': feature_names,
            'Importance': importances
        }).sort_values('Importance', ascending=False).head(10)
        
        # Create bar chart
        fig = px.bar(
            importance_df,
            x='Importance',
            y='Feature',
            orientation='h',
            title='Top 10 Fitur Paling Berpengaruh',
            color='Importance',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(
            yaxis={'categoryorder':'total ascending'},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("""
        💡 **Interpretasi Feature Importance:**
        - Semakin tinggi nilai importance, semakin besar pengaruh fitur tersebut terhadap prediksi
        - Fitur dengan importance tinggi adalah faktor utama yang menentukan risiko stres
        - Model menggunakan kombinasi semua fitur untuk prediksi yang akurat
        """)
        
    except Exception as e:
        st.warning(f"Feature importance tidak dapat ditampilkan: {str(e)}")
    
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
        - **Numerik**: Umur, Jam Belajar, Jam Tidur, IPK, Jumlah Tugas
        - **Kategorikal**: Gender, Jurusan, Frekuensi Olahraga, Pemasukan Keluarga, Status Hubungan
        """)