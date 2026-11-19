# Smart City Traffic Monitoring & Congestion Analytics System

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Framework-Flask%203.0-black?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![AWS EC2](https://img.shields.io/badge/Cloud-AWS%20EC2%20t2.micro-FF9900?logo=amazon-aws&logoColor=white)](https://aws.amazon.com/ec2/)
[![SQLite3](https://img.shields.io/badge/Storage-SQLite3%20Time--Series-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Leaflet.js](https://img.shields.io/badge/Geospatial-Leaflet.js%20%2B%20OpenStreetMap-199900?logo=leaflet&logoColor=white)](https://leafletjs.com/)
[![Chart.js](https://img.shields.io/badge/Analytics-Chart.js-FF6384?logo=chartdotjs&logoColor=white)](https://www.chartjs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

An end-to-end cloud-native IoT traffic telemetry, real-time congestion detection, and analytics platform. The system ingests continuous multi-variable sensor streams across key urban transit corridors, performs deterministic congestion evaluations, aggregates time-series metrics, and visualizes live traffic patterns on an interactive geospatial dashboard.

---

## 👨‍💻 Project Information & Developer Bio

* **Developer:** **K M Rakshith Gowda**
* **Academic Program:** Bachelor of Computer Applications (BCA) — 3rd Year (5th Semester)
* **Registration Number:** `24UG00267`
* **Domain:** Cloud Computing & Real-Time IoT Systems
* **Target Cloud:** Amazon Web Services (AWS) — 100% Free Tier Architecture

---

## 🌐 Live Cloud Demo & Endpoints

| Environment | Access Link / Host | Protocol | Status |
| :--- | :--- | :--- | :--- |
| **Global Cloud Demo** | [https://searches-linux-temperatures-knives.trycloudflare.com](https://searches-linux-temperatures-knives.trycloudflare.com) | HTTPS (Port 443) | 🟢 **Live 24/7** |
| **AWS Direct IPv4** | `http://98.84.86.227` | HTTP (Port 80) | 🟢 **Active** |
| **Local Development** | `http://localhost:5000` | HTTP (Port 5000) | 💻 **Localhost** |

---

## 📌 Cloud & System Architecture

```
+-------------------------------------------------------------------------+
|                          1. IOT SENSOR LAYER                            |
|  - SENS-MGROAD-01 (MG Road Corridor)                                    |
|  - SENS-SILKBOARD-02 (Central Silk Board Junction)                      |
|  - SENS-ORR-03 (Outer Ring Road - Bellandur)                            |
|  - SENS-AIRPORT-04 (Airport Expressway)                                 |
|  - SENS-INDNAGAR-05 (Indiranagar 100ft Road)                            |
|  - SENS-HEBBAL-06 (Hebbal Flyover Junction)                             |
|                                                                         |
|  Engine: simulator.py (Streams JSON telemetry packets every 3 seconds)  |
+------------------------------------+------------------------------------+
                                     |
                                     | HTTP POST JSON Telemetry Stream
                                     v
+-------------------------------------------------------------------------+
|                  2. AWS CLOUD COMPUTING BACKEND                         |
|  AWS EC2 Linux VM (t2.micro - us-east-1) | Public IP: 98.84.86.227      |
|                                                                         |
|  +-------------------------------------------------------------------+  |
|  | Web Application Server (Flask on Port 80)                         |  |
|  | - Ingestion API: POST /api/ingest                                 |  |
|  | - Real-Time State API: GET /api/realtime                          |  |
|  | - Analytical Engine: GET /api/analytics                           |  |
|  | - Alert Query API: GET /api/alerts                                |  |
|  | - Historical CSV Export: GET /api/export-csv                      |  |
|  +---------------------------------+---------------------------------+  |
|                                    |                                    |
|         +--------------------------+--------------------------+         |
|         v                                                     v         |
|  +------------------------------+     +------------------------------+  |
|  | Congestion Evaluation Engine |     | Time-Series Storage Engine   |  |
|  | - Count > 500                |     | - SQLite3 (traffic_data.db)  |  |
|  | - Speed < 15.0 km/h          |     | - Indexed on (timestamp,     |  |
|  | - State: is_congested = 0 / 1|     |   sensor_id, road_name)      |  |
|  +------------------------------+     +------------------------------+  |
|                                    |                                    |
|  +---------------------------------+---------------------------------+  |
|  | Cloudflare Edge TLS Tunnel Daemon (cloudflared)                   |  |
|  | - Outbound encrypted tunnel from Port 80 to Cloudflare Edge       |  |
|  | - Public Domain: searches-linux-temperatures-knives.trycloudflare.com |  |
|  +-------------------------------------------------------------------+  |
+------------------------------------+------------------------------------+
                                     |
                                     | Secure HTTPS (Port 443)
                                     v
+-------------------------------------------------------------------------+
|                      3. OPERATIONS DASHBOARD LAYER                      |
|  - Real-Time KPI Cards (Active Sensors, Average Speed, Volume, Alerts)  |
|  - Geospatial Map (Leaflet.js + OpenStreetMap with Dynamic Markers)     |
|  - 24-Hour Diurnal Traffic Volume Histogram (Chart.js)                  |
|  - Real-Time Vehicular Volume Trend Line Graph                          |
|  - Most Congested Road Analytical Ranking Table                         |
|  - Live Alert Banner & Historical Incident Audit Log                    |
+-------------------------------------------------------------------------+
```

---

## ✨ Key Features

1. **Distributed IoT Sensor Simulator (`simulator.py`):**
   * Emulates continuous sensor telemetry across 6 major transit corridors in Bengaluru.
   * Generates randomized vehicular load, speed variance, and occupancy ratios with burst mode simulation support.

2. **Automated Congestion Detection Engine:**
   * Automatically evaluates incoming readings against dual safety rules:
     $$\text{Congestion Flag} = (\text{Vehicle Count} > 500) \lor (\text{Average Speed} < 15.0\text{ km/h})$$
   * Triggers immediate UI state change (marker switches from Green to Red), raises a high-priority alert banner, and logs incident details.

3. **Real-Time Traffic Analytics:**
   * **Most Congested Road:** Ranks corridors by highest alert frequency and lowest average speed (Central Silk Board ranked #1).
   * **24-Hour Hourly Profile:** Computes city-wide diurnal traffic volume distribution.
   * **Volume Trends:** Sliding window trend graph showing vehicular inflow rates.
   * **Peak Traffic Periods:** Identifies top morning and evening rush hours.

4. **One-Click Audit Export:**
   * Generates and downloads a complete sensor telemetry audit trail as a standard CSV file (`/api/export-csv`).

5. **Zero-Cost Secure Cloud Deployment:**
   * Hosted entirely on an AWS EC2 `t2.micro` Linux instance (100% Free Tier, \$0.00 spend).
   * Outbound TLS tunnel via Cloudflare delivers valid SSL encryption, bypassing mobile carrier firewall blocks on raw IP ports.

---

## 🚀 Running Locally (Localhost Setup)

You can clone and run this entire project locally on Windows, macOS, or Linux in less than 2 minutes.

### 1. Clone the Repository
```bash
git clone https://github.com/KMRakshithGowda/Smart-City-Traffic-Monitoring-System.git
cd Smart-City-Traffic-Monitoring-System
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```
*(Dependencies: `flask>=3.0.0`, `requests>=2.31.0`)*

### 3. Start the Backend Web Server
```bash
python app.py
```
* The server will initialize `traffic_data.db` and start listening on:  
  👉 **`http://localhost:5000`**

### 4. Start the IoT Sensor Simulator (in a new terminal)
```bash
python simulator.py
```
* The simulator will begin transmitting readings every 3 seconds to `http://127.0.0.1:5000/api/ingest`.

#### Optional: Simulate Heavy Congestion Bursts
To force continuous alert events across all corridors for testing:
```bash
python simulator.py --burst
```

---

## ☁️ AWS Cloud Deployment Guide (EC2 Free Tier)

Here is the exact step-by-step setup used to deploy this system to AWS:

### 1. Launch EC2 Instance
* **AMI:** Ubuntu Server 24.04 LTS (HVM)
* **Instance Type:** `t2.micro` (1 vCPU, 1 GB RAM — Free Tier eligible)
* **Storage:** 8 GB General Purpose SSD (`gp3`)
* **Region:** `us-east-1` (N. Virginia)

### 2. Configure Inbound Security Group (`SmartCity-Traffic-SG`)
| Type | Protocol | Port Range | Source | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **SSH** | TCP | `22` | `0.0.0.0/0` | Remote SSH Console Access |
| **HTTP** | TCP | `80` | `0.0.0.0/0` | Standard Web Traffic |
| **Custom TCP** | TCP | `5000` | `0.0.0.0/0` | Development Web Traffic |

### 3. Deploy Software on EC2
Connect via SSH or AWS EC2 Instance Connect and run:
```bash
# Update packages and install python dependencies
sudo apt update && sudo apt install -y python3-flask python3-requests git

# Clone repository
git clone https://github.com/KMRakshithGowda/Smart-City-Traffic-Monitoring-System.git
cd Smart-City-Traffic-Monitoring-System

# Start Flask server on Port 80 in background
sudo nohup python3 app.py > app.log 2>&1 &

# Start IoT telemetry stream in background
nohup python3 simulator.py --target http://127.0.0.1:80/api/ingest > sim.log 2>&1 &
```

### 4. Enable Secure Cloudflare Edge Tunnel (HTTPS)
```bash
# Download cloudflared binary
curl -sL https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o cloudflared && chmod +x cloudflared

# Launch tunnel proxying Port 80 in background
nohup ./cloudflared tunnel --url http://localhost:80 > cf.log 2>&1 &

# View assigned public HTTPS domain
grep -o 'https://[-a-zA-Z0-9.]*\.trycloudflare\.com' cf.log
```

---

## 📡 REST API Reference

| Endpoint | Method | Description | Sample Response / Status |
| :--- | :--- | :--- | :--- |
| `/api/ingest` | `POST` | Ingests real-time IoT sensor telemetry | `{"status": "success", "congested": true}` (201) |
| `/api/ingest` | `GET` | Health check and API usage instructions | `{"status": "online", "message": "..."}` (200) |
| `/api/realtime` | `GET` | Returns latest readings from all 6 corridors | Array of 6 sensor objects (200) |
| `/api/analytics`| `GET` | Computes most congested road, volume, hourly stats | Analytics JSON payload (200) |
| `/api/alerts` | `GET` | Returns historical congestion incidents (limit 50) | Array of alert records (200) |
| `/api/sample-data`| `GET`| Returns sample sensor telemetry schema | Sample JSON structure (200) |
| `/api/export-csv`| `GET` | Downloads full database audit trail as CSV | File: `traffic_sensor_evidence.csv` (200) |

---

## 📂 Repository File Structure

```
Smart-City-Traffic-Monitoring-System/
├── app.py                  # Core Flask backend, database persistence, analytics & API endpoints
├── simulator.py            # IoT traffic sensor stream generator for 6 Bengaluru corridors
├── requirements.txt        # Python package dependencies (Flask, Requests)
├── traffic_data.db         # Time-series SQLite database (auto-generated on first run)
├── templates/
│   └── index.html          # Responsive operations dashboard (Leaflet.js + Chart.js + OpenStreetMap)
├── report_assets/          # Embedded visual evidence and deployment screenshots
│   ├── fig1_aws_instance_and_security.jpg
│   ├── fig2_cloudflared_and_terminal.png
│   ├── fig3_dashboard_overview.png
│   └── fig4_congestion_alert.png
├── start_server.bat        # Windows 1-click startup script for web server
├── start_simulator.bat     # Windows 1-click startup script for IoT simulator
├── push_to_github.bat      # Automation script for Git synchronization
└── README.md               # Complete project documentation & setup guide
```

---

## 📊 Simulated Transit Corridors

| Sensor ID | Transit Corridor | Coordinates | Target Baseline Volume | Normal Speed |
| :--- | :--- | :--- | :--- | :--- |
| `SENS-MGROAD-01` | MG Road Central | `12.9716, 77.5946` | 200 – 450 veh | 18 – 32 km/h |
| `SENS-SILKBOARD-02`| Central Silk Board | `12.9177, 77.6238` | 380 – 650 veh | 8 – 22 km/h *(High Alert)* |
| `SENS-ORR-03` | Outer Ring Road | `12.9352, 77.6946` | 300 – 550 veh | 14 – 35 km/h |
| `SENS-AIRPORT-04` | Airport Expressway | `13.1986, 77.7066` | 120 – 280 veh | 55 – 85 km/h *(Free Flow)* |
| `SENS-INDNAGAR-05` | Indiranagar 100ft | `12.9784, 77.6408` | 180 – 400 veh | 20 – 40 km/h |
| `SENS-HEBBAL-06` | Hebbal Flyover | `13.0358, 77.5970` | 250 – 520 veh | 12 – 28 km/h |

---

## 📜 License

This project is open-source and distributed under the **[MIT License](LICENSE)**. Free for academic, educational, and development use.

---

**Developed with ❤️ by K M Rakshith Gowda (Reg. No: 24UG00267)**  
*BCA 3rd Year / 5th Semester*
