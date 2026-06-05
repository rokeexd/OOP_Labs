import asyncio
from sqlalchemy import Column, Integer, String, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.future import select

# ––– Налаштування підключення та моделі БД –––
DATABASE_URL = "sqlite+aiosqlite:///network.db"
Base = declarative_base()

# Завдання: Створити базу даних та таблицю nodes
class Node(Base):
    __tablename__ = 'nodes'
    id = Column(Integer, primary_key=True)
    ip_address = Column(String, unique=True, nullable=False)
    status = Column(String, default="unknown")

# Створення асинхронного рушія та фабрики сесій
engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class NetworkDatabaseManager:
    """Клас для управління асинхронною взаємодією з базою даних вузлів"""
    
    @staticmethod
    async def create_tables():
        # Створення таблиці
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            
    @staticmethod
    async def reset_nodes():
        # Очищення таблиці перед новим запуском, щоб уникнути дублікатів
        async with AsyncSessionLocal() as session:
            await session.execute(text("DELETE FROM nodes"))
            await session.commit()

    @staticmethod
    async def add_nodes(count=15):
        # Завдання: Додавання 10-15 вузлів у базу
        async with AsyncSessionLocal() as session:
            nodes = [Node(ip_address=f"192.168.1.{i}", status="unknown") for i in range(1, count + 1)]
            session.add_all(nodes)
            await session.commit()
            print(f"[Система] Успішно додано {count} вузлів.")

    @staticmethod
    async def get_nodes(label="Поточний список вузлів"):
        # Завдання: Асинхронна функція для отримання списку вузлів
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Node))
            nodes = result.scalars().all()
            print(f"\n--- {label} ---")
            for node in nodes:
                print(f"ID: {node.id:02d} | IP: {node.ip_address:<15} | Статус: {node.status}")
            return nodes

    @staticmethod
    async def monitor_nodes():
        # Завдання: Асинхронна система збору статусів (імітація мережевих запитів)
        print("\n[Моніторинг] Початок опитування вузлів...")
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Node))
            nodes = result.scalars().all()
            
            for node in nodes:
                # Імітація мережевої затримки для кожного вузла
                await asyncio.sleep(0.1) 
                
                # Логіка зміни статусу: парні IP - offline, непарні - active
                last_octet = int(node.ip_address.split('.')[-1])
                node.status = "offline" if last_octet % 2 == 0 else "active"
                
            # Завдання: Зберігати отримані дані у базі
            await session.commit()
        print("[Моніторинг] Опитування завершено. Статуси оновлено в БД.")


# ––– ГОЛОВНИЙ БЛОК ВИКОНАННЯ –––
async def main():
    manager = NetworkDatabaseManager()
    
    # 1. Підготовка БД
    await manager.create_tables()
    await manager.reset_nodes()
    
    # 2. Додавання початкових даних
    await manager.add_nodes(10)
    
    # 3. Виведення списку ДО моніторингу
    await manager.get_nodes("Вузли ДО моніторингу")
    
    # 4. Запуск імітації опитування та оновлення статусів
    await manager.monitor_nodes()
    
    # 5. Виведення списку ПІСЛЯ моніторингу
    await manager.get_nodes("Вузли ПІСЛЯ оновлення статусів")

if __name__ == "__main__":
    # Запуск асинхронного циклу подій
    asyncio.run(main())
