# 📋 Website Team Assignment Card

**Team Name:** Web Application & API  
**Your Role:** User Interface & System Integration  
**Start Here:** `team_website/README.md`

---

## ✨ Your Unique Value

You're the **communicator** of the system. You bring IoT data and AI predictions to real users.

---

## 📦 Your Deliverables

### Phase 1: REST API (Week 1-2)
- [ ] Build 10+ REST endpoints
- [ ] Implement data serialization
- [ ] Add error handling & logging
- [ ] Integrate with Model Team
- [ ] Test all endpoints

### Phase 2: Dashboard UI (Week 2-3)
- [ ] Build responsive web dashboard
- [ ] Real-time data visualization
- [ ] Interactive map of Indian coast
- [ ] Alert notifications
- [ ] System status display

### Phase 3: Integration & Filtering (Week 3-4)
- [ ] Implement India-impact filtering
- [ ] Generate user-friendly alerts
- [ ] Manage alert levels & messages
- [ ] Deploy to Railway/Render
- [ ] Monitor production

---

## 📊 Success Metrics

```
Metric                  Target          Status
─────────────────────────────────────────────
API Response Time       < 500ms         ⭕
Dashboard Load Time     < 2 seconds     ⭕
Endpoint Availability   > 99.9%         ⭕
Real-time Updates       < 30 sec        ⭕
Zero False Alarms       100%            ⭕
Alert Accuracy          100%            ⭕
User Experience        ⭐⭐⭐⭐⭐        ⭕
```

---

## 🔧 Core Files to Modify

```
src/web_app/
├── app.py                   ← Flask app factory
├── api_routes.py            ← REST endpoints (EDIT THIS)
└── web_routes.py            ← Web pages

src/filtering/
├── india_impact_filter.py   ← Geographic logic (EDIT THIS)
└── risk_assessor.py         ← Alert generation

static/
└── index_live.html          ← Dashboard (EDIT THIS)

deployment/
├── Dockerfile               ← Container config
├── docker-compose.yml       ← Multi-service
├── railway.json             ← Railway deployment
└── render.yaml              ← Render deployment
```

---

## 🚀 Quick Start

### **Run Locally**
```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python main.py

# Access at http://localhost:5000
```

### **Run in Docker**
```bash
cd deployment
docker-compose up

# Access at http://localhost:5000
```

---

## 📊 API Endpoints You'll Create

```
GET /health
  → System status

GET /api/status
  → Current monitoring state

POST /api/run-check
  → Trigger immediate tsunami check

POST /api/monitoring/start
  → Start background monitoring

POST /api/monitoring/stop
  → Stop background monitoring

GET /api/current-assessment
  → Latest risk assessment ⭐ MOST IMPORTANT

GET /api/earthquake/recent
  → Recent earthquakes

GET /api/ocean/conditions
  → Current ocean state

GET /api/advisories/incois
  → Official advisories

GET /api/model/info
  → Model metadata
```

---

## 🌐 Dashboard Features

### **Real-time Display:**
- ✅ Current risk level (🟢 NONE / 🟡 WATCH / 🟠 ADVISORY / 🔴 WARNING)
- ✅ Risk score (0-100%)
- ✅ Model confidence
- ✅ Recent earthquakes
- ✅ Affected regions
- ✅ ETA to Indian coast
- ✅ Safety recommendations

### **Visualizations:**
- Interactive map of Indian Ocean
- Earthquake epicenter markers
- Coastline highlighting
- Wave propagation paths
- Risk zones colored by threat level

### **Real-time Updates:**
- Auto-refresh every 30 seconds
- WebSocket for live updates
- User-triggered refresh button

---

## 🔗 Integration Points

**Input from IoT Team:**
```json
{
  "earthquake": {
    "magnitude": 7.5,
    "depth": 30,
    "location": "Andaman Sea",
    "time": "2026-01-29T10:00:00Z"
  },
  "ocean_conditions": {
    "tide_anomaly": 0.45,
    "wave_height": 2.3
  }
}
```

**Input from Model Team:**
```json
{
  "risk_probability": 0.85,
  "confidence": 0.92,
  "classification": 1
}
```

**Output to Users:**
```json
{
  "alert_level": "WARNING",
  "risk_score": 85,
  "message": "⚠️ TSUNAMI WARNING for Indian coast",
  "affected_regions": ["West Coast", "Andaman & Nicobar"],
  "eta_minutes": 150,
  "recommendations": [...]
}
```

---

## 🎯 Weekly Checklist

**Week 1:**
- [ ] Read team documentation
- [ ] Set up Flask development environment
- [ ] Create basic API structure
- [ ] Implement /health endpoint
- [ ] Test locally

**Week 2:**
- [ ] Implement 10+ REST endpoints
- [ ] Connect to Model Team
- [ ] Connect to IoT Team
- [ ] Test all integrations
- [ ] Add error handling

**Week 3:**
- [ ] Build dashboard HTML/CSS
- [ ] Implement real-time updates
- [ ] Create alert system
- [ ] Add India filtering logic
- [ ] Test full system

**Week 4:**
- [ ] Deploy to Railway/Render
- [ ] Monitor production
- [ ] Performance optimization
- [ ] Final documentation
- [ ] Team presentation

---

## 📈 API Response Examples

### **GET /api/current-assessment (Most Important)**
```json
{
  "success": true,
  "data": {
    "assessment_id": "TSUNAMI_20260129_100000",
    "timestamp": "2026-01-29T10:00:00Z",
    "alert_level": "WARNING",
    "india_at_risk": true,
    "risk_score": 85,
    "confidence": 0.92,
    "earthquake_info": {
      "magnitude": 7.8,
      "depth_km": 30,
      "location": "Andaman Sea",
      "time": "2026-01-29T09:45:00Z"
    },
    "affected_regions": [
      "West Coast",
      "Andaman & Nicobar Islands",
      "Lakshadweep"
    ],
    "estimated_arrival_minutes": {
      "west_coast": 150,
      "east_coast": 255,
      "andaman_nicobar": 105
    },
    "alert_message": "⚠️ TSUNAMI WARNING for Indian coast",
    "recommendations": [
      "Evacuate coastal areas immediately",
      "Move to higher ground (minimum 30 meters)",
      "Follow official evacuation instructions",
      "Remain on high ground for at least 2 hours"
    ]
  }
}
```

---

## 🗺️ India Impact Filter Logic

```python
def assess_india_risk(earthquake, model_prediction):
    # 1. Check model detected risk
    if model_prediction < 0.5:
        return {"india_at_risk": False}
    
    # 2. Check if in Indian Ocean
    if not in_indian_ocean(earthquake):
        return {"india_at_risk": False}
    
    # 3. Analyze distance to coast
    distance = calculate_distance_to_coast(earthquake)
    if distance > 5000:
        return {"india_at_risk": False}
    
    # 4. Check critical zones
    zones = get_critical_zones()
    affected = get_affected_zones(earthquake, zones)
    
    # 5. Calculate ETA
    etas = calculate_wave_etas(earthquake, affected)
    
    # 6. Return assessment
    return {
        "india_at_risk": True,
        "affected_regions": affected,
        "estimated_arrival_times": etas,
        "risk_score": model_prediction * 100
    }
```

---

## 🌍 Critical Tsunami Zones in India

```
Zone 1: West Coast (Mumbai, Goa, Kerala)
Zone 2: East Coast (Chennai, Kolkata, Orissa)
Zone 3: Andaman & Nicobar Islands
Zone 4: Lakshadweep Islands
Zone 5: Gulf of Kutch
Zone 6: Bay of Bengal
Zone 7: Arabian Sea
Zone 8: Maldives-adjacent waters
```

---

## ⚠️ Common Challenges

**Challenge:** Real-time data updates  
**Solution:** WebSocket connection + background tasks

**Challenge:** Model integration timing  
**Solution:** Queue system for async predictions

**Challenge:** Alert accuracy  
**Solution:** India filtering + multiple validation checks

**Challenge:** Deployment configuration  
**Solution:** Environment variables for Railway/Render

---

## 💡 Pro Tips

1. **Cache API responses** - Reduce backend load
2. **Implement rate limiting** - Prevent abuse
3. **Add comprehensive logging** - Debug production issues
4. **Use environment variables** - For secrets & config
5. **Test with mock data** - Before real API integration
6. **Monitor performance** - Track response times

---

## 🧪 Testing Checklist

- [ ] All endpoints return valid JSON
- [ ] Dashboard loads without errors
- [ ] Real-time updates work (WebSocket)
- [ ] API responses have correct status codes
- [ ] Error handling works for API failures
- [ ] Model predictions integrate correctly
- [ ] India filtering works (no false alerts)
- [ ] Alerts format correctly
- [ ] Database/caching works
- [ ] Docker build succeeds
- [ ] Health check endpoint responds
- [ ] Deployed successfully to Railway/Render

---

## 🚀 Deployment Commands

### **Railway**
```bash
# Push to GitHub
git push origin main

# Railway auto-deploys
# Available at: https://your-app.railway.app
```

### **Render**
```bash
# Push to GitHub
# Render detects deployment/render.yaml
# Available at: https://tsunami-warning.onrender.com
```

### **Docker Local**
```bash
docker build -f deployment/Dockerfile -t tsunami-warning .
docker run -p 5000:5000 tsunami-warning
```

---

**Your interface is how the world receives life-saving tsunami warnings!** 🌐🚀
