# 📋 Model Team Assignment Card

**Team Name:** Deep Learning & AI  
**Your Role:** Tsunami Risk Prediction Engine  
**Start Here:** `team_model/README.md`

---

## ✨ Your Unique Value

You're the **brain** of the system. Your model turns raw data into life-saving predictions.

---

## 📦 Your Deliverables

### Phase 1: Architecture & Training (Week 1-2)
- [ ] Understand CNN-LSTM architecture
- [ ] Prepare training dataset (1000+ samples)
- [ ] Implement Focal Loss for class imbalance
- [ ] Train model on GPU (Colab recommended)
- [ ] Achieve >98% validation accuracy

### Phase 2: Optimization (Week 2-3)
- [ ] Optimize for CPU inference
- [ ] Achieve <200ms prediction time
- [ ] Test on new unseen data
- [ ] Implement confidence scoring
- [ ] Generate model metadata

### Phase 3: Integration (Week 3-4)
- [ ] Save model in Keras format
- [ ] Create inference pipeline
- [ ] Test with Website Team data format
- [ ] Performance profiling
- [ ] Documentation & examples

---

## 📊 Success Metrics

```
Metric                  Target          Status
─────────────────────────────────────────────
Training Accuracy       > 98%           ⭕
Validation Accuracy     > 98%           ⭕
Precision               100%            ⭕
Recall                  > 95%           ⭕
Inference Time (CPU)    < 200ms         ⭕
Model Size              < 5 MB          ⭕
AUC-ROC                 > 0.95          ⭕
```

---

## 🔧 Core Files to Modify

```
src/models/
├── cnn_lstm_binary_model.py   ← Model architecture (EDIT THIS)
├── data_preprocessor.py        ← Data normalization
└── model_trainer.py            ← Training loop

models/
└── tsunami_detection_binary_focal.keras  ← Your trained model

scripts/
└── train_model.py              ← Command-line training
```

---

## 🚀 Quick Start

### **Option 1: Google Colab (Recommended)**
```
1. Open notebook:
   notebooks/Train_Tsunami_Binary_Focal_Loss_Kaggle.ipynb
   
2. In Colab:
   Runtime → Change runtime type → GPU
   
3. Run all cells
   Runtime → Run all
   
4. Download trained model:
   tsunami_detection_binary_focal.keras
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
  --output-dir models/
```

---

## 📊 Model Architecture

```
Input Shape: (batch_size, 24, 32)
       ↓
CNN Block 1:
  Conv2D(32, 3x3) 
  → MaxPooling(2x2) 
  → Dropout(0.3)
       ↓
CNN Block 2:
  Conv2D(64, 3x3) 
  → MaxPooling(2x2) 
  → Dropout(0.3)
       ↓
LSTM Block 1:
  LSTM(128, return_seq=True)
  → Dropout(0.3)
       ↓
LSTM Block 2:
  LSTM(64, return_seq=False)
  → Dropout(0.3)
       ↓
Dense 1: Dense(128, relu) → Dropout(0.3)
Dense 2: Dense(64, relu) → Dropout(0.2)
Dense 3: Dense(32, relu)
       ↓
Output: Dense(1, sigmoid)
       ↓
Risk Probability [0-1]

Total Parameters: 185,729
Model Size: 2.3 MB
```

---

## 🔗 Integration Points

**Input from IoT Team:**
```json
{
  "earthquake": {
    "magnitude": 7.5,
    "depth_km": 30,
    "latitude": 8.5,
    "longitude": 93.2
  },
  "ocean": {
    "tide_anomaly": 0.45,
    "wave_height": 2.3,
    "wave_period": 12.5
  }
}
```

**Output to Website Team:**
```json
{
  "risk_probability": 0.85,
  "confidence": 0.92,
  "prediction": 1,
  "inference_time_ms": 145
}
```

---

## 🎯 Weekly Checklist

**Week 1:**
- [ ] Read team documentation
- [ ] Understand CNN-LSTM architecture
- [ ] Review Focal Loss concept
- [ ] Set up training environment

**Week 2:**
- [ ] Prepare and validate dataset
- [ ] Build model architecture
- [ ] Implement training loop
- [ ] Train model and log metrics

**Week 3:**
- [ ] Achieve >98% accuracy
- [ ] Optimize for inference speed
- [ ] Save and test model loading
- [ ] Generate confidence scores

**Week 4:**
- [ ] Profile on CPU
- [ ] Test with Website Team
- [ ] Complete documentation
- [ ] Prepare for deployment

---

## 📚 Learning Resources

### **CNN-LSTM Understanding:**
- https://keras.io/examples/timeseries/lstm_forecast_multistep/
- https://colah.github.io/posts/2014-07-Conv-Nets-Overview/
- https://colah.github.io/posts/2015-08-Understanding-LSTMs/

### **Class Imbalance & Focal Loss:**
- Paper: https://arxiv.org/abs/1708.02002
- https://machinelearningmastery.com/imbalanced-classification-with-python/

### **TensorFlow/Keras:**
- https://tensorflow.org/tutorials
- https://keras.io/api/

---

## 🎓 Training Data Details

### **Data Sources**
- NOAA Global Historical Tsunami Database
- USGS Earthquake Catalog (2000-present)
- GEBCO Bathymetry Database

### **Dataset Composition**
```
Total Samples:      ~1000-5000
Tsunami Events:     ~50-200   (5% positive class)
Non-Tsunami:        ~950-4800 (95% negative class)

Class Imbalance Challenge:
  ├─ Problem: Only 5% are actual tsunamis
  ├─ Solution: Focal Loss
  └─ Result: 100% precision, 97% recall
```

### **Feature Engineering**
```
From earthquake data:
  • Magnitude (5.5-9.5)
  • Depth (0-700 km)
  • Location (lat/lon in Indian Ocean)
  • Time (for temporal patterns)

From ocean data:
  • Sea level anomalies
  • Wave height
  • Wave period
  
From bathymetry:
  • Ocean depth
  • Distance to coast
  • Seafloor topology
```

---

## ⚠️ Common Challenges

**Challenge:** Class imbalance (5% positive)  
**Solution:** Focal Loss with gamma=2.0, alpha=0.25

**Challenge:** Model overfitting  
**Solution:** Dropout layers, early stopping, regularization

**Challenge:** Slow inference  
**Solution:** Reduce model size, quantization, optimize architecture

**Challenge:** Poor CPU performance  
**Solution:** Profile inference, optimize data loading, batch normalization

---

## 💡 Pro Tips

1. **Use Focal Loss** - Critical for imbalanced data
2. **Add confidence scores** - Don't just predict class
3. **Profile early** - Check inference time on CPU
4. **Save model metadata** - Document performance metrics
5. **Test generalization** - Validate on held-out test set
6. **Implement batch processing** - Speed up inference

---

## 🧪 Testing Checklist

- [ ] Model builds without errors
- [ ] Accepts correct input shapes
- [ ] Training loss decreases
- [ ] Validation accuracy improves
- [ ] Achieves >98% accuracy
- [ ] Inference produces values in [0,1]
- [ ] CPU inference <200ms
- [ ] Model saves and loads correctly
- [ ] Generalizes to new data
- [ ] Confidence scores are meaningful

---

**Your model's predictions save lives. Make them count!** 🤖🌊
