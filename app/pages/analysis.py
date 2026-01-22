import streamlit as st
import plotly.express as px

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