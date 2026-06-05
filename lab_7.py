import asyncio
import websockets

class WebSocketClient:
    """Клас для асинхронної взаємодії з WebSocket сервером."""
    
    def __init__(self):
        self.websocket = None

    async def connect(self, url):
        """Встановлює WebSocket-з'єднання за вказаною адресою з обробкою помилок."""
        try:
            self.websocket = await websockets.connect(url)
            print(f"[Система] Успішно підключено до: {url}")
        except Exception as e:
            print(f"[Помилка] Не вдалося підключитися до сервера: {e}")
            self.websocket = None

    async def send_message(self, message):
        """Надсилає повідомлення серверу."""
        # Перевіряємо лише наявність об'єкта websocket
        if self.websocket:
            try:
                await self.websocket.send(message)
                print(f"[Клієнт -> Сервер] Відправлено: {message}")
            except Exception as e:
                print(f"[Помилка] Збій під час відправки повідомлення: {e}")
        else:
            print("[Помилка] Немає активного з'єднання для відправки.")

    async def receive_message(self):
        """Отримує повідомлення від сервера."""
        if self.websocket:
            try:
                message = await self.websocket.recv()
                print(f"[Сервер -> Клієнт] Отримано: {message}")
                return message
            except Exception as e:
                print(f"[Помилка] Збій під час отримання повідомлення: {e}")
                return None
        else:
            print("[Помилка] Немає активного з'єднання для отримання даних.")
            return None

    async def close_connection(self):
        """Закриває WebSocket-з'єднання."""
        if self.websocket:
            await self.websocket.close()
            self.websocket = None # Очищаємо об'єкт після закриття
            print("[Система] З'єднання закрито.")
        else:
            print("[Система] З'єднання вже закрите або не було встановлене.")


# ––– ГОЛОВНИЙ БЛОК ВИКОНАННЯ –––
async def main():
    # Використовуємо публічний echo-сервер для тестування
    test_url = "wss://ws.postman-echo.com/raw"
    client = WebSocketClient()

    # 1. Встановлення з'єднання
    await client.connect(test_url)

    # 2. Відправка та отримання першого повідомлення
    await client.send_message("Привіт, WebSocket сервер! Це перевірка зв'язку.")
    await client.receive_message()

    # 3. Відправка та отримання другого повідомлення
    await asyncio.sleep(1)
    await client.send_message("Передача даних у реальному часі працює чудово.")
    await client.receive_message()

    # 4. Закриття з'єднання
    await client.close_connection()

    # 5. Перевірка обробки помилок
    await client.send_message("Це повідомлення не має відправитись.")

if __name__ == "__main__":
    # Запуск асинхронного циклу
    asyncio.run(main())
