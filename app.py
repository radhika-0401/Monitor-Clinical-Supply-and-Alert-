from flask import Flask, render_template, jsonify
import serial

app = Flask(__name__)

# Change COM port for Windows or /dev/ttyUSBx for Linux/Mac
ser = serial.Serial("COM7", 9600, timeout=1)  # Change COM5 to your port

@app.route('/')
def home():
    return render_template('dashboard.html')

@app.route('/data')
def get_sensor_data():
    if ser.in_waiting:
        try:
            data = ser.readline().decode('utf-8').strip()
            print("Raw Serial Data:", data)  # Debugging

            if data.startswith("{") and data.endswith("}"):
                sensor_data = eval(data)  # Convert JSON string to dictionary
                return jsonify(sensor_data)
        except Exception as e:
            print("Error:", e)
    
    return jsonify({"flame": 0, "humidity": 0, "temperature": 0, "distance": 0})  # Default values

if __name__ == '__main__':
    app.run(debug=True)

