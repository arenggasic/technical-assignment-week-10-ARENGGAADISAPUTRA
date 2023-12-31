import time
import Adafruit_DHT
import requests

# Konfigurasi sensor DHT22
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4  # Ganti dengan pin GPIO tempat Anda menghubungkan sensor DHT22

# Konfigurasi Ubidots
UBIDOTS_TOKEN = "BBFF-2jXFcArgZADJPrXdNDezHs4Q95gudr"
DEVICE_LABEL = "suhu"  # Ganti dengan label device yang Anda buat di Ubidots

def get_humidity():
    humidity, _ = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    return humidity

def send_humidity_to_ubidots(humidity):
    url = f"https://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_LABEL}"
    headers = {"X-Auth-Token": UBIDOTS_TOKEN, "Content-Type": "application/json"}

    payload = {
        "humidity": humidity
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            print("Humidity data successfully sent to Ubidots")
        else:
            print("Failed to send humidity data to Ubidots")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    try:
        while True:
            humidity = get_humidity()
            if humidity is not None:
                print(f"Humidity: {humidity:.2f}%")
                send_humidity_to_ubidots(humidity)
            else:
                print("Failed to retrieve humidity data from the sensor.")
            time.sleep(0.1)  # Ubah angka 10 ke interval yang diinginkan (dalam detik)
    except KeyboardInterrupt:
        print("Terminated by the user")