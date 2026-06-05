import sqlite3
import pandas as pd
import re

# ––– Завдання 1 та 7. Підготовка даних та управління з'єднанням –––
class DatabaseManager:
    def __init__(self, db_name, csv_path):
        self.db_name = db_name
        self.csv_path = csv_path
        self.conn = None

    def setup_database(self):
        try:
            # Завантаження CSV
            df = pd.read_csv(self.csv_path)
            
            # Підготовка: витягуємо середнє числове значення зарплати для SQL-аналітики
            def extract_avg_salary(val):
                nums = re.findall(r'\d+', str(val).replace(',', ''))
                if len(nums) == 2: return (int(nums[0]) + int(nums[1])) / 2
                elif len(nums) == 1: return int(nums[0])
                return 0
                
            df['Numeric_Salary'] = df['Salary Range'].apply(extract_avg_salary)
            
            # Підготовка: конвертуємо дату, щоб легко дістати рік
            df['Date Posted'] = pd.to_datetime(df['Date Posted'], errors='coerce')
            df['Year'] = df['Date Posted'].dt.year

            # Створення підключення та таблиці
            self.conn = sqlite3.connect(self.db_name)
            df.to_sql('jobs', self.conn, if_exists='replace', index=False)
            print("База даних успішно створена, дані завантажено.")
            return True
        except FileNotFoundError:
            print(f"Помилка: Файл {self.csv_path} не знайдено!")
            return False

    def close_connection(self):
        if self.conn:
            self.conn.close()
            print("З'єднання з базою даних закрито.")

    def run_query(self, query):
        # Виконання SQL-запиту та повернення результату як DataFrame
        return pd.read_sql(query, self.conn)


# ––– Завдання 2–6. Виконання SQL запитів –––
class SQLAnalyzer:
    def __init__(self, db_manager):
        self.db = db_manager

    def execute_task_2(self):
        print("\n--- Завдання 2. Основні запити SQL ---")
        print("Перші 5 вакансій (LIMIT використано для економії місця):")
        print(self.db.run_query("SELECT `Job Title`, Company FROM jobs LIMIT 5;"))
        
        print("\nВакансії з вимогою SQL:")
        print(self.db.run_query("SELECT `Job Title`, `Required Skills` FROM jobs WHERE `Required Skills` LIKE '%SQL%' LIMIT 5;"))
        
        print("\nУнікальні Location та Company (перші 5):")
        print(self.db.run_query("SELECT DISTINCT Location, Company FROM jobs LIMIT 5;"))

    def execute_task_3(self):
        print("\n--- Завдання 3. Аналітичні запити ---")
        print("Середня зарплата за рівнем досвіду:")
        print(self.db.run_query("SELECT `Experience Level`, AVG(Numeric_Salary) as Avg_Salary FROM jobs GROUP BY `Experience Level`;"))
        
        print("\nКількість вакансій за рівнем досвіду:")
        print(self.db.run_query("SELECT `Experience Level`, COUNT(*) as Vacancies_Count FROM jobs GROUP BY `Experience Level`;"))
        
        print("\nМінімальна та максимальна зарплата серед усіх:")
        print(self.db.run_query("SELECT MIN(Numeric_Salary) as Min_Sal, MAX(Numeric_Salary) as Max_Sal FROM jobs WHERE Numeric_Salary > 0;"))

    def execute_task_4(self):
        print("\n--- Завдання 4. Використання агрегатних функцій ---")
        print("Кількість вакансій у кожній індустрії (де зарплата > 50000):")
        print(self.db.run_query("SELECT Industry, COUNT(*) as Count FROM jobs WHERE Numeric_Salary > 50000 GROUP BY Industry;"))
        
        print("\nСередня зарплата для кожної індустрії:")
        print(self.db.run_query("SELECT Industry, AVG(Numeric_Salary) as Avg_Sal FROM jobs GROUP BY Industry LIMIT 5;"))

    def execute_task_5(self):
        print("\n--- Завдання 5. Складніші запити ---")
        print("Кількість вакансій за містом та досвідом (фрагмент):")
        print(self.db.run_query("SELECT Location, `Experience Level`, COUNT(*) as Count FROM jobs GROUP BY Location, `Experience Level` LIMIT 5;"))
        
        print("\nКількість вакансій за індустрією та типом роботи (фрагмент):")
        print(self.db.run_query("SELECT Industry, `Employment Type`, COUNT(*) as Count FROM jobs GROUP BY Industry, `Employment Type` LIMIT 5;"))

    def execute_task_6_bonus(self):
        print("\n--- Завдання 6. Додаткові запити ---")
        print("5 вакансій з найвищою зарплатою:")
        print(self.db.run_query("SELECT `Job Title`, Company, Numeric_Salary FROM jobs ORDER BY Numeric_Salary DESC LIMIT 5;"))
        
        print("\nКомпанії з найбільшою кількістю вакансій у 2023 році:")
        print(self.db.run_query("SELECT Company, COUNT(*) as Total_2023 FROM jobs WHERE Year = 2023 GROUP BY Company ORDER BY Total_2023 DESC LIMIT 5;"))


# ––– ГОЛОВНИЙ БЛОК ВИКОНАННЯ –––
if __name__ == "__main__":
    # Налаштування бази даних та файлу
    db_manager = DatabaseManager('it_jobs.db', 'Job opportunities.csv')
    
    if db_manager.setup_database():
        analyzer = SQLAnalyzer(db_manager)
        
        analyzer.execute_task_2()
        analyzer.execute_task_3()
        analyzer.execute_task_4()
        analyzer.execute_task_5()
        analyzer.execute_task_6_bonus()
        
        # Завдання 7: Закриття з'єднання
        print("\n--- Завдання 7 ---")
        db_manager.close_connection()

