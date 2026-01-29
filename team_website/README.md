# 🌐 Website Team - Web Application & API Component

## 🎨 Team Responsibility
Build the web application, REST API, and user interface that integrates all components and displays results to users.

## 👥 Team Members
- **Lead:** [Your Name]
- **Contributors:** [Team Members]

---

## 📋 Overview

The Website team creates the user-facing interface and backend API that orchestrates the entire tsunami warning system. We connect IoT data collection, AI model predictions, and risk assessment into a seamless application.

### **Key Deliverables:**
1. **Web Dashboard** - Real-time visual interface
2. **REST API** - Programmatic access to system
3. **Integration Logic** - Workflow orchestration
4. **Risk Filtering** - India-specific threat assessment

---

## 🎯 Key Responsibilities

- ✅ Build interactive web dashboard
- ✅ Create REST API endpoints (10+)
- ✅ Integrate IoT data with model predictions
- ✅ Implement India-impact filtering
- ✅ Generate user-friendly alerts
- ✅ Handle real-time updates via WebSocket
- ✅ Manage error handling and logging
- ✅ Deploy to cloud platforms

---

## 📁 Project Files You Own

```
src/web_app/
├── app.py                     ← Flask application factory
├── api_routes.py              ← REST API endpoints
└── web_routes.py              ← Web page routes

src/filtering/
├── india_impact_filter.py     ← Geographic filtering logic
└── risk_assessor.py           ← Comprehensive risk assessment

src/inference_engine.py        ← Workflow orchestration

static/
└── index_live.html            ← Web dashboard

app.py                          ← Simple Flask entry point
main.py                         ← Full app entry point

deployment/
├── Dockerfile                 ← Container config
├── docker-compose.yml         ← Multi-service setup
├── Procfile                   ← Heroku deployment
├── railway.json               ← Railway deployment
└── render.yaml                ← Render deployment
```

---

## 🔧 Technologies Used

- **Flask** - Python web framework
- **Flask-CORS** - Cross-origin support
- **Flask-SocketIO** - Real-time WebSocket
- **Jinja2** - Template rendering
- **HTML/CSS/JavaScript** - Frontend
- **Docker** - Containerization
- **Gunicorn** - Production server

---

## 📊 API Endpoints

### **System Monitoring**
```bash
GET /health
# Returns: {"status": "healthy", "model_loaded": true}

GET /api/status
# Returns: System status, monitoring state, last check time

GET /api/current-assessment
# Returns: Latest risk assessment
```

### **Manual Control**
```bash
POST /api/run-check
# Triggers: Immediate tsunami check

POST /api/monitoring/start
# Request: {"interval_seconds": 300}
# Starts: Continuous background monitoring

POST /api/monitoring/stop
# Stops: Background monitoring
```

### **Data Access**
```bash
GET /api/earthquake/recent?hours=24&min_magnitude=6.0
# Returns: Recent earthquakes from IoT team

GET /api/ocean/conditions
# Returns: Current tide and buoy data

GET /api/advisories/incois
# Returns: Official INCOIS advisories

GET /api/model/info
# Returns: Model metadata and performance
```

---

## 🌐 Web Dashboard Features

### **Real-time Display:**
- ✅ Current risk level (color-coded)
- ✅ Risk score and confidence
- ✅ Recent earthquake information
- ✅ Affected coastal regions
- ✅ Estimated arrival times
- ✅ Safety recommendations
- ✅ Alert history

### **Map Visualization:**
- Earthquake epicenter locations
- Indian coastline highlighting
- Wave propagation paths
- Risk zones

### **Data Refresh:**
- Auto-refresh every 30 seconds
- WebSocket for real-time updates
- User-triggered refresh

---

## 🚀 How to Run Your Component

### **Development Mode**
```bash
# Install dependencies
pip install -r requirements.txt

# Run Flask app
python main.py --debug

# Access at http://localhost:5000
```

### **Production Mode**
```bash
# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 main:app

# Or use Docker
docker build -f deployment/Dockerfile -t tsunami-warning .
docker run -p 5000:5000 tsunami-warning
```

### **Docker Compose**
```bash
cd deployment
docker-compose up

# Access at http://localhost:5000
```

---

## 📈 API Response Examples

### **GET /api/current-assessment**
```json
{
  "success": true,
  "data": {
    "assessment_id": "TSUNAMI_20260129_100000",
    "timestamp": "2026-01-29T10:00:00",
    "alert_level": "WARNING",
    "india_at_risk": true,
    "india_risk_score": 0.85,
    "model_confidence": 0.92,
    "earthquake_info": {
      "magnitude": 7.8,
      "depth_km": 30,
      "location": {
        "latitude": 10.5,
        "longitude": 95.3
      },
      "time": "2026-01-29T09:45:00",
      "place": "Andaman Sea"
    },
    "affected_regions": ["west_coast", "andaman_nicobar"],
    "estimated_arrival_times": {
      "west_coast": "02:30 UTC",
      "east_coast": "04:15 UTC",
      "andaman_nicobar": "01:45 UTC"
    },
    "alert_message": "⚠️ TSUNAMI WARNING for Indian coast",
    "recommendations": [
      "Evacuate coastal areas immediately",
      "Move to higher ground",
      "Follow official instructions"
    ]
  }
}
```

---

## 🔗 Component Integration

### **Workflow**
```
1. IoT Team collects data
   ↓
2. Website receives data
   ↓
3. Model Team predicts risk
   ↓
4. Website applies India filter
   ↓
5. Website displays to users
```

### **Data Flow**
```
USGS API → Earthquake Collector → Preprocessor → Model
NOAA Tides → Tides Collector → Preprocessor → Model
NOAA Buoys → Buoys Collector → Preprocessor → Model
    ↓
    Model predicts risk
    ↓
    India Impact Filter assesses if India at risk
    ↓
    Risk Assessor generates alert
    ↓
    Website displays dashboard & API
    ↓
    Users see alerts and assessments
```

---

## 🧪 Testing Checklist

- [ ] All endpoints return valid JSON
- [ ] Dashboard loads without errors
- [ ] Real-time updates work (WebSocket)
- [ ] API responses have correct status codes
- [ ] Error handling works for API failures
- [ ] Model predictions integrate correctly
- [ ] India filtering works (no false positives)
- [ ] Alerts format correctly
- [ ] Database/caching works
- [ ] Docker build succeeds
- [ ] Health check endpoint responds

---

## 📝 Configuration

Edit deployment settings in `config/config.yaml`:
```yaml
system:
  inference_interval_seconds: 300  # Check every 5 minutes
  api_timeout_seconds: 30
  log_level: "INFO"

dashboard:
  refresh_interval_ms: 30000  # 30 seconds
  max_events_display: 50
  map_center: [12.0, 80.0]  # India center
  map_zoom: 5

alerts:
  levels:
    critical:
      threshold: 0.75
      color: "#FF0000"
```

---

## 🎓 Frontend Technologies

### **HTML/CSS/JavaScript**
- Bootstrap 5 for responsive design
- Chart.js for visualization
- Leaflet.js for maps
- Socket.io for real-time updates

### **Backend Stack**
- Flask routing and views
- Jinja2 templating
- JSON serialization
- Error middleware

---

## 🐛 Troubleshooting

**API Connection Issues:**
- Check Flask server is running
- Verify port 5000 is available
- Check firewall settings
- Verify CORS configuration

**Dashboard Not Updating:**
- Check WebSocket connection
- Verify JavaScript console for errors
- Check network requests in browser dev tools
- Verify server is sending updates

**Model Integration Issues:**
- Check model file exists at `models/tsunami_detection_binary_focal.keras`
- Verify model loads without errors
- Check input data format matches model expectations
- Review inference output format

**Deployment Issues:**
- Check Docker build logs
- Verify environment variables
- Check port mappings
- Review deployment logs

---

## 🚀 Deployment Options

### **Option 1: Railway (Recommended)**
```bash
# Push to GitHub
git push origin main

# Railway auto-deploys from deployment/railway.json
# Available at: https://your-app.railway.app
```

### **Option 2: Render**
```bash
# Push to GitHub
# Render auto-detects deployment/render.yaml
# Available at: https://tsunami-warning.onrender.com
```

### **Option 3: Docker Local**
```bash
docker build -f deployment/Dockerfile -t tsunami-warning .
docker run -p 5000:5000 tsunami-warning
```

---

## 📚 Code Examples

### **Starting Monitoring**
```python
@api_bp.route('/monitoring/start', methods=['POST'])
def start_monitoring():
    data = request.get_json() or {}
    interval = data.get('interval_seconds', 300)
    
    engine = get_inference_engine()
    engine.start_monitoring(interval_seconds=interval)
    
    return jsonify({
        'success': True,
        'message': f'Monitoring started with {interval}s interval'
    }), 200
```

### **Filtering for India Risk**
```python
# In india_impact_filter.py
def assess_india_risk(self, earthquake_data, model_prediction):
    # 1. Check model detected risk
    # 2. Evaluate location threat (critical zones)
    # 3. Calculate distance to coast
    # 4. Analyze wave propagation
    # 5. Return India-specific risk assessment
```

---

## 🔐 Security Considerations

- [ ] Validate all API inputs
- [ ] Implement rate limiting
- [ ] Add CORS restrictions in production
- [ ] Use HTTPS in production
- [ ] Sanitize HTML output
- [ ] Log all access attempts
- [ ] Monitor for DDoS attacks

---

## 🎯 Next Steps

1. Build responsive dashboard UI
2. Implement WebSocket for real-time updates
3. Add historical data visualization
4. Create mobile-friendly version
5. Implement user authentication (optional)
6. Add SMS/email alerting (optional)
7. Create admin dashboard for monitoring
8. Deploy to production

---

**Your website brings the entire system to life for users!** 🌐✨
