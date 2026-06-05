import pandas as pd
import re

# ––– Завдання 1 та 2. Завантаження та первинний аналіз даних –––
class DataLoader:
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None

    def load_data(self):
        try:
            self.df = pd.read_csv(self.filepath)
            return self.df
        except FileNotFoundError:
            print(f"Файл {self.filepath} не знайдено. Створіть тестовий файл для перевірки.")
            return pd.DataFrame()

    def basic_analysis(self):
        if self.df.empty: return
        print("--- Завдання 1. Первинний аналіз ---")
        print("Перші 5 рядків:\n", self.df.head())
        print("\nОстанні 5 рядків:\n", self.df.tail())
        
        rows, cols = self.df.shape
        print(f"\nКількість рядків: {rows}, Кількість стовпців: {cols}")
        
        mem_bytes = self.df.memory_usage(deep=True).sum()
        print(f"Обсяг пам'яті: {mem_bytes / (1024**2):.2f} MB")

        print("\n--- Завдання 2. Типи та пропуски ---")
        print("Типи даних:\n", self.df.dtypes)
        print("\nПропущені значення:\n", self.df.isnull().sum())
        print("Висновок: Дані успішно завантажені, типи визначені. Пропуски потребують уваги, якщо вони є.")


# ––– Завдання 3. Фільтрація даних –––
class DataFilter:
    def __init__(self, df):
        self.df = df

    def filter_vacancies(self):
        if self.df.empty: return
        print("\n--- Завдання 3. Фільтрація ---")
        
        # Перевірка наявності колонок (для уникнення помилок)
        cols = self.df.columns
        if 'Industry' in cols:
            cloud_jobs = self.df[self.df['Industry'] == 'Cloud Computing']
            print(f"Вакансій у Cloud Computing: {len(cloud_jobs)}")
            
        if 'Experience Level' in cols:
            senior_jobs = self.df[self.df['Experience Level'] == 'Senior']
            print(f"Вакансій рівня Senior: {len(senior_jobs)}")
            
        if 'Employment Type' in cols and 'Location' in cols:
            # Для прикладу візьмемо місто 'New York'
            ft_ny = self.df[(self.df['Employment Type'] == 'Full-Time') & (self.df['Location'] == 'New York')]
            print(f"Full-Time вакансій у New York: {len(ft_ny)}")


# ––– Завдання 4, 5, 6. Аналіз зарплат та створення нових ознак –––
class SalaryProcessor:
    def __init__(self, df):
        self.df = df

    # Допоміжна функція для витягування чисел з тексту "50000-70000"
    @staticmethod
    def extract_salaries(salary_str):
        if pd.isna(salary_str): return 0, 0
        nums = re.findall(r'\d+', str(salary_str).replace(',', ''))
        if len(nums) >= 2: return int(nums[0]), int(nums[1])
        elif len(nums) == 1: return int(nums[0]), int(nums[0])
        return 0, 0

    def process_salaries(self):
        if self.df.empty or 'Salary Range' not in self.df.columns: return
        
        # Створення числових колонок
        self.df[['Min_Salary', 'Max_Salary']] = self.df['Salary Range'].apply(
            lambda x: pd.Series(self.extract_salaries(x))
        )

        print("\n--- Завдання 4. Сортування за зарплатою ---")
        sorted_df = self.df.sort_values(by='Max_Salary', ascending=False)
        print("Топ-5 високооплачуваних вакансій (за макс. зарплатою):")
        print(sorted_df[['Job Title', 'Max_Salary']].head())

        print("\n--- Завдання 5. Групування за галузями ---")
        if 'Industry' in self.df.columns:
            ind_stats = self.df.groupby('Industry').agg(
                Кількість=('Job Title', 'count'),
                Середня_Мін_Зарплата=('Min_Salary', 'mean')
            ).sort_values(by='Середня_Мін_Зарплата', ascending=False)
            
            print(ind_stats.head())
            print(f"Найвища середня мін. зарплата у галузі: {ind_stats.index[0]}")

        print("\n--- Завдання 6. Категоризація зарплат (apply) ---")
        def categorize(max_sal):
            if max_sal <= 40000: return 'Low'
            elif 40000 < max_sal <= 70000: return 'Medium'
            else: return 'High'

        self.df['Salary Category'] = self.df['Max_Salary'].apply(categorize)
        print("Перевірка категоризації (перші 5 записів):")
        print(self.df[['Max_Salary', 'Salary Category']].head())


# ––– Завдання 7. Часовий аналіз –––
class TimeAnalyzer:
    def __init__(self, df):
        self.df = df

    def analyze_dates(self):
        if self.df.empty or 'Date Posted' not in self.df.columns: return
        print("\n--- Завдання 7. Часовий аналіз ---")
        
        self.df['Date Posted'] = pd.to_datetime(self.df['Date Posted'], errors='coerce')
        self.df['Year'] = self.df['Date Posted'].dt.year
        
        year_stats = self.df.groupby('Year')['Job Title'].count().sort_values(ascending=False)
        print("Кількість вакансій за роками:")
        print(year_stats)
        
        if not year_stats.empty:
            print(f"Висновок: Найактивнішим роком на ринку праці був {int(year_stats.index[0])} рік.")


# ––– ГОЛОВНИЙ БЛОК ВИКОНАННЯ –––
if __name__ == "__main__":
    filepath = 'Job opportunities.csv'
    
    # Створюємо об'єкти класів та послідовно викликаємо методи
    loader = DataLoader(filepath)
    df = loader.load_data()
    loader.basic_analysis()
    
    filter_obj = DataFilter(df)
    filter_obj.filter_vacancies()
    
    salary_obj = SalaryProcessor(df)
    salary_obj.process_salaries()
    
    time_obj = TimeAnalyzer(df)
    time_obj.analyze_dates()

