import pickle
from src.data_preprocessing import load_data
from src.model_training import train_model

print("=" * 80)
print("SAVING MODEL")
print("=" * 80)

# Load data
print("\n📂 Loading data...")
df = load_data('data/raw/dataset.csv')
print(f"✅ Data loaded: {len(df):,} rows")

# Train model
print("\n🚀 Training model...")
model, accuracy, f1, cm, X_test, y_test, stats = train_model(df)

print(f"\n📊 Model Performance:")
print(f"  • Accuracy: {accuracy*100:.2f}%")
print(f"  • F1-Score: {f1*100:.2f}%")

# Save model
print("\n💾 Saving model...")
with open('models/best_model.pkl', 'wb') as f:
    pickle.dump(model, f)
print("✅ Model saved to: models/best_model.pkl")

# Save preprocessing stats
print("\n💾 Saving preprocessing stats...")
with open('models/preprocessing_stats.pkl', 'wb') as f:
    pickle.dump(stats, f)
print("✅ Stats saved to: models/preprocessing_stats.pkl")

print("\n" + "=" * 80)
print("✅ ALL FILES SAVED SUCCESSFULLY!")
print("=" * 80)