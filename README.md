# Smart City Traffic Monitoring & Congestion Analytics System
**Cloud Computing SA Assignment #22**  
**Author:** K M Rakshith Gowda  
**Target Environment:** AWS Free Tier (EC2 `t2.micro` Linux VM)

---

## 📌 Architecture Overview
```
[ IoT Traffic Simulator (simulator.py) ]
              │ (HTTP/REST Ingestion every 3s)
              ▼
[ AWS EC2 Linux VM (t2.micro - Free Tier) ]
   ├── Ingestion & Analytics Engine (app.py - Flask)
   ├── Time-Series Database (traffic_data.db)
   ├── Congestion Detection Engine (Count > 500 OR Speed < 15 km/h)
   └── Interactive Operations Dashboard (Leaflet.js + Chart.js + OpenStreetMap)
              │
              ▼
[ Web Browser Access: http://<EC2-Public-IP>:5000 ]
```

---

## 🚀 Running Locally (Step-by-Step)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start Cloud Backend / Web Server
```bash
python app.py
```
Open your browser at: `http://localhost:5000`

### 3. Start IoT Sensor Simulator (in a new terminal)
```bash
python simulator.py
```

To simulate constant heavy congestion bursts for testing alerts:
```bash
python simulator.py --burst
```

---

## ☁️ AWS EC2 Free Tier Deployment Steps

1. Launch a **`t2.micro`** EC2 instance with **Ubuntu 22.04 LTS** or **Amazon Linux 2023** (Free Tier eligible).
2. Under **Security Groups**, add inbound rules:
   - **SSH**: Port `22` (Source: My IP)
   - **Custom TCP**: Port `5000` (Source: `0.0.0.0/0` - Anywhere)
3. Connect via SSH to your EC2 instance.
4. Clone or copy these files to the EC2 instance.
5. Run:
   ```bash
   sudo apt update && sudo apt install -y python3-pip
   pip3 install -r requirements.txt
   nohup python3 app.py &
   nohup python3 simulator.py &
   ```
6. Access the live dashboard at: `http://<EC2-Public-IP>:5000`
