# 📋 IoT Team Assignment Card

**Team Name:** IoT Data Collection  
**Your Role:** Real-time Sensor Data Integration  
**Start Here:** `team_iot/README.md`

---

## ✨ Your Unique Value

You're the **eyes and ears** of the system. Without you, there's no data to predict on.

---

## 📦 Your Deliverables

### Phase 1: API Integration (Week 1-2)
- [ ] USGS Earthquake API fetching & caching
- [ ] NOAA Tides API integration
- [ ] NOAA Buoys API integration
- [ ] INCOIS Advisory API integration
- [ ] GEBCO Bathymetry data loading

### Phase 2: Data Quality (Week 2-3)
- [ ] Data validation for all sources
- [ ] Error handling and retry logic
- [ ] Missing value handling
- [ ] Data consistency checks
- [ ] Logging and monitoring

### Phase 3: Integration (Week 3-4)
- [ ] Pass data to Model Team format
- [ ] Cache data efficiently
- [ ] Implement 5-minute collection cycle
- [ ] Performance testing
- [ ] Documentation

---

## 📊 Success Metrics

```
Metric                  Target          Status
─────────────────────────────────────────────
USGS Fetch Time        < 2 seconds      ⭕
NOAA Tides Fetch       < 3 seconds      ⭕
NOAA Buoys Fetch       < 3 seconds      ⭕
INCOIS Fetch           < 2 seconds      ⭕
Data Validation        100%             ⭕
Total Cycle Time       < 10 seconds     ⭕
API Success Rate       > 99%            ⭕
```

---

## 🔧 Core Files to Modify

```
src/data_collection/
├── usgs_collector.py          ← USGS earthquake data
├── noaa_tides_collector.py    ← NOAA tide gauges
├── noaa_buoys_collector.py    ← Wave height & period
├── incois_collector.py        ← Official advisories
└── bathymetry_loader.py       ← Ocean floor depth
```

---

## 🚀 Quick Start

```bash
# Test your USGS collector
python -c "
from src.data_collection import USGSEarthquakeCollector
import yaml
config = yaml.safe_load(open('config/config.yaml'))
collector = USGSEarthquakeCollector(config)
quakes = collector.fetch_recent_earthquakes(hours=24)
print(f'✅ Found {len(quakes)} earthquakes')
"

# Test all collectors
python scripts/prepare_data.py --test-apis
```

---

## 📚 API Documentation Links

- **USGS:** https://earthquake.usgs.gov/fdsnws/event/1/
- **NOAA Tides:** https://api.tidesandcurrents.noaa.gov/api/prod/
- **NOAA NDBC:** https://www.ndbc.noaa.gov/
- **INCOIS:** https://incois.gov.in/
- **GEBCO:** https://www.gebco.net/

---

## 🔗 Integration Points

**Your Output → Model Team Input:**
```json
{
  "earthquake": {
    "magnitude": 7.5,
    "depth_km": 30,
    "latitude": 8.5,
    "longitude": 93.2,
    "time": "2026-01-29T10:00:00Z"
  },
  "ocean": {
    "tide_anomaly": 0.45,
    "wave_height": 2.3,
    "wave_period": 12.5
  },
  "bathymetry": {
    "ocean_depth": [4200, 4100, 3900]
  }
}
```

---

## 🎯 Weekly Checklist

**Week 1:**
- [ ] Read team documentation
- [ ] Set up development environment
- [ ] Test each API individually
- [ ] Create data validation tests

**Week 2:**
- [ ] Implement error handling
- [ ] Add retry logic
- [ ] Implement caching
- [ ] Handle missing data

**Week 3:**
- [ ] Optimize performance
- [ ] Add comprehensive logging
- [ ] Test with Model Team
- [ ] Write documentation

**Week 4:**
- [ ] Final integration testing
- [ ] Performance tuning
- [ ] Code review
- [ ] Deployment preparation

---

## ⚠️ Common Challenges

**Challenge:** API rate limits  
**Solution:** Implement caching with TTL (time-to-live)

**Challenge:** API downtime  
**Solution:** Add fallback data and retry logic

**Challenge:** Network timeouts  
**Solution:** Implement connection timeouts and graceful degradation

**Challenge:** Data format inconsistencies  
**Solution:** Normalize all data to consistent format

---

## 💡 Pro Tips

1. **Cache everything** - Don't hammer APIs repeatedly
2. **Add timestamps** - Track when data was fetched
3. **Validate early** - Catch bad data before it reaches the model
4. **Log extensively** - Help debug issues in production
5. **Test offline** - Create mock API responses for testing

---

## 🎓 Learning Path

1. Read USGS API documentation (1 day)
2. Implement USGSEarthquakeCollector (1-2 days)
3. Test USGS integration thoroughly (1 day)
4. Repeat for NOAA Tides (3 days)
5. Repeat for NOAA Buoys (3 days)
6. Repeat for INCOIS (2 days)
7. Implement validation & error handling (2 days)
8. Performance optimization (1-2 days)

---

**You're building the foundation that makes everything else possible!** 🌊📡
