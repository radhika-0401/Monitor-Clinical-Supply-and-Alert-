
#include <DHT.h>
#include <DHT_U.h>

#define DHTPIN 12
#define DHTTYPE DHT11 

DHT dht(DHTPIN, DHTTYPE);

int flameSensorPin = 2;
const int trigPin = 9;
const int echoPin = 10;
long travelTime;
int distance;

void setup() {
  pinMode(flameSensorPin, INPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  int flameDetected = digitalRead(flameSensorPin);
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  // Ultrasonic Sensor Distance Measurement
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  travelTime = pulseIn(echoPin, HIGH);
  distance = travelTime * 0.034 / 2;

  // **Output JSON Format (Corrected)**
  Serial.print("{\"flame\":");
  Serial.print(flameDetected == LOW ? "1" : "0");  
  Serial.print(",\"humidity\":");
  Serial.print(humidity, 2);  
  Serial.print(",\"temperature\":");
  Serial.print(temperature, 2);
  Serial.print(",\"distance\":");
  Serial.print(distance);
  Serial.println("}\n");  // **Ensure proper end-of-line**

  delay(1000);
}
