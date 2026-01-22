from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

from .data_preprocessing import preprocess_data, get_preprocessing_stats

def train_model(df):
    """Train the Random Forest model"""
    # Preprocess data
    processed_df = preprocess_data(df)
    
    # Define features
    numeric_features = ['Umur', 'Jam Belajar per Hari', 'Jam Tidur per Hari', 'IPK', 'Jumlah Tugas Besar per Minggu']
    categorical_features = ['Gender', 'Jurusan/Program Studi', 'Frekuensi Olahraga', 'Pemasukan Keluarga', 'Status Hubungan']
    
    # Prepare data
    X = processed_df.drop('Label', axis=1)
    y = processed_df['Label']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Create preprocessor
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', 'passthrough', numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ],
        remainder='passthrough'
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
    
    # Get preprocessing stats
    stats = get_preprocessing_stats(df)
    
    return model, accuracy, f1, cm, X_test, y_test, stats