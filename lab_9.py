import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import re

# ––– Завдання: Підготовка середовища та завантаження даних –––
class DataLoader:
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None

    def load_and_prepare(self):
        """Правильна назва методу: load_and_prepare"""
        try:
            self.df = pd.read_csv(self.filepath)
            
            # Створення колонки Average Salary
            def get_avg_salary(val):
                nums = re.findall(r'\d+', str(val).replace(',', ''))
                if len(nums) == 2: return (int(nums[0]) + int(nums[1])) / 2
                elif len(nums) == 1: return int(nums[0])
                return 0
                
            self.df['Average Salary'] = self.df['Salary Range'].apply(get_avg_salary)
            
            # Перетворення дати
            self.df['Date Posted'] = pd.to_datetime(self.df['Date Posted'], errors='coerce')
            self.df['Year'] = self.df['Date Posted'].dt.year
            
            print("[Система] Дані успішно завантажено та підготовлено.")
            return self.df
        except FileNotFoundError:
            print(f"[Помилка] Файл {self.filepath} не знайдено.")
            return None


# ––– Завдання: Побудова графіків Seaborn –––
class DataVisualizer:
    def __init__(self, df):
        self.df = df
        sns.set_theme(style="whitegrid")

    def show_all_plots(self):
        """Метод для послідовного виводу всіх графіків."""
        
        # 1. Barplot
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Experience Level', y='Average Salary', data=self.df, palette='viridis', errorbar=None)
        plt.title('Середня зарплата за рівнем досвіду')
        plt.show()

        # 2. Boxplot
        plt.figure(figsize=(12, 6))
        sns.boxplot(x='Industry', y='Average Salary', data=self.df, palette='Set2')
        plt.title('Розподіл зарплат за галузями')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

        # 3. Heatmap
        plt.figure(figsize=(10, 6))
        pivot_table = pd.crosstab(self.df['Experience Level'], self.df['Industry'])
        sns.heatmap(pivot_table, annot=True, cmap='Blues', fmt='d', linewidths=0.5)
        plt.title('Кількість вакансій: Досвід vs Галузь')
        plt.show()

        # 4. Scatterplot
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='Year', y='Average Salary', hue='Experience Level', data=self.df, palette='deep', alpha=0.7)
        plt.title('Тенденція зарплат за роками')
        plt.show()

        # 5. Pairplot
        plot_data = self.df[['Year', 'Average Salary', 'Experience Level']].dropna()
        sns.pairplot(plot_data, hue='Experience Level', palette='bright', diag_kind='kde')
        plt.show()


# ––– ГОЛОВНИЙ БЛОК ВИКОНАННЯ –––
if __name__ == "__main__":
    loader = DataLoader('Job opportunities.csv')
    # ВИПРАВЛЕНО: викликаємо метод з правильною назвою
    df = loader.load_and_prepare()
    
    if df is not None:
        visualizer = DataVisualizer(df)
        visualizer.show_all_plots()
