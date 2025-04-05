from flask import Flask, render_template
from flask_socketio import SocketIO
import random
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


TELEGRAM_BOT_TOKEN = "7271857677:AAEYeNI6mptq5iHMSNjUr41ynjtjlMqP2CY"
CHAT_ID = "6325331215"
message="Test Alertttttttttt"

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"6325331215": CHAT_ID, "text": message}
    requests.post(url, json=payload)

@app.route('/')
def index():
    return render_template('dashboard.html')
    
def get_sensor_data():
    while True:
    # Example sensor values (replace with real data from Arduino)
      sensor_data = {
          "oxygen": random.randint(80,100),  
          "temperature": random.randint(25,45),  
          "acceleration": random.randint(0,100),  
          "flame": random.uniform(-5,5)  
    }
    socketio.emit('update_data',sensor_data)
    time.sleep(2)

    # **Trigger Alerts Based on Thresholds**
   
    if sensor_data["temperature"] > 40:
        send_telegram_alert("🔥 High Temperature Alert! Risk of fire!")
    if sensor_data["flame"] > 50:
        send_telegram_alert("🔥 Flame Detected! Possible Fire Hazard!")
  

    return jsonify(sensor_data)
    
def manual_alert():
    send_telegram_alert("🚨 Manual Alert Triggered from Dashboard!")
    return jsonify({"message": "Alert sent!"})

#def generate_sensor_data():
  #  while True:
    #    sensor_value = random.randint(90, 100)  # Simulate real sensor data
      #  socketio.emit('update_sensor', {'value': sensor_value})  # Send data to frontend
        #time.sleep(2)  # Update every 2 seconds

@socketio.on('connect')
def handle_connect():
    socketio.start_background_task(get_sensor_data)

if __name__ == '__main__':
    socketio.run(app, debug=True)

