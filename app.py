import sqlite3
import os
import datetime
import random
from flask import Flask, request, jsonify, render_template, Response

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), "traffic_data.db")

# Predefined Smart City Sensor Corridors (with realistic GPS coordinates)
CORRIDORS = {
    "SENS-MGROAD-01": {"road": "MG Road Corridor", "lat": 12.9756, "lng": 77.6066},
    "SENS-SILKBOARD-02": {"road": "Central Silk Board Junction", "lat": 12.9177, "lng": 77.6238},
    "SENS-ORR-03": {"road": "Outer Ring Road (Tech Park)", "lat": 12.9352, "lng": 77.6946},
    "SENS-AIRPORT-04": {"road": "Airport Expressway", "lat": 13.1986, "lng": 77.7066},
    "SENS-INDNAGAR-05": {"road": "100ft Road Indiranagar", "lat": 12.9784, "lng": 77.6408},
    "SENS-HEBBAL-06": {"road": "Hebbal Flyover Junction", "lat": 13.0358, "lng": 77.5970}
}

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_readings (
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
        )
    ''')
    conn.commit()

    # Seed some initial historical records if empty so analytics show data immediately
    cursor.execute('SELECT COUNT(*) FROM sensor_readings')
    if cursor.fetchone()[0] == 0:
        print("[DB] Pre-seeding baseline historical traffic data...")
        now = datetime.datetime.now()
        for hours_ago in range(12, 0, -1):
            sample_time = now - datetime.timedelta(hours=hours_ago)
            hour_val = sample_time.hour
            # Peak hours around 9 AM and 6 PM
            is_peak = (8 <= hour_val <= 11) or (17 <= hour_val <= 20)
            
            for s_id, meta in CORRIDORS.items():
                if is_peak:
                    count = random.randint(380, 620)
                    speed = round(random.uniform(9.0, 22.0), 1)
                    occupancy = round(random.uniform(70.0, 96.0), 1)
                else:
                    count = random.randint(120, 340)
                    speed = round(random.uniform(35.0, 65.0), 1)
                    occupancy = round(random.uniform(20.0, 55.0), 1)
                
                congested = 1 if (count > 500 or speed < 15.0) else 0
                alert_reason = ""
                if count > 500 and speed < 15.0:
                    alert_reason = "Vehicle Count > 500 AND Speed < 15 km/h"
                elif count > 500:
                    alert_reason = "Vehicle Count > 500"
                elif speed < 15.0:
                    alert_reason = "Average Speed < 15 km/h"

                cursor.execute('''
                    INSERT INTO sensor_readings 
                    (sensor_id, road_name, latitude, longitude, vehicle_count, avg_speed, road_occupancy, timestamp, is_congested, alert_reason)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (s_id, meta["road"], meta["lat"], meta["lng"], count, speed, occupancy, sample_time.strftime("%Y-%m-%d %H:%M:%S"), congested, alert_reason))
        conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

# Ingestion API for IoT Simulator
@app.route('/api/ingest', methods=['GET', 'POST'])
def ingest():
    if request.method == 'GET':
        return jsonify({
            "status": "active",
            "endpoint": "/api/ingest",
            "message": "IoT Traffic Ingestion Gateway is online. Send HTTP POST with JSON payload (sensor_id, vehicle_count, avg_speed, road_occupancy, timestamp)."
        }), 200

    data = request.get_json(force=True)
    sensor_id = data.get("sensor_id")
    vehicle_count = int(data.get("vehicle_count", 0))
    avg_speed = float(data.get("avg_speed", 0.0))
    road_occupancy = float(data.get("road_occupancy", 0.0))
    timestamp = data.get("timestamp") or datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    meta = CORRIDORS.get(sensor_id, {"road": "City Road Segment", "lat": 12.9716, "lng": 77.5946})
    road_name = data.get("road_name") or meta["road"]
    latitude = float(data.get("latitude") or meta["lat"])
    longitude = float(data.get("longitude") or meta["lng"])

    # Prof Assignment Rule: Congestion Alert when Vehicle Count > 500 OR Speed < 15 km/h
    is_congested = False
    reasons = []
    if vehicle_count > 500:
        reasons.append("Vehicle Count > 500")
        is_congested = True
    if avg_speed < 15.0:
        reasons.append("Average Speed < 15 km/h")
        is_congested = True

    alert_reason = " & ".join(reasons) if is_congested else ""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO sensor_readings 
        (sensor_id, road_name, latitude, longitude, vehicle_count, avg_speed, road_occupancy, timestamp, is_congested, alert_reason)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (sensor_id, road_name, latitude, longitude, vehicle_count, avg_speed, road_occupancy, timestamp, 1 if is_congested else 0, alert_reason))
    conn.commit()
    conn.close()

    return jsonify({
        "status": "success",
        "message": "Data ingested successfully",
        "is_congested": is_congested,
        "alert_reason": alert_reason
    }), 201

# Real-time state of all sensors
@app.route('/api/realtime', methods=['GET'])
def get_realtime():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get latest reading for each sensor
    cursor.execute('''
        SELECT r.* FROM sensor_readings r
        INNER JOIN (
            SELECT sensor_id, MAX(id) as max_id
            FROM sensor_readings
            GROUP BY sensor_id
        ) latest ON r.id = latest.max_id
        ORDER BY r.sensor_id ASC
    ''')
    rows = cursor.fetchall()
    sensors = [dict(row) for row in rows]

    # Overall KPIs
    total_active_sensors = len(sensors)
    total_vehicles = sum(s["vehicle_count"] for s in sensors) if sensors else 0
    avg_speed_city = round(sum(s["avg_speed"] for s in sensors) / total_active_sensors, 1) if total_active_sensors else 0.0
    active_alerts = sum(1 for s in sensors if s["is_congested"] == 1)

    conn.close()
    return jsonify({
        "sensors": sensors,
        "kpis": {
            "total_active_sensors": total_active_sensors,
            "total_vehicles": total_vehicles,
            "avg_speed_city": avg_speed_city,
            "active_alerts": active_alerts
        }
    })

# Analytics API satisfying professor requirements:
# 1. Most congested road
# 2. Average traffic by hour
# 3. Vehicle volume trends
# 4. Peak traffic periods
@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 1. Most Congested Road (ranked by lowest average speed and highest congestion incidents)
    cursor.execute('''
        SELECT road_name, 
               ROUND(AVG(avg_speed), 1) as mean_speed, 
               ROUND(AVG(road_occupancy), 1) as mean_occupancy,
               SUM(is_congested) as alert_count,
               COUNT(*) as total_samples
        FROM sensor_readings
        GROUP BY road_name
        ORDER BY alert_count DESC, mean_speed ASC
    ''')
    congested_roads = [dict(r) for r in cursor.fetchall()]

    # 2. Average Traffic by Hour (0 to 23)
    cursor.execute('''
        SELECT strftime('%H:00', timestamp) as hour_label,
               ROUND(AVG(vehicle_count), 0) as avg_vehicle_count,
               ROUND(AVG(avg_speed), 1) as avg_speed
        FROM sensor_readings
        GROUP BY hour_label
        ORDER BY hour_label ASC
    ''')
    hourly_traffic = [dict(r) for r in cursor.fetchall()]

    # 3. Vehicle Volume Trends (Last 20 readings overall across time)
    cursor.execute('''
        SELECT timestamp, sensor_id, vehicle_count, avg_speed, road_occupancy
        FROM sensor_readings
        ORDER BY id DESC
        LIMIT 20
    ''')
    trends = [dict(r) for r in cursor.fetchall()]
    trends.reverse()

    # 4. Peak Traffic Periods (Top hours with maximum vehicle counts)
    cursor.execute('''
        SELECT strftime('%H:00', timestamp) as peak_hour,
               MAX(vehicle_count) as max_vehicles,
               ROUND(AVG(vehicle_count), 0) as avg_vehicles
        FROM sensor_readings
        GROUP BY peak_hour
        ORDER BY avg_vehicles DESC
        LIMIT 3
    ''')
    peak_periods = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return jsonify({
        "most_congested_road": congested_roads[0] if congested_roads else None,
        "congested_roads_ranking": congested_roads,
        "hourly_traffic": hourly_traffic,
        "volume_trends": trends,
        "peak_traffic_periods": peak_periods
    })

# Recent Alert Logs
@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, sensor_id, road_name, vehicle_count, avg_speed, road_occupancy, timestamp, alert_reason
        FROM sensor_readings
        WHERE is_congested = 1
        ORDER BY id DESC
        LIMIT 15
    ''')
    alerts = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify({"alerts": alerts})

# Raw Sample Data for Reports
@app.route('/api/sample-data', methods=['GET'])
def get_sample_data():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
        SELECT sensor_id, road_name, vehicle_count, avg_speed, road_occupancy, timestamp, is_congested, alert_reason
        FROM sensor_readings
        ORDER BY id DESC
        LIMIT 10
    ''')
    samples = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify({"sample_sensor_data": samples})

# CSV Export for Prof Evidence
@app.route('/api/export-csv', methods=['GET'])
def export_csv():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT sensor_id, road_name, vehicle_count, avg_speed, road_occupancy, timestamp, is_congested, alert_reason
        FROM sensor_readings ORDER BY id DESC LIMIT 200
    ''')
    rows = cursor.fetchall()
    conn.close()

    csv_data = "Sensor ID,Road Name,Vehicle Count,Average Speed (km/h),Road Occupancy (%),Timestamp,Is Congested,Alert Reason\n"
    for r in rows:
        csv_data += f'"{r[0]}","{r[1]}",{r[2]},{r[3]},{r[4]},"{r[5]}",{r[6]},"{r[7]}"\n'

    return Response(csv_data, mimetype="text/csv", headers={"Content-disposition": "attachment; filename=traffic_sensor_evidence.csv"})

if __name__ == '__main__':
    # Runs on all network interfaces on port 5000 (accessible on cloud VM via public IP)
    app.run(host='0.0.0.0', port=5000, debug=False)
