# Cloud Computing Laboratory & Theory Project Report
## Assignment 22: Smart City Traffic Monitoring System

---

**Course Title:** Cloud Computing (SA Assignment)  
**Assignment Number:** 22  
**Domain:** Transportation / Real-Time IoT Analytics  
**Submitted By:** **K M Rakshith Gowda**  
**Target Cloud Platform:** Amazon Web Services (AWS) — 100% Free Tier Architecture  
**Evaluation Breakdown:** 15 Total Marks (10 Marks Project Work & Report + 5 Marks Presentation/Demo)  

---

## Table of Contents
1. Executive Summary & Problem Statement
2. Project Objectives
3. Cloud System Architecture & Ingestion Flow
4. IoT Data Specification & Database Design
5. Automated Congestion Alert Engine
6. Real-Time Analytics Requirements
7. AWS Free Tier Deployment Guide
8. Testing Report & Verification Matrix
9. Deliverables & Evidence Screenshot Checklist
10. Challenges Faced & Lessons Learned
11. Conclusion & Future Enhancements
12. 3-Minute Demo Presentation Script

---

## 1. Executive Summary & Problem Statement

### 1.1 Problem Statement
Modern metropolitan cities experience rapid vehicular growth leading to severe road congestion, elevated carbon emissions, increased emergency response delays, and economic productivity losses. Traditional static traffic monitoring systems fail to provide instantaneous visibility or predictive insights required by municipal traffic authorities.

### 1.2 Proposed Solution
The **Smart City Traffic Monitoring System** is an event-driven, cloud-hosted IoT intelligence platform. It continuously ingests real-time telemetry from edge traffic sensors distributed across critical urban transit corridors, stores high-frequency time-series data, detects congestion bottlenecks instantly using automated threshold evaluation, and presents dynamic visual analytics via an interactive cloud dashboard.

---

## 2. Project Objectives

1. **IoT Sensor Simulation:** Emulate distributed road sensor nodes streaming multi-variable telemetry (Sensor ID, Vehicle Count, Average Speed, Road Occupancy %, and Timestamp) at high frequency.
2. **Cloud Backend Hosting:** Deploy a scalable ingestion pipeline and REST API on an AWS EC2 Free Tier Linux Virtual Machine (`t2.micro`).
3. **Time-Series Persistence:** Maintain time-stamped vehicular metrics using an InfluxDB-style time-series storage model.
4. **Automated Event-Driven Alerts:** Trigger high-priority congestion alerts whenever:
   $$\text{Vehicle Count} > 500 \quad \text{OR} \quad \text{Average Speed} < 15\text{ km/h}$$
5. **Real-Time Analytics & Geospatial Dashboard:** Provide real-time KPI metrics, interactive OpenStreetMap geospatial tracking with Leaflet.js, peak-hour analysis, hourly averages, and volume trend graphs.

---

## 3. Cloud System Architecture & Ingestion Flow

The application is structured into four cohesive layers adhering to standard cloud architecture patterns:

```
[ IoT Edge Layer ]
  - Sensor Node 1: MG Road (SENS-MGROAD-01)
  - Sensor Node 2: Central Silk Board (SENS-SILKBOARD-02)
  - Sensor Node 3: Outer Ring Road (SENS-ORR-03)
  - Sensor Node 4: Hebbal Flyover (SENS-HEBBAL-06)
  - Telemetry Generator (simulator.py)
         │
         ▼ (HTTP POST JSON Stream every 3 seconds)
[ AWS Cloud Infrastructure - Free Tier ]
  - Security Group (Firewall): Inbound Ports 22 (SSH), 5000 (HTTP)
  - AWS EC2 Linux VM (t2.micro):
      ├── Ingestion Gateway (POST /api/ingest)
      ├── Congestion Alert Engine (Count > 500 OR Speed < 15 km/h)
      ├── Time-Series Database (traffic_data.db / InfluxDB Model)
      ├── Analytics Aggregator (Hourly Means, Volume Trends, Peak Hours)
      └── Cloud Web Dashboard Server (Flask Engine on Port 5000)
         │
         ▼
[ Client & Operations Layer ]
  - Browser Access via Public IP: http://<EC2-Public-IP>:5000
  - Live OpenStreetMap Heat Map (Leaflet.js)
  - Time-Series Charts (Chart.js)
  - CSV Evidence Export Engine
```

---

## 4. IoT Data Specification & Database Design

### 4.1 IoT Telemetry Schema
Each smart sensor node transmits JSON payloads matching the assignment criteria:

| Field | Data Type | Description | Example Value |
| :--- | :--- | :--- | :--- |
| `sensor_id` | String | Unique hardware node identifier | `"SENS-SILKBOARD-02"` |
| `road_name` | String | Urban corridor designation | `"Central Silk Board Junction"` |
| `latitude` | Float | GPS latitude of the sensor | `12.9177` |
| `longitude` | Float | GPS longitude of the sensor | `77.6238` |
| `vehicle_count`| Integer | Detected vehicles in sampling window | `542` |
| `avg_speed` | Float | Mean vehicular speed (km/h) | `11.4` |
| `road_occupancy`| Float | Percentage of roadway occupied (%) | `88.5` |
| `timestamp` | Datetime | Telemetry capture timestamp | `"2026-11-14 19:35:10"` |

### 4.2 Database Schema (Time-Series Table)
```sql
CREATE TABLE sensor_readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sensor_id TEXT NOT NULL,
    road_name TEXT NOT NULL,
    latitude REAL,
    longitude REAL,
    vehicle_count INTEGER NOT NULL,
    avg_speed REAL NOT NULL,
    road_occupancy REAL NOT NULL,
    timestamp TEXT NOT NULL,
    is_congested INTEGER NOT NULL,
    alert_reason TEXT
);
```

### 4.3 Sample Ingested Records (Deliverable)
```json
[
  {
    "sensor_id": "SENS-SILKBOARD-02",
    "road_name": "Central Silk Board Junction",
    "vehicle_count": 560,
    "avg_speed": 10.8,
    "road_occupancy": 89.2,
    "timestamp": "2026-11-14 19:30:12",
    "is_congested": 1,
    "alert_reason": "Vehicle Count > 500 AND Speed < 15 km/h"
  },
  {
    "sensor_id": "SENS-AIRPORT-04",
    "road_name": "Airport Expressway",
    "vehicle_count": 190,
    "avg_speed": 68.5,
    "road_occupancy": 28.0,
    "timestamp": "2026-11-14 19:30:15",
    "is_congested": 0,
    "alert_reason": ""
  }
]
```

---

## 5. Automated Congestion Alert Engine

The assignment specifies the following business rules:

> **Congestion Trigger Condition:**
> * `Vehicle Count > 500` **OR**
> * `Average Speed < 15 km/h`

### Evaluation Logic (Python Implementation):
```python
is_congested = False
reasons = []

if vehicle_count > 500:
    reasons.append("Vehicle Count > 500")
    is_congested = True

if avg_speed < 15.0:
    reasons.append("Average Speed < 15 km/h")
    is_congested = True

alert_reason = " & ".join(reasons) if is_congested else ""
```

When triggered:
1. `is_congested = 1` is committed to the database.
2. The UI dashboard displays a high-priority red alert banner.
3. The affected corridor pin on the OpenStreetMap changes from **Green** to **Red**.
4. The event is appended to the **Congestion Alert Log** with time, speed, volume, and exact rule violated.

---

## 6. Real-Time Analytics Requirements

The platform calculates four distinct analytical metrics:

### 6.1 Most Congested Road
* **Methodology:** Aggregates all sensor readings by road name, ranking by the highest frequency of congestion alerts and lowest average speed:
```sql
SELECT road_name, ROUND(AVG(avg_speed), 1) AS mean_speed,
       ROUND(AVG(road_occupancy), 1) AS mean_occupancy,
       SUM(is_congested) AS alert_count
FROM sensor_readings
GROUP BY road_name
ORDER BY alert_count DESC, mean_speed ASC
LIMIT 1;
```

### 6.2 Average Traffic by Hour (24-Hour Profile)
* **Methodology:** Groups time-series readings by hour interval (`00:00` to `23:00`), calculating mean vehicular volume. Displayed via a bar chart on the dashboard.

### 6.3 Vehicle Volume Trends (Time-Series Stream)
* **Methodology:** Plots real-time chronological traffic volume variations across recent ingestion intervals via a responsive line chart.

### 6.4 Peak Traffic Periods
* **Methodology:** Identifies the top 3 hourly intervals generating the highest average traffic density (e.g., Morning Peak: 09:00–10:00, Evening Peak: 18:00–20:00).

---

## 7. AWS Free Tier Deployment Guide

This project is deployed entirely within the **AWS Free Tier ($0 Budget)**:

1. **Virtual Machine Provisioning:**
   * **Service:** Amazon Elastic Compute Cloud (EC2)
   * **Instance Type:** `t2.micro` (1 vCPU, 1 GB RAM, 750 free hours/month)
   * **Operating System:** Ubuntu Server 22.04 LTS / 24.04 LTS (HVM)
   * **Storage:** 20 GB General Purpose SSD (gp3) (Free up to 30 GB)
2. **Security Group (Firewall) Rules:**
   * Inbound Rule 1: `SSH` | Protocol: `TCP` | Port: `22` | Source: `My IP` (or `0.0.0.0/0`)
   * Inbound Rule 2: `Custom TCP` | Protocol: `TCP` | Port: `5000` | Source: `0.0.0.0/0` (Dashboard Access)
3. **Execution on EC2 Instance:**
   ```bash
   sudo apt update && sudo apt install -y python3-pip git
   pip3 install flask requests
   # Run server in the background
   nohup python3 app.py > app.log 2>&1 &
   # Run IoT simulator in the background
   nohup python3 simulator.py --target http://127.0.0.1:5000/api/ingest > sim.log 2>&1 &
   ```
4. **Public Verification:**
   Accessible worldwide at: `http://<EC2-Public-IP>:5000`

---

## 8. Testing Report & Verification Matrix

| Test ID | Test Scenario | Input Data | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-01** | Normal Traffic Ingestion | Count = 220, Speed = 45 km/h, Occ = 35% | Ingested successfully; `is_congested = 0`; Map pin Green | Ingested; Status 201; No alert | **PASS** |
| **TC-02** | High Volume Congestion | Count = 580, Speed = 22 km/h, Occ = 82% | Congestion triggered (`Count > 500`); Red alert logged | Ingested; `is_congested = 1`; Alert triggered | **PASS** |
| **TC-03** | Low Speed Congestion | Count = 420, Speed = 9.5 km/h, Occ = 88% | Congestion triggered (`Speed < 15 km/h`); Map pin turns Red | Ingested; `is_congested = 1`; Map updated | **PASS** |
| **TC-04** | Dual Threshold Violation | Count = 640, Speed = 8.2 km/h, Occ = 94% | Congestion triggered (`Count > 500 & Speed < 15 km/h`) | Ingested; Both reasons flagged in log | **PASS** |
| **TC-05** | Real-Time Analytics API | `GET /api/analytics` | Returns most congested road, hourly averages, volume trends | Returned HTTP 200 with JSON metrics | **PASS** |
| **TC-06** | Historical CSV Export | `GET /api/export-csv` | Generates downloadable CSV evidence file | Successfully downloads `traffic_sensor_evidence.csv` | **PASS** |

---

## 9. Deliverables & Evidence Screenshot Checklist

When preparing your final document submission, insert the following original screenshots:

* [ ] **Screenshot 1: AWS EC2 Management Console**  
  *Showing the `t2.micro` instance in "Running" state with public IPv4 address and Free Tier badge.*
* [ ] **Screenshot 2: EC2 Security Group Configuration**  
  *Showing Inbound Rules allowing Port 22 (SSH) and Port 5000 (Custom TCP).*
* [ ] **Screenshot 3: Terminal Output of Sensor Simulator**  
  *Showing `simulator.py` streaming telemetry and printing `[NORMAL FLOW]` and `[ALERT FIRED]`.*
* [ ] **Screenshot 4: Real-Time Traffic Operations Dashboard**  
  *Showing the top navigation bar, 4 KPI cards, OpenStreetMap with colored markers, and volume charts.*
* [ ] **Screenshot 5: Active Congestion Alert Evidence**  
  *Showing the red alert banner and the logged alert details when speed < 15 km/h or vehicle count > 500.*

---

## 10. Challenges Faced & Lessons Learned

1. **Zero-Cost Cloud Architecture:** Choosing to host open-source time-series storage and visualization directly on an EC2 `t2.micro` instance prevented high costs associated with proprietary managed services like AWS Timestream or Managed Grafana.
2. **Handling Browser GET vs. API POST Requests:** Initial direct navigation to `/api/ingest` returned HTTP 405 (Method Not Allowed). Implemented route handling for both `GET` (health status) and `POST` (sensor telemetry) to ensure smooth operation.
3. **Geospatial Mapping without Billing Dependencies:** Replaced proprietary mapping APIs requiring billing credentials with OpenStreetMap and Leaflet.js, ensuring 100% free operation and rapid rendering.

---

## 11. Conclusion & Future Enhancements

The **Smart City Traffic Monitoring System** satisfies all objectives outlined for Assignment 22. It demonstrates end-to-end cloud computing principles: infrastructure provisioning (AWS EC2), time-series data storage, RESTful ingestion pipelines, automated event-driven rule processing, and browser-based real-time analytics.

### Future Enhancements:
* **Edge ML Integration:** Deploying lightweight Computer Vision models (YOLOv8-nano) directly at edge cameras for automated vehicle counting.
* **Smart Traffic Light Actuation:** Automatically extending green signal intervals along corridors flagged by the congestion alert engine.

---

## 12. 3-Minute Demo Presentation Script

Use this structured walkthrough for your 5-mark live presentation:

* **0:00 – 0:45 (Introduction & Cloud Architecture):**  
  *"Good morning Sir/Ma'am. My name is K M Rakshith Gowda, and my assignment is Topic #22: Smart City Traffic Monitoring System. I deployed a real-time IoT traffic intelligence platform hosted entirely on an AWS EC2 Free Tier Linux VM."*
* **0:45 – 1:30 (IoT Ingestion & Real-Time Dashboard):**  
  *"Here is our cloud web dashboard running live on port 5000. On the left, we have an interactive OpenStreetMap showing Bangalore's key transit corridors such as Silk Board, MG Road, and Hebbal. The telemetry simulator is streaming live readings every 3 seconds, including Vehicle Count, Average Speed, and Road Occupancy."*
* **1:30 – 2:30 (Congestion Detection Demo):**  
  *"Now, let us observe the alert rule engine. As specified in the assignment, if the vehicle count exceeds 500 or average speed drops below 15 km/h, the system automatically fires a critical congestion alert. You can see the Silk Board node just recorded a speed of 11 km/h: the marker immediately switches to red, a high-priority alert banner appears at the top, and the violation is logged in our time-series database."*
* **2:30 – 3:00 (Analytics & Conclusion):**  
  *"Below the map, our analytics engine calculates the Most Congested Road, 24-hour hourly averages, and volume trends over time. We can also export the full audit trail as a CSV file with one click. This demonstrates a complete, zero-cost, cloud-native IoT solution. Thank you, and we are ready for any questions!"*
