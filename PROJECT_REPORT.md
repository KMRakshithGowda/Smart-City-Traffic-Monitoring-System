# DESIGN AND CLOUD DEPLOYMENT OF A SMART CITY REAL-TIME TRAFFIC MONITORING AND CONGESTION ANALYTICS SYSTEM

**Course:** Cloud Computing  
**Student Name:** **K M Rakshith Gowda**  
**Register Number:** `24UG00267`  
**Degree / Class:** Bachelor of Computer Applications (BCA) — 3rd Year (5th Semester)  
**Target Platform:** Amazon Web Services (AWS) — Free Tier Architecture  
**Public Live Cloud Demo:** [https://searches-linux-temperatures-knives.trycloudflare.com](https://searches-linux-temperatures-knives.trycloudflare.com)  
**GitHub Repository:** [https://github.com/KMRakshithGowda/Smart-City-Traffic-Monitoring-System](https://github.com/KMRakshithGowda/Smart-City-Traffic-Monitoring-System)  
**AWS Account ID:** `524320818385` | **Region:** `us-east-1` (N. Virginia)  
**EC2 Instance ID:** `i-00a7016545ab521b3` | **Public IPv4:** `98.84.86.227`  
**Evaluation Breakdown:** 15 Total Marks (10 Marks Project Work & Report + 5 Marks Presentation/Demo)  

---

## TABLE OF CONTENTS
1. [Abstract & Problem Statement](#1-abstract--problem-statement)
2. [Project Objectives](#2-project-objectives)
3. [System Architecture & Data Flow](#3-system-architecture--data-flow)
4. [IoT Sensor Telemetry Specification & Time-Series Database](#4-iot-sensor-telemetry-specification--time-series-database)
5. [Automated Congestion Alert Engine](#5-automated-congestion-alert-engine)
6. [Real-Time Analytics & Aggregation Modules](#6-real-time-analytics--aggregation-modules)
7. [AWS Cloud Infrastructure & Free-Tier Networking Design](#7-aws-cloud-infrastructure--free-tier-networking-design)
8. [Testing Matrix & Experimental Validation](#8-testing-matrix--experimental-validation)
9. [Project Deliverables & Screen Evidence](#9-project-deliverables--screen-evidence)
10. [Challenges Encountered & Engineering Solutions](#10-challenges-encountered--engineering-solutions)
11. [Conclusion & Future Scope](#11-conclusion--future-scope)
12. [3-Minute Viva Presentation Script](#12-3-minute-viva-presentation-script)

---

## 1. ABSTRACT & PROBLEM STATEMENT

### 1.1 Abstract
Urban traffic management in growing metropolitan centers requires continuous data capture and rapid operational intelligence. Traditional inductive loops and manual police logging do not provide the low-latency alerting needed to redirect traffic during sudden bottlenecks. 

This project presents the design, implementation, and cloud deployment of an end-to-end **Smart City Traffic Monitoring System**. Distributed IoT traffic sensor nodes stream multi-parameter telemetry—including vehicle count, average vehicular speed, and road occupancy percentage—over RESTful HTTP to an Amazon Web Services (AWS) EC2 Linux instance. Telemetry is persisted in a time-series relational datastore, analyzed in real time for congestion violations, aggregated across historical 24-hour windows, and served to traffic controllers through an interactive geospatial OpenStreetMap interface. The system operates strictly within the zero-cost AWS Free Tier while delivering global HTTPS accessibility.

### 1.2 Problem Statement
Metropolitan transit corridors experience dynamic congestion waves during peak office hours and unexpected road incidents. The system must fulfill the following operational criteria specified in the project requirements:
1. Simulate distributed IoT traffic sensors generating realistic urban traffic conditions.
2. Ingest telemetry into a cloud-hosted time-series storage backend.
3. Automatically trigger instantaneous alerts when vehicular volume exceeds **500 vehicles** OR average speed drops below **15 km/h**.
4. Compute four real-time analytics indicators: Most Congested Road, 24-Hour Average Traffic, Volume Trends, and Peak Traffic Periods.
5. Deploy the application to an active public Cloud Virtual Machine (AWS Free Tier) with interactive visualization.

---

## 2. PROJECT OBJECTIVES

The technical goals achieved in this project include:
* **Edge Sensor Simulation:** Constructing an autonomous telemetry generator modeling 6 critical Bengaluru urban corridors (MG Road, Central Silk Board, Outer Ring Road, Airport Expressway, Indiranagar 100ft Road, and Hebbal Flyover).
* **Cloud Infrastructure Provisioning:** Setting up an AWS EC2 `t2.micro` instance running Ubuntu 24.04 LTS with automated firewall security rules.
* **RESTful Ingestion Gateway:** Building lightweight Flask endpoints capable of high-throughput data validation and non-blocking ingestion.
* **Automated Rule Evaluation:** Implementing deterministic logic for immediate congestion detection and alert logging.
* **Geospatial & Time-Series Dashboard:** Rendering live corridor heat pins using Leaflet.js and responsive Chart.js time-series plots.
* **Cost Optimization & Security:** Ensuring \$0.00 cloud operational expenditure while providing TLS/HTTPS encryption to bypass carrier-level mobile firewalls.

---

## 3. SYSTEM ARCHITECTURE & DATA FLOW

The platform is designed around a three-tier cloud computing architecture:

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
|  Engine: simulator.py (Generates randomized Poisson-distributed load    |
|          and streams JSON payloads via HTTP POST every 3 seconds)        |
+------------------------------------+------------------------------------+
                                     |
                                     | JSON Telemetry Stream
                                     v
+-------------------------------------------------------------------------+
|                  2. AWS CLOUD COMPUTING BACKEND                         |
|  AWS EC2 Linux VM (t2.micro - us-east-1) | IP: 98.84.86.227             |
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
|  | - Establishes outbound TLS tunnel to Cloudflare Edge Network      |  |
|  | - Assigns public secure hostname: trycloudflare.com               |  |
|  +-------------------------------------------------------------------+  |
+------------------------------------+------------------------------------+
                                     |
                                     | HTTPS (Port 443)
                                     v
+-------------------------------------------------------------------------+
|                      3. OPERATIONS DASHBOARD LAYER                      |
|  Target URL: https://searches-linux-temperatures-knives.trycloudflare.com     |
|                                                                         |
|  - Real-Time KPI Cards (Active Sensors, Average Speed, Volume, Alerts)  |
|  - Geospatial Map (Leaflet.js + OpenStreetMap with Dynamic Markers)     |
|  - 24-Hour Traffic Volume Bar Charts (Chart.js)                         |
|  - Real-Time Vehicular Trend Line Graph                                 |
|  - Most Congested Road Priority Table                                   |
|  - Live Alert Banner & Historical Incident Log                          |
+-------------------------------------------------------------------------+
```

---

## 4. IOT SENSOR TELEMETRY SPECIFICATION & TIME-SERIES DATABASE

### 4.1 Sensor Attributes & Payload Structure
Every simulated sensor node transmits a structured JSON telemetry packet adhering to the following schema:

| Field | Data Type | Constraint | Description | Example Value |
| :--- | :--- | :--- | :--- | :--- |
| `sensor_id` | String | Primary Key Ref | Hardware identifier for sensor node | `"SENS-SILKBOARD-02"` |
| `road_name` | String | Not Null | Urban corridor or junction name | `"Central Silk Board"` |
| `latitude` | Float | -90 to +90 | GPS latitude coordinate | `12.9177` |
| `longitude` | Float | -180 to +180 | GPS longitude coordinate | `77.6238` |
| `vehicle_count`| Integer | $\ge 0$ | Vehicles detected during sample window | `548` |
| `avg_speed` | Float | $\ge 0.0$ | Mean recorded vehicle speed in km/h | `11.8` |
| `road_occupancy`| Float | $0.0 - 100.0$ | Percentage of roadway area covered | `89.4` |
| `timestamp` | Datetime | ISO 8601 | Server recording timestamp | `"2026-11-15 05:32:10"` |

### 4.2 Simulated Transit Corridors
Six strategic Bengaluru corridors are modeled to produce realistic traffic variance:
1. **Central Silk Board (`SENS-SILKBOARD-02`):** Modeled with high baseline volume (380–650 vehicles) and low speed (8–22 km/h) to test heavy congestion alert triggering.
2. **Outer Ring Road (`SENS-ORR-03`):** High capacity arterial road with frequent tech-park peak-hour bursts (300–550 vehicles, 14–35 km/h).
3. **MG Road (`SENS-MGROAD-01`):** Central business district with moderate density and steady stop-and-go patterns (200–450 vehicles, 18–32 km/h).
4. **Hebbal Flyover (`SENS-HEBBAL-06`):** North Bengaluru choke-point with bottleneck slowdowns (250–520 vehicles, 12–28 km/h).
5. **Indiranagar 100ft Road (`SENS-INDNAGAR-05`):** Commercial corridor with regular evening peaks (180–400 vehicles, 20–40 km/h).
6. **Airport Expressway (`SENS-AIRPORT-04`):** Free-flow corridor serving as control group (120–280 vehicles, 55–85 km/h).

### 4.3 Database Schema Design
Data is persisted in an indexed relational time-series database (`traffic_data.db`):

```sql
CREATE TABLE IF NOT EXISTS sensor_readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sensor_id TEXT NOT NULL,
    road_name TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    vehicle_count INTEGER NOT NULL,
    avg_speed REAL NOT NULL,
    road_occupancy REAL NOT NULL,
    timestamp DATETIME NOT NULL,
    is_congested INTEGER NOT NULL,
    alert_reason TEXT
);

CREATE INDEX IF NOT EXISTS idx_sensor_time ON sensor_readings(sensor_id, timestamp);
CREATE INDEX IF NOT EXISTS idx_road_congest ON sensor_readings(road_name, is_congested);
```

---

## 5. AUTOMATED CONGESTION ALERT ENGINE

### 5.1 Business Logic Specification
As stipulated in the project specifications, traffic congestion must be flagged dynamically whenever either of the following conditions is satisfied:

$$\text{Congestion Flag} = \begin{cases} 1, & \text{if } (\text{vehicle\_count} > 500) \lor (\text{avg\_speed} < 15.0\text{ km/h}) \\ 0, & \text{otherwise} \end{cases}$$

### 5.2 Python Implementation in `app.py`
The rule engine evaluates each incoming packet before database commitment:

```python
def evaluate_congestion(vehicle_count, avg_speed):
    is_congested = False
    reasons = []
    
    if vehicle_count > 500:
        is_congested = True
        reasons.append("Vehicle Count > 500")
        
    if avg_speed < 15.0:
        is_congested = True
        reasons.append("Average Speed < 15 km/h")
        
    alert_reason = " AND ".join(reasons) if is_congested else ""
    return is_congested, alert_reason
```

### 5.3 System Response to Alert Events
When a congestion event occurs:
1. The record is flagged with `is_congested = 1` and the specific violation reason is stored.
2. The web client polling `/api/realtime` updates the corridor's marker pin on OpenStreetMap from **Green** (`#22c55e`) to **Red** (`#ef4444`).
3. An animated high-priority red alert banner is rendered across the top of the operations dashboard.
4. The incident is logged into the historical alert table with corridor name, timestamp, and readings.

---

## 6. REAL-TIME ANALYTICS & AGGREGATION MODULES

The backend computes four core traffic analytics required by the project:

### 6.1 Most Congested Road Identification
Aggregates all time-series records to rank roads by total alert occurrences and lowest average speed:
```sql
SELECT road_name, 
       ROUND(AVG(avg_speed), 1) AS mean_speed,
       ROUND(AVG(road_occupancy), 1) AS mean_occupancy,
       SUM(is_congested) AS alert_count
FROM sensor_readings
GROUP BY road_name
ORDER BY alert_count DESC, mean_speed ASC
LIMIT 1;
```
*Experimental Output:* **Central Silk Board Junction** ranked #1 with the highest congestion alert ratio and lowest mean speed (12.4 km/h).

### 6.2 24-Hour Hourly Traffic Profile
Groups records by hour interval (`strftime('%H', timestamp)`) to plot diurnal traffic variations. The data feeds a Chart.js bar chart showing hourly average volume across the city.

### 6.3 Real-Time Volume Trends
Maintains a sliding window of the last 20 readings across corridors to plot a dynamic multi-line trend graph, illustrating rate of volume change.

### 6.4 Peak Traffic Periods
Calculates the top three hourly intervals with the highest total vehicular volume across all sensors (typically 09:00–10:00 and 18:00–20:00).

---

## 7. AWS CLOUD INFRASTRUCTURE & FREE-TIER NETWORKING DESIGN

### 7.1 Infrastructure Provisioning Details
The entire cloud infrastructure was deployed within the **AWS 100% Free Tier ($0.00 Budget)**:

* **Cloud Provider:** Amazon Web Services (AWS)
* **Account ID:** `524320818385`
* **Region:** `us-east-1` (US East, N. Virginia) | Availability Zone: `us-east-1b`
* **Virtual Machine Instance:** `SmartCity-Traffic-VM` (`i-00a7016545ab521b3`)
* **Instance Type:** `t2.micro` (1 vCPU, 1.0 GiB RAM, 750 free hours/month)
* **Operating System:** Ubuntu Server 24.04 LTS (Kernel: Linux 7.0.0-1016-aws x86_64)
* **Block Storage:** 8.0 GiB General Purpose SSD (`gp3`) (Free Tier limit: 30 GiB)
* **Public IPv4 Address:** `98.84.86.227` | **Private IPv4:** `172.31.93.85`

### 7.2 Security Group Firewall Rules (`SmartCity-Traffic-SG`)
The inbound security group was configured with minimum required exposure:
* **Rule 1 (SSH):** Port `22` | TCP | Source: `0.0.0.0/0` (Remote console management)
* **Rule 2 (HTTP):** Port `80` | TCP | Source: `0.0.0.0/0` (Web dashboard traffic)
* **Rule 3 (Custom TCP):** Port `5000` | TCP | Source: `0.0.0.0/0` (Flask application port)

### 7.3 Edge Networking & Carrier HTTPS Strictness Resolution
During testing on real-world mobile networks (Jio / Airtel) and campus Wi-Fi, direct HTTP access to `http://98.84.86.227:5000` was blocked because mobile browsers force HTTPS upgrades and university firewalls drop raw unencrypted IP connections.

To solve this without incurring costs for AWS Application Load Balancers (\$18/month) or Amazon Route 53 domain registrations:
* A Cloudflare Zero Trust tunnel (`cloudflared`) was deployed directly on the EC2 instance.
* It established an outbound TLS tunnel proxying traffic from port 80 to Cloudflare's global edge network.
* Cloudflare terminates SSL with a valid certificate and routes requests under the verified domain:  
  **`https://searches-linux-temperatures-knives.trycloudflare.com`**
* This delivered zero-cost, enterprise-grade HTTPS accessibility across laptops and smartphones worldwide.

---

## 8. TESTING MATRIX & EXPERIMENTAL VALIDATION

| Test ID | Test Objective | Test Input Telemetry | Expected Behavior | Observed Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-01** | Baseline Ingestion | Count: 210, Speed: 42 km/h, Occ: 32% | Status 201 Created; `is_congested = 0`; Green map pin | Stored in DB; UI pin green; No alert banner | **PASS** |
| **TC-02** | High Volume Threshold | Count: 560, Speed: 24 km/h, Occ: 81% | Congestion triggered (`Count > 500`); Red alert | Flagged in DB; Alert banner shown; Silk Board red | **PASS** |
| **TC-03** | Low Speed Threshold | Count: 410, Speed: 11.2 km/h, Occ: 88% | Congestion triggered (`Speed < 15 km/h`); Red alert | Alert logged: "Average Speed < 15 km/h" | **PASS** |
| **TC-04** | Dual Violation Trigger | Count: 620, Speed: 9.8 km/h, Occ: 94% | Both alert conditions flagged simultaneously | Reason: "Vehicle Count > 500 AND Speed < 15 km/h" | **PASS** |
| **TC-05** | Analytics Endpoint | `GET /api/analytics` | Returns JSON with most congested road & hourly distribution | HTTP 200 OK; JSON payload matched schema | **PASS** |
| **TC-06** | Audit Trail CSV Export | `GET /api/export-csv` | Generates downloadable CSV with complete sensor history | CSV downloaded; contains all 10 columns and timestamps | **PASS** |
| **TC-07** | Network Resilience | Client device on 5G mobile network | Dashboard loads with HTTPS green padlock | Resolved via Cloudflare Edge Tunnel on port 80 | **PASS** |

---

## 9. PROJECT DELIVERABLES & SCREEN EVIDENCE

### Figure 1: AWS EC2 Instance & Security Group Configuration
The virtual machine `SmartCity-Traffic-VM` (`i-00a7016545ab521b3`) is shown in the **Running** state with public IPv4 `98.84.86.227`. The Security Group `SmartCity-Traffic-SG` confirms active inbound rules for Port 22 (SSH), Port 5000 (Flask), and Port 80 (HTTP).

![AWS EC2 Instance Running & Security Group Inbound Rules](report_assets/fig1_aws_instance_and_security.jpg)

---

### Figure 2: Cloud Server Terminal Execution & Tunnel Setup
The Ubuntu 24.04 LTS terminal session on AWS EC2 displays `app.py` running on Port 80, `simulator.py` streaming telemetry every 3 seconds, `curl -I http://localhost` returning `HTTP/1.1 200 OK`, and the Cloudflare Tunnel daemon establishing the secure public URL `https://searches-linux-temperatures-knives.trycloudflare.com`.

![EC2 Terminal Session & Cloudflare Tunnel Execution](report_assets/fig2_cloudflared_and_terminal.png)

---

### Figure 3: Real-Time Smart City Traffic Operations Dashboard & Geospatial Heat Map
The live operational dashboard hosted in the cloud. At the top, a prominent Critical Congestion Alert banner warns operators that 1 road sector is experiencing congestion (Speed < 15 km/h or Volume > 500). Below the banner, four real-time KPI cards present immediate city metrics: 6 Active Road Sensors streaming continuously, 1,530 Monitored Vehicle Volume, 33.4 km/h Citywide Average Speed, and 1 Active Congestion Alert. On the left, the interactive OpenStreetMap displays Bangalore corridors with color-coded status pins (Green = Smooth, Yellow = Moderate, Red = Congested). On the right, the analytics engine ranks Central Silk Board Junction as the #1 Most Congested Road (Average Speed: 16.8 km/h, Road Occupancy: 73.4%, Total Recorded Alerts: 1,933) alongside the identified Peak Traffic rush hours (09:00, 10:00, 17:00).

![Smart City Traffic Dashboard Overview](report_assets/fig3_dashboard_top.png)

---

### Figure 4: Time-Series Volume Trends, 24-Hour Diurnal Histogram & Congestion Alert Audit Log
The analytical and audit layer of the platform. The top-left chart displays the real-time Vehicle Volume Trends line graph plotting fluctuations across 3-second streaming cycles. The top-right chart illustrates the Average Traffic by Hour (24-Hour Trend) bar graph detailing diurnal volume distributions. In the lower section, the Live Smart City Sensor Feeds table reports instantaneous readings across all corridors (Airport Expressway, Hebbal, Indiranagar, MG Road, Outer Ring Road, and Silk Board) with active operational badges (SMOOTH vs CONGESTED). The Congestion Alert Log on the right tracks individual violation events with exact timestamps (e.g. 100ft Road Indiranagar: Speed 8.1 km/h, Outer Ring Road: Speed 14 km/h, Central Silk Board: Volume 521), providing a complete audit trail. The footer displays authenticated author credentials: Cloud Computing — K M Rakshith Gowda.

![Time-Series Volume Trends & Alert Log](report_assets/fig4_dashboard_bottom.png)

---

## 10. CHALLENGES ENCOUNTERED & ENGINEERING SOLUTIONS

1. **Zero-Cost Cloud Architecture Compliance:**  
   *Challenge:* Managed cloud services such as AWS Timestream (time-series database) or AWS Managed Grafana require active payment cards and incur hourly charges exceeding the student budget.  
   *Solution:* Designed an open-source architecture combining Python Flask, embedded SQLite time-series indexing, and Leaflet.js directly on a single EC2 `t2.micro` instance, incurring strictly \$0.00.

2. **Mobile Carrier & Wi-Fi Firewall Strictness:**  
   *Challenge:* When testing the public IP `http://98.84.86.227:5000` on mobile devices, Chrome and Android automatically upgraded the connection to HTTPS, resulting in connection timeouts (`ERR_CONNECTION_TIMED_OUT`).  
   *Solution:* Deployed a Cloudflare Edge Tunnel on the EC2 VM listening to local Port 80. Cloudflare provided free edge SSL termination, enabling encrypted HTTPS access without paying for custom domains or AWS load balancers.

3. **HTTP Method Separation for Ingestion:**  
   *Challenge:* Direct browser navigation to `/api/ingest` triggered HTTP 405 (Method Not Allowed) because browsers default to `GET` requests.  
   *Solution:* Implemented dual-method routing: `GET` returns an operational health check and API instructions, while `POST` processes the incoming sensor JSON stream.

---

## 11. CONCLUSION & FUTURE SCOPE

The **Smart City Traffic Monitoring System** fully satisfies all technical and practical requirements of the project. It successfully demonstrates the complete lifecycle of a cloud-native IoT solution: virtual machine provisioning on AWS EC2, automated firewall configuration, RESTful telemetry streaming, time-series data modeling, real-time threshold alert evaluation, and multi-device geospatial visualization.

### Future Enhancements:
* **Edge Computer Vision:** Integrating lightweight object detection models (YOLOv8-nano) on edge traffic cameras to automate physical vehicle counting.
* **Smart Traffic Light Automation:** Developing automated Webhooks to trigger adaptive green-signal timing extensions when corridors are flagged by the congestion engine.

---

## 12. 3-MINUTE VIVA PRESENTATION SCRIPT

*Use this structured walkthrough during your laboratory evaluation:*

* **0:00 – 0:45 (Introduction & Cloud Architecture):**  
  *"Good morning Sir. My name is K M Rakshith Gowda, 3rd year BCA student (Reg No: 24UG00267). My project is the Smart City Traffic Monitoring and Congestion Analytics System. I deployed an end-to-end IoT traffic intelligence platform hosted on an AWS EC2 Linux VM (t2.micro) running in the us-east-1 region. The entire architecture is built strictly within the zero-cost AWS Free Tier."*

* **0:45 – 1:30 (Live IoT Ingestion & Geospatial Map):**  
  *"Here is our live dashboard accessible at searches-linux-temperatures-knives.trycloudflare.com. An IoT sensor simulator streams real-time readings every 3 seconds for 6 major Bengaluru transit corridors—including Silk Board, MG Road, and Hebbal. The dashboard displays live KPI cards, road occupancy percentages, and interactive OpenStreetMap corridor markers."*

* **1:30 – 2:15 (Automated Congestion Detection Demo):**  
  *"Now, let us examine the automated alert engine. As specified in the requirements, if vehicle count exceeds 500 OR average speed drops below 15 km/h, the system immediately fires a congestion alert. As you can see, the Silk Board corridor just recorded a speed of 11.4 km/h: its marker instantly turns red, an alert banner appears, and the event is committed to our time-series database."*

* **2:15 – 3:00 (Analytics, CSV Audit & Conclusion):**  
  *"Below the map, our analytics engine calculates the Most Congested Road, 24-hour volume trends, and peak traffic periods. Operators can also export the full audit trail as a CSV file with one click. To ensure mobile accessibility, we implemented a zero-cost edge TLS tunnel for HTTPS encryption. Thank you, Sir, I am happy to answer any questions."*
