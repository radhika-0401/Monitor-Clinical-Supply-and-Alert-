from flask import Flask, jsonify, render_template
import serial
import time

app = Flask(__name__)
ser = serial.Serial('COM3', 9600, timeout=1)  # Change COM3 to your port

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/data')
def get_data():
    if ser.in_waiting > 0:
        try:
            line = ser.readline().decode('utf-8').strip()
            print("Received:", line)  # Debugging purpose
            data = eval(line)  # Convert JSON string to dictionary
            return jsonify(data)
        except Exception as e:
            print("Error:", e)
            return jsonify({})
    return jsonify({})

if __name__ == '__main__':
    time.sleep(2)  # Give serial connection time to start
    app.run(debug=True, host='0.0.0.0', port=5000)
