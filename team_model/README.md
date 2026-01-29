# 🤖 Model Team - Deep Learning CNN-LSTM Component

## 🧠 Team Responsibility
Develop, train, and optimize the deep learning model that predicts tsunami risk from multi-modal data.

## 👥 Team Members
- **Lead:** [Your Name]
- **Contributors:** [Team Members]

---

## 📋 Overview

The Model team builds and maintains the CNN-LSTM neural network that forms the intelligent core of the tsunami warning system. We process earthquake, ocean, and spatial data to predict tsunami probability.

### **Model Architecture:**
- **Input:** 3 modalities (earthquake, ocean, bathymetry)
- **CNN Layers:** Extract spatial patterns
- **LSTM Layers:** Analyze temporal evolution
- **Output:** Risk probability (0-1), confidence, risk class

---

## 🎯 Key Responsibilities

- ✅ Build multi-modal CNN-LSTM architecture
- ✅ Train model on global historical tsunami data
- ✅ Implement focal loss for class imbalance handling
- ✅ Achieve high accuracy (>98%)
- ✅ Optimize inference speed (<200ms)
- ✅ Handle data preprocessing and feature scaling
- ✅ Implement model evaluation metrics
- ✅ Save and serialize trained models

---

## 📁 Project Files You Own

```
src/models/
├── cnn_lstm_binary_model.py   ← Model architecture definition
├── data_preprocessor.py        ← Data preprocessing pipeline
└── model_trainer.py            ← Training loop & utilities

models/
├── tsunami_detection_binary_focal.keras   ← Trained model (2.3MB)
└── model_metadata.json                    ← Model info & performance

notebooks/
└── Train_Tsunami_Binary_Focal_Loss_Kaggle.ipynb  ← Training notebook

scripts/
└── train_model.py             ← Command-line training script
```

---

## 🔧 Technologies Used

- **TensorFlow 2.18** - Deep learning framework
- **Keras** - Neural network API
- **NumPy** - Numerical operations
- **Pandas** - Data manipulation
- **scikit-learn** - Data preprocessing & metrics

---

## 📊 Model Specifications

### **Input Shape**
```python
# Earthquake data: (timesteps=24, features=4)
#   Features: magnitude, depth, latitude, longitude

# Ocean data: (locations=5, features=3)
#   Features: sea_level_anomaly, wave_height, wave_period

# Spatial data: (height=64, width=64, channels=2)
#   Channels: bathymetry, distance_to_coast

# Combined: (24, 32) after flattening
```

### **Model Architecture**
```
Input (24, 32)
    ↓
CNN Block 1: Conv2D(32, 3x3) → MaxPool(2x2) → Dropout(0.3)
CNN Block 2: Conv2D(64, 3x3) → MaxPool(2x2) → Dropout(0.3)
    ↓
LSTM Block 1: LSTM(128, return_seq=True) → Dropout(0.3)
LSTM Block 2: LSTM(64, return_seq=False) → Dropout(0.3)
    ↓
Dense 1: Dense(128, relu) → Dropout(0.3)
Dense 2: Dense(64, relu) → Dropout(0.2)
Dense 3: Dense(32, relu)
    ↓
Output: Dense(1, sigmoid) → Probability [0-1]
```

### **Model Statistics**
- **Total Parameters:** 185,729
- **Model Size:** 2.3 MB
- **Inference Time (CPU):** ~100-200 ms
- **Training Time:** ~15-30 min (50 epochs on GPU)

---

## 📈 Performance Metrics

### **Validation Results**
| Metric | Value | Status |
|--------|-------|--------|
| Accuracy | 98.90% | ✅ |
| AUC-ROC | 1.0000 | ✅ |
| Recall | 97.23% | ✅ |
| Precision | 100.00% | ✅ |

### **What These Mean**
- **Accuracy:** 989 out of 1000 predictions correct
- **AUC:** Perfect discrimination between tsunami/no-tsunami
- **Recall:** Detects 97% of actual tsunamis (minimizes misses)
- **Precision:** 0 false alarms (100% alert reliability)

---

## 🚀 How to Train Your Model

### **Option 1: Google Colab (Recommended)**
```bash
# 1. Open the notebook
notebooks/Train_Tsunami_Binary_Focal_Loss_Kaggle.ipynb

# 2. Set runtime to GPU
# Runtime → Change runtime type → GPU

# 3. Run all cells
# Runtime → Run all
```

### **Option 2: Local Training**
```bash
# Prepare data
python scripts/prepare_data.py --sample --prepare

# Train model
python scripts/train_model.py \
  --epochs 50 \
  --batch-size 32 \
  --data-dir data/raw \
  --output-dir models
```

### **Option 3: Python Script**
```python
from src.models import TsunamiPredictionBinaryModel, DataPreprocessor
from src.utils import load_config
import numpy as np

# Load configuration
config = load_config('config/config.yaml')

# Initialize model
model = TsunamiPredictionBinaryModel(config)

# Build architecture
model.build_model(input_shape=(24, 32))

# Prepare data
preprocessor = DataPreprocessor(config)
X_train = preprocessor.preprocess_combined_data(...)
y_train = np.array([...])

# Train
model.train(X_train, y_train, epochs=50, batch_size=32)

# Save
model.save_model('models/tsunami_detection_binary_focal.keras')
```

---

## 📊 Training Data

### **Sources**
- NOAA Global Historical Tsunami Database
- USGS Earthquake Catalog
- Historical ocean observations

### **Dataset Composition**
- **Total samples:** ~1000-5000 events
- **Tsunami events:** ~50-200 (5% positive)
- **Non-tsunami events:** ~950-4800 (95% negative)
- **Time period:** 2000-present (historical + recent)

### **Class Imbalance Problem**
The problem: Only 5% of earthquakes cause tsunamis!

The solution: **Focal Loss**
```python
# Standard cross-entropy treats all examples equally
# Focal loss focuses on hard-to-classify examples
# This prevents the model from ignoring rare tsunami patterns

def focal_loss(gamma=2.0, alpha=0.25):
    """Focal loss for class imbalance"""
    # Down-weights easy negatives
    # Emphasizes hard positives
    # Achieves 100% precision with 97% recall
```

---

## 🧪 Testing Checklist

- [ ] Model architecture builds without errors
- [ ] Model accepts correct input shapes
- [ ] Forward pass produces (batch_size, 1) outputs
- [ ] Training loss decreases over epochs
- [ ] Validation accuracy improves
- [ ] Model saves and loads correctly
- [ ] Inference produces values in [0, 1]
- [ ] Inference speed < 200ms per sample
- [ ] Model generalizes to new data

---

## 🔗 Integration Points

**Input from IoT Team:**
- Earthquake features (magnitude, depth, lat, lon)
- Ocean features (sea level, wave height, period)
- Bathymetry data (ocean floor topography)

**Output to Website Team:**
- Risk probability (0-1)
- Confidence score (0-1)
- Risk classification (high/medium/low/none)

---

## 📝 Configuration

Edit model settings in `config/config.yaml`:
```yaml
model:
  architecture:
    cnn_filters: [32, 64]
    lstm_units: [128, 64]
    dense_units: [128, 64, 32]
    dropout_rate: 0.3
    
  training:
    batch_size: 32
    epochs: 50
    learning_rate: 0.0005
    early_stopping_patience: 15
    
  thresholds:
    high_risk: 0.75
    medium_risk: 0.50
    low_risk: 0.25
```

---

## 🎓 Learning Resources

### **CNN-LSTM Architecture**
- https://keras.io/examples/timeseries/lstm_forecast_multistep/
- Understanding CNN: https://colah.github.io/posts/2014-07-Conv-Nets-Overview/
- Understanding LSTM: https://colah.github.io/posts/2015-08-Understanding-LSTMs/

### **Focal Loss**
- Paper: https://arxiv.org/abs/1708.02002
- Implementation: Explained in src/models/cnn_lstm_binary_model.py

### **Class Imbalance Handling**
- Techniques: https://machinelearningmastery.com/imbalanced-classification-with-python/

---

## 🐛 Troubleshooting

**Model Not Training:**
- Check input data shapes
- Verify data preprocessing
- Check loss function values
- Review GPU memory availability

**Poor Performance:**
- Increase training epochs
- Adjust learning rate
- Modify architecture (add/remove layers)
- Verify training data quality
- Check class balance

**Inference Issues:**
- Verify input preprocessing matches training
- Check model loading errors
- Ensure feature scaling is consistent

---

## 🚀 Next Steps

1. Train model on full dataset (1000+ samples)
2. Implement hyperparameter tuning
3. Test with unseen earthquake/ocean data
4. Optimize for production inference
5. Document training procedure
6. Version control trained models
7. Monitor performance on new data

---

**Your model's predictions power the entire tsunami warning system!** 🤖🌊
