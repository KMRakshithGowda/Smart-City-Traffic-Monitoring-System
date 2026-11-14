"""
Smart City Traffic Sensor Simulator
Simulates IoT edge sensor units streaming traffic data over HTTP/REST to the Cloud Backend.
Matches the Assignment 22 specification:
- Sensor ID
- Vehicle Count
- Average Speed (km/h)
- Road Occupancy (%)
- Timestamp
- Automated Congestion Simulation: triggers Vehicle Count > 500 OR Speed < 15 km/h
"""

import time
import datetime
import random
import argparse
import requests

SENSORS = [
    {"sensor_id": "SENS-MGROAD-01", "road": "MG Road Corridor", "lat": 12.9756, "lng": 77.6066, "base_speed": 35},
    {"sensor_id": "SENS-SILKBOARD-02", "road": "Central Silk Board Junction", "lat": 12.9177, "lng": 77.6238, "base_speed": 18},
    {"sensor_id": "SENS-ORR-03", "road": "Outer Ring Road (Tech Park)", "lat": 12.9352, "lng": 77.6946, "base_speed": 28},
    {"sensor_id": "SENS-AIRPORT-04", "road": "Airport Expressway", "lat": 13.1986, "lng": 77.7066, "base_speed": 70},
    {"sensor_id": "SENS-INDNAGAR-05", "road": "100ft Road Indiranagar", "lat": 12.9784, "lng": 77.6408, "base_speed": 30},
    {"sensor_id": "SENS-HEBBAL-06", "road": "Hebbal Flyover Junction", "lat": 13.0358, "lng": 77.5970, "base_speed": 22}
]

def generate_sensor_reading(sensor_meta, force_congestion=False):
    # If congestion forced or Silk Board bottleneck chance
    if force_congestion or (sensor_meta["sensor_id"] == "SENS-SILKBOARD-02" and random.random() < 0.45) or random.random() < 0.25:
        # CONGESTION EVENT (Rules: Vehicle Count > 500 OR Speed < 15 km/h)
        scenario = random.choice(["high_count", "low_speed", "both"])
        if scenario == "high_count":
            vehicle_count = random.randint(510, 650)
            avg_speed = round(random.uniform(16.0, 24.0), 1)
            road_occupancy = round(random.uniform(75.0, 92.0), 1)
        elif scenario == "low_speed":
            vehicle_count = random.randint(350, 480)
            avg_speed = round(random.uniform(7.0, 14.5), 1) # < 15 km/h
            road_occupancy = round(random.uniform(80.0, 95.0), 1)
        else: # Both
            vehicle_count = random.randint(520, 700)
            avg_speed = round(random.uniform(6.0, 13.0), 1)
            road_occupancy = round(random.uniform(85.0, 98.0), 1)
    else:
        # NORMAL TRAFFIC FLOW
        vehicle_count = random.randint(80, 420)
        base = sensor_meta["base_speed"]
        avg_speed = round(random.uniform(base - 10, base + 15), 1)
        if avg_speed < 16.0:
            avg_speed = 22.0
        road_occupancy = round(random.uniform(20.0, 65.0), 1)

    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
        "sensor_id": sensor_meta["sensor_id"],
        "road_name": sensor_meta["road"],
        "latitude": sensor_meta["lat"],
        "longitude": sensor_meta["lng"],
        "vehicle_count": vehicle_count,
        "avg_speed": avg_speed,
        "road_occupancy": road_occupancy,
        "timestamp": now_str
    }

def run_simulation(target_url, interval=3, force_burst=False):
    print("=" * 65)
    print("🚦 Smart City IoT Traffic Sensor Simulator Active")
    print(f"📡 Target Endpoint: {target_url}")
    print(f"⏱️ Ingestion Interval: {interval} seconds")
    print(f"⚠️ Congestion Alert Rule: Vehicle Count > 500 OR Speed < 15 km/h")
    print("=" * 65)

    iteration = 0
    while True:
        iteration += 1
        sensor = random.choice(SENSORS)
        
        # Inject occasional congestion spike every few iterations
        should_spike = force_burst or (iteration % 4 == 0)
        payload = generate_sensor_reading(sensor, force_congestion=should_spike)

        try:
            res = requests.post(target_url, json=payload, timeout=5)
            if res.status_code == 201:
                result = res.json()
                if result.get("is_congested"):
                    print(f"🚨 [ALERT FIRED] {payload['sensor_id']} ({payload['road_name']}): "
                          f"Count={payload['vehicle_count']} | Speed={payload['avg_speed']} km/h "
                          f"| Occupancy={payload['road_occupancy']}% -> Reason: {result.get('alert_reason')}")
                else:
                    print(f"✅ [NORMAL FLOW] {payload['sensor_id']} ({payload['road_name']}): "
                          f"Count={payload['vehicle_count']} | Speed={payload['avg_speed']} km/h "
                          f"| Occupancy={payload['road_occupancy']}%")
            else:
                print(f"⚠️ Error {res.status_code}: {res.text}")
        except Exception as e:
            print(f"❌ Failed to reach endpoint {target_url}: {e}")

        time.sleep(interval)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Smart City IoT Traffic Simulator")
    parser.add_argument("--target", default="http://127.0.0.1:5000/api/ingest", help="Backend ingestion endpoint")
    parser.add_argument("--interval", type=float, default=3.0, help="Seconds between sensor readings")
    parser.add_argument("--burst", action="store_true", help="Continuously generate heavy traffic congestion")
    args = parser.parse_args()

    run_simulation(args.target, interval=args.interval, force_burst=args.burst)
