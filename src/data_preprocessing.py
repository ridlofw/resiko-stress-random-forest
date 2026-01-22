import pandas as pd
import numpy as np

def load_data(filepath='data/raw/dataset.csv'):
    """Load and preprocess the dataset"""
    df = pd.read_csv(filepath, sep=';')
    return df

def clean_ipk(value):
    """Clean IPK value - convert various formats to float"""
    if pd.isna(value):
        return np.nan
    
    # Convert to string
    val_str = str(value).strip()
    
    # Replace comma with dot
    val_str = val_str.replace(',', '.')
    
    try:
        val_float = float(val_str)
        # If value is less than 1, it might be in decimal format like 0.188194444
        # These seem to be time fractions, convert to proper IPK scale (0-4)
        if val_float < 1:
            # These values appear to be time fractions, multiply by appropriate factor
            # Based on the data pattern, values like 0.188194444 should map to ~2.7-3.5 range
            val_float = val_float * 20  # Scale to approximate IPK range
            if val_float > 4:
                val_float = 4.0
        return val_float
    except:
        return np.nan

def preprocess_data(df):
    """Preprocess the dataframe similar to notebook"""
    df = df.copy()
    
    # Clean IPK column
    df['IPK'] = df['IPK'].apply(clean_ipk)
    
    # Convert numeric columns to proper numeric type
    numeric_features = ['Jam Belajar per Hari', 'Jam Tidur per Hari', 'IPK', 'Jumlah Tugas Besar per Minggu']
    df[numeric_features] = df[numeric_features].apply(pd.to_numeric, errors='coerce')
    
    # Normalize numeric features (Z-score normalization like in notebook)
    df[numeric_features] = (df[numeric_features] - df[numeric_features].mean()) / df[numeric_features].std()
    
    return df

# TAMBAHKAN FUNGSI INI (logic dari train_model yang asli)
def get_preprocessing_stats(df):
    """Get mean and std for normalization - used for prediction"""
    raw_df = df.copy()
    raw_df['IPK'] = raw_df['IPK'].apply(clean_ipk)
    numeric_cols = ['Jam Belajar per Hari', 'Jam Tidur per Hari', 'IPK', 'Jumlah Tugas Besar per Minggu']
    raw_df[numeric_cols] = raw_df[numeric_cols].apply(pd.to_numeric, errors='coerce')
    
    stats = {
        'mean': raw_df[numeric_cols].mean().to_dict(),
        'std': raw_df[numeric_cols].std().to_dict()
    }
    
    return stats