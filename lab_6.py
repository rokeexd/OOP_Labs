import requests

class RestClient:
    """Клас для виконання HTTP-запитів до REST API."""
    
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')

    def get(self, endpoint):
        """Виконує HTTP GET-запит та повертає отримані дані."""
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.get(url)
            # Перевіряємо успішність запиту (статус 200 OK)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"[Помилка GET] Сервер повернув статус-код: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"[Помилка з'єднання GET] {e}")
            return None

    def post(self, endpoint, data):
        """Виконує HTTP POST-запит з переданими даними у форматі JSON."""
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.post(url, json=data)
            # Для POST успішним статусом зазвичай є 201 Created (або 200 OK)
            if response.status_code in (200, 201):
                return response.json()
            else:
                print(f"[Помилка POST] Сервер повернув статус-код: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"[Помилка з'єднання POST] {e}")
            return None


# ––– ГОЛОВНИЙ БЛОК ВИКОНАННЯ –––
if __name__ == "__main__":
    # Ініціалізація клієнта з базовим URL тестового API JSONPlaceholder
    api_client = RestClient("https://jsonplaceholder.typicode.com")

    print("--- 1. Тестування методу GET ---")
    # Отримуємо список постів (звертаємось до endpoint 'posts')
    posts_data = api_client.get("posts")
    
    if posts_data:
        print(f"Успішно отримано постів: {len(posts_data)}")
        print("Перший пост із масиву:")
        print(posts_data[0])

    print("\n--- 2. Тестування методу POST ---")
    # Формуємо словник з даними для нового запису
    new_post = {
        "title": "Тестовий заголовок для лаби",
        "body": "Це текст нового поста, надісланий через наш RestClient.",
        "userId": 999
    }
    
    # Відправляємо POST-запит
    created_post = api_client.post("posts", new_post)
    
    if created_post:
        print("Запис успішно створено на сервері. Відповідь сервера:")
        print(created_post)
