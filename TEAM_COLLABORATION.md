# 🌊 Team Collaboration Guide - Full Project Structure

## 📋 Project Overview

The **India-specific Tsunami Early Warning System** is a real-time monitoring system that:
1. **Collects** data from 5 real-time APIs (IoT Team)
2. **Predicts** tsunami risk using deep learning (Model Team)  
3. **Displays** results via web interface (Website Team)

---

## 👥 Three-Team Structure

### **Team IoT** 🌐 (Data Collection)
**Responsibility:** Fetch and validate real-time earthquake, ocean, and advisory data

**Files:** `src/data_collection/`, `scripts/prepare_data.py`

**Key Technologies:** USGS API, NOAA APIs, INCOIS API, Data validation

**Output:** Clean, validated earthquake/ocean/advisory data

**README:** `team_iot/README.md`

---

### **Team Model** 🤖 (Deep Learning)
**Responsibility:** Build and train CNN-LSTM that predicts tsunami probability

**Files:** `src/models/`, `notebooks/`, `scripts/train_model.py`

**Key Technologies:** TensorFlow, Keras, Focal Loss, CNN-LSTM architecture

**Input:** IoT team data

**Output:** Risk probability (0-1), confidence score

**Performance:** 98.9% accuracy, 100% precision, <200ms inference

**README:** `team_model/README.md`

---

### **Team Website** 🌐 (Web Application)
**Responsibility:** Build REST API, web dashboard, alert system, and deployment

**Files:** `src/web_app/`, `src/filtering/`, `static/`, `deployment/`

**Key Technologies:** Flask, Docker, REST API, Web dashboard

**Input:** IoT data + Model predictions

**Output:** User alerts, web dashboard, REST API

**README:** `team_website/README.md`

---

## 📁 Complete File Structure

```
India-specific-tsunami-early-warning-system/
│
├── 📁 src/                          (Core application code)
│   ├── __init__.py
│   ├── inference_engine.py          ← Orchestrates workflow
│   ├── 📁 data_collection/          ← IoT TEAM OWNS
│   │   ├── usgs_collector.py
│   │   ├── noaa_tides_collector.py
│   │   ├── noaa_buoys_collector.py
│   │   ├── incois_collector.py
│   │   └── bathymetry_loader.py
│   ├── 📁 models/                   ← MODEL TEAM OWNS
│   │   ├── cnn_lstm_binary_model.py
│   │   ├── data_preprocessor.py
│   │   ├── model_trainer.py
│   │   └── __init__.py
│   ├── 📁 filtering/                ← WEBSITE TEAM OWNS
│   │   ├── india_impact_filter.py
│   │   └── risk_assessor.py
│   ├── 📁 utils/                    (Shared utilities)
│   │   ├── config_loader.py
│   │   ├── data_helpers.py
│   │   ├── logger.py
│   │   └── __init__.py
│   └── 📁 web_app/                  ← WEBSITE TEAM OWNS
│       ├── app.py
│       ├── api_routes.py
│       ├── web_routes.py
│       └── __init__.py
│
├── 📁 team_iot/                     (IoT Team workspace)
│   └── README.md                    ← Data Collection overview
│
├── 📁 team_model/                   (Model Team workspace)
│   └── README.md                    ← Deep Learning overview
│
├── 📁 team_website/                 (Website Team workspace)
│   └── README.md                    ← Web Application overview
│
├── 📁 models/                       ← Trained model files
│   ├── tsunami_detection_binary_focal.keras
│   └── model_metadata.json
│
├── 📁 static/                       ← Website frontend
│   └── index_live.html
│
├── 📁 config/
│   └── config.yaml                  ← Configuration for all teams
│
├── 📁 deployment/                   ← Deployment configs
│   ├── Dockerfile
│   ├── Dockerfile.api
│   ├── docker-compose.yml
│   ├── docker-compose.api.yml
│   ├── Procfile
│   ├── railway.json
│   └── render.yaml
│
├── 📁 notebooks/                    ← Model training notebooks
│   └── Train_Tsunami_Binary_Focal_Loss_Kaggle.ipynb
│
├── 📁 scripts/                      ← Utility scripts
│   ├── train_model.py
│   ├── prepare_data.py
│   ├── check_health.py
│   ├── demo.py
│   ├── quick_test.py
│   ├── api_usage_examples.py
│   └── healthcheck.sh
│
├── 📁 docs/                         ← Documentation
│   ├── README.md
│   ├── API_EXAMPLES.md
│   ├── QUICKSTART.md
│   ├── DEPLOYMENT_GUIDE.md
│   └── TRAINING_GUIDE.md
│
├── 📁 data/                         ← Data storage
│
├── app.py                           ← Simple Flask entry
├── main.py                          ← Full app entry
├── requirements.txt                 ← Python dependencies
└── config.yaml                      ← Root configuration
```

---

## 🔄 Data Flow & Integration Points

```
┌─────────────────────────────────────────────────────────────┐
│                    SYSTEM ARCHITECTURE                       │
└─────────────────────────────────────────────────────────────┘

┌──────────────────┐
│  EXTERNAL APIs   │
├──────────────────┤
│ • USGS           │  Earthquakes
│ • NOAA Tides     │  Sea levels
│ • NOAA Buoys     │  Wave data
│ • INCOIS         │  Advisories
│ • GEBCO          │  Bathymetry
└────────┬─────────┘
         │
         ▼
    ┌─────────────────┐
    │   IOT TEAM      │◄── team_iot/README.md
    │ Data Collection │
    └────────┬────────┘
             │ Clean Data
             ▼
    ┌─────────────────┐
    │  MODEL TEAM     │◄── team_model/README.md
    │ CNN-LSTM Model  │
    │  (98.9% acc)    │
    └────────┬────────┘
             │ Risk Probability [0-1]
             ▼
    ┌─────────────────┐
    │  WEBSITE TEAM   │◄── team_website/README.md
    │ Web Application │
    │   REST API      │
    └────────┬────────┘
             │
         ┌───┴──────────┬────────────────┬──────────┐
         │              │                │          │
         ▼              ▼                ▼          ▼
    Web         REST       India       Alert
    Dashboard   API        Filtering   Generation
    (HTML)      (JSON)     (Geography) (Users)

```

---

## 🔗 How Teams Work Together

### **Team IoT → Team Model**
- **Input:** Raw earthquake, ocean, bathymetry data
- **Processing:** Cleaned, validated, normalized
- **Format:** `{"magnitude": 7.5, "depth": 30, ...}` 
- **Frequency:** Every 5 minutes

### **Team Model → Team Website**
- **Input:** Clean IoT data
- **Processing:** CNN-LSTM prediction + risk scoring
- **Output:** `{"risk_probability": 0.85, "confidence": 0.92}`
- **Latency:** <200ms per prediction

### **Team Website (Full Integration)**
- **Receives:** IoT data + Model predictions
- **Processes:** India impact filtering + risk assessment
- **Outputs:** User alerts, web dashboard, REST API
- **Users:** View real-time risk assessment

---

## 🎯 Getting Started by Team

### **If you're IoT Team:**
1. Read `team_iot/README.md`
2. Explore `src/data_collection/*.py` files
3. Test individual API collectors
4. Verify data quality and validation

### **If you're Model Team:**
1. Read `team_model/README.md`
2. Review `src/models/cnn_lstm_binary_model.py`
3. Study the architecture and loss function
4. Train model with `scripts/train_model.py`

### **If you're Website Team:**
1. Read `team_website/README.md`
2. Review `src/web_app/api_routes.py`
3. Study `src/filtering/india_impact_filter.py`
4. Run dashboard with `python main.py`

---

## 🤝 Collaboration Best Practices

### **Documentation**
- Each team has its own `team_*/README.md` file
- Update it with progress and discoveries
- Document any API changes or new features

### **Version Control**
```bash
# Always work on feature branches
git checkout -b feature/iot-usgs-improvement

# Commit with clear messages
git commit -m "IoT: Add retry logic to USGS API collector"

# Push to GitHub
git push origin feature/iot-usgs-improvement

# Open Pull Request for review
```

### **Testing**
- IoT Team: Test each API independently
- Model Team: Test with sample data
- Website Team: Test full integration

### **Communication**
- Shared file: `config/config.yaml` (coordinate changes)
- Shared file: `requirements.txt` (coordinate dependencies)
- Check Git log before pulling

---

## 📊 Key Metrics & Targets

| Aspect | Target | Measure |
|--------|--------|---------|
| **IoT Data** | All sources OK | 100% API success rate |
| **Model Accuracy** | High precision | 98%+ accuracy, 100% precision |
| **Inference Speed** | Fast | <200ms per prediction |
| **Website Response** | Responsive | API <500ms response time |
| **System Uptime** | Reliable | 99%+ availability |

---

## 🚀 Deployment Path

```
1. IoT Team validates all APIs ✓
2. Model Team trains and exports model ✓
3. Website Team integrates all components ✓
4. Push to GitHub ✓
5. Deploy to Railway/Render
6. Monitor in production
7. Handle alerts and feedback
```

---

## 📞 Quick Reference

### **Commands**
```bash
# Run dashboard
python main.py

# Run API only
python app.py

# Train model
python scripts/train_model.py

# Test system
python scripts/quick_test.py

# Check health
python scripts/check_health.py
```

### **Config File**
```bash
# Edit configuration for all teams
nano config/config.yaml
```

### **Logs**
```bash
# View application logs
tail -f logs/app.log

# View model training logs
tail -f logs/training.log
```

---

## 📝 Team README Files

- **IoT Team Details:** [team_iot/README.md](../team_iot/README.md)
- **Model Team Details:** [team_model/README.md](../team_model/README.md)
- **Website Team Details:** [team_website/README.md](../team_website/README.md)

---

## ✅ Success Criteria

Each team will know they're done when:

**IoT Team:**
- ✅ All 4 APIs return valid data
- ✅ Data validation catches errors
- ✅ Retry logic handles failures
- ✅ Performance <10 seconds total fetch time

**Model Team:**
- ✅ Model trains without errors
- ✅ Validation accuracy >98%
- ✅ Inference <200ms on CPU
- ✅ Model file saved and loadable

**Website Team:**
- ✅ Dashboard displays without errors
- ✅ All API endpoints functional
- ✅ India filtering works correctly
- ✅ Deployed to Railway/Render

---

## 🎓 Learning Resources

### **Shared Resources**
- [Project README](../README.md) - Full project overview
- [QUICKSTART.md](../docs/QUICKSTART.md) - Get running in 10 minutes
- [API_EXAMPLES.md](../docs/API_EXAMPLES.md) - API documentation
- [DEPLOYMENT_GUIDE.md](../docs/DEPLOYMENT_GUIDE.md) - Cloud deployment

### **Team-Specific Resources**
- **IoT:** API documentation links in `team_iot/README.md`
- **Model:** Neural network resources in `team_model/README.md`
- **Website:** Framework docs in `team_website/README.md`

---

**Together, your three teams build a life-saving tsunami warning system!** 🌊🚀
