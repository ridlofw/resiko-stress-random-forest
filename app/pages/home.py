import streamlit as st
import plotly.express as px

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