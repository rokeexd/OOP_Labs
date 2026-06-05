import asyncio
import requests
import websockets
import paho.mqtt.client as mqtt
import time
import json

# ––– 1. Клас для роботи з REST API –––
class RestClient:
    @staticmethod
    def get_data(url):
        """Отримує дані через HTTP GET запит."""
        print(f"\n[REST] Відправка GET-запиту до {url}...")
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                print("[REST] Дані успішно отримано.")
                return data
            print(f"[REST] Помилка: {response.status_code}")
        except Exception as e:
            print(f"[REST] Помилка з'єднання: {e}")
        return None

# ––– 2. Клас для роботи з WebSocket –––
class WebSocketClient:
    async def process_data(self, url, data):
        """Відправляє дані на WebSocket сервер і отримує відповідь."""
        print(f"\n[WebSocket] Підключення до {url}...")
        try:
            async with websockets.connect(url) as ws:
                message = json.dumps(data)
                print(f"[WebSocket -> Сервер] Відправка даних...")
                await ws.send(message)
                
                response = await ws.recv()
                print(f"[Сервер -> WebSocket] Дані успішно повернулися.")
                return response
        except Exception as e:
            print(f"[WebSocket] Помилка: {e}")
            return None

# ––– 3. Клас для роботи з MQTT –––
class MQTTClient:
    def __init__(self, broker, port):
        self.broker = broker
        self.port = port
        # Створюємо клієнта (для нових версій paho-mqtt використовується CallbackAPIVersion, 
        # але для зворотної сумісності залишаємо базовий виклик)
        self.client = mqtt.Client()
        self.client.on_connect = self._on_connect
        self.client.on_publish = self._on_publish

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("[MQTT] Успішно підключено до брокера.")
        else:
            print(f"[MQTT] Помилка підключення, код: {rc}")

    def _on_publish(self, client, userdata, mid):
        print(f"[MQTT] Повідомлення успішно опубліковано на брокері.")

    def connect(self):
        """Підключення до брокера та запуск фонового циклу."""
        print(f"\n[MQTT] Спроба підключення до {self.broker}:{self.port}...")
        self.client.connect(self.broker, self.port, keepalive=60)
        self.client.loop_start()
        time.sleep(1) # Даємо час на встановлення з'єднання

    def publish(self, topic, message):
        """Публікація повідомлення у задану тему."""
        print(f"[MQTT -> Брокер] Публікація в тему '{topic}'...")
        result = self.client.publish(topic, message, qos=0, retain=False)
        result.wait_for_publish()

    def disconnect(self):
        """Відключення від брокера."""
        time.sleep(1)
        self.client.disconnect()
        self.client.loop_stop()
        print("[MQTT] Відключено від брокера.")


# ––– ГОЛОВНИЙ БЛОК ВИКОНАННЯ (Інтеграція) –––
async def main():
    # Налаштування URL-адрес та брокера
    rest_url = "https://jsonplaceholder.typicode.com/posts/1" # Тестовий пост
    ws_url = "wss://ws.postman-echo.com/raw"                  # Echo-сервер
    mqtt_broker = "broker.hivemq.com"                         # Публічний брокер
    mqtt_topic = "student/lab5/integration_test"              # Унікальна тема

    print("=== ЗАПУСК ІНТЕГРОВАНОЇ СИСТЕМИ (REST -> WS -> MQTT) ===")

    # Крок 1. Отримання даних через REST API
    rest_client = RestClient()
    raw_data = rest_client.get_data(rest_url)
    
    if not raw_data:
        return

    # Залишаємо лише заголовок для зручності
    payload = {"source": "REST API", "title": raw_data.get("title")}

    # Крок 2. Передача даних через WebSocket
    ws_client = WebSocketClient()
    processed_data = await ws_client.process_data(ws_url, payload)

    if not processed_data:
        return

    # Крок 3. Публікація фінальних даних через MQTT
    mqtt_client = MQTTClient(mqtt_broker, 1883)
    mqtt_client.connect()
    
    mqtt_client.publish(mqtt_topic, processed_data)
    
    mqtt_client.disconnect()
    print("\n=== КОНВЕЄР УСПІШНО ЗАВЕРШЕНО ===")

if __name__ == "__main__":
    # Запуск асинхронного циклу
    asyncio.run(main())
