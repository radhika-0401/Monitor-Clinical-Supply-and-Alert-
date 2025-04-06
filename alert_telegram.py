import serial
import time
import requests
import json

# Set your port and baud rate
arduino = serial.Serial('COM7', 9600)  # Change COM3 if needed
time.sleep(2)  # Wait for Arduino to boot

# Telegram Bot config
BOT_TOKEN = '8069184372:AAEX6ia-9AvHV04yrhhegFvn3L1Cq50fv4Q'
CHAT_ID = '6325331215'

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {'chat_id': CHAT_ID, 'text': message}
    try:
        requests.post(url, data=data)
    except:
        print("Error sending Telegram message")

while True:
    try:
        line = arduino.readline().decode().strip()
        print(f"Sensor Value: {line}")
        
        if line:
            try:
                data = json.loads(line)  # Parse JSON data
                
                # **Check Conditions for Alerts**
                if data.get("flame") == 1:
                    send_telegram("🔥 Flame detected! Immediate action required!")
                
                if data.get("Gas Leakage") == 1:
                    send_telegram("⚠️ Gas leakage detected! Take precautions!")

                if data.get("Storage Temp too high") == 1:
                    send_telegram(f"🌡️ High storage temperature detected: {data.get('temperature')}°C!")
             
             
            except json.JSONDecodeError:
                print("Error: Received data is not valid JSON")
  
        if line.isdigit():
            value = int(line)
            if value > 800:
                send_telegram(f"🚨 Sensor Alert! Value = {value}")
                time.sleep(10)  # Avoid spamming

    except Exception as e:
        print("Error:", e)