from database import DatabaseConfig, DatabaseConnection
from migration import MigrationManager
from repository import ProductRepository
from service import ProductService
from fastapi import FastAPI, HTTPException
from products import Product

# Инициализация
db_config = DatabaseConfig(
    'ozonshopdb',      # Название БД
    'postgres',        # Имя пользователя
    'postgres',        # Пароль
    '123Secret_a',     # Пароль (проверьте корректность!)
    5432               # Порт
)
db_connection = DatabaseConnection(db_config)

# Миграции
migration_manager = MigrationManager(db_config)
migration_manager.create_tables()

# Репозиторий и сервис
repository = ProductRepository(db_connection)
service = ProductService(repository)

app = FastAPI(title="Ozon Shop API")

@app.get("/")
async def root():
    return {"message": "Добро пожаловать в API магазина Ozon!"}

@app.get("/products")
async def get_products():
    try:
        return service.get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")

@app.post("/products")
async def create_product(product_data: dict):
    try:
        # Валидация входных данных
        required_fields = ["name", "price", "count", "quality"]
        for field in required_fields:
            if field not in product_data:
                raise HTTPException(status_code=400, detail=f"Не указано поле: {field}")
        product = Product(
            name=product_data['name'],
            price=product_data['price'],
            count=product_data['count'],
            quality=product_data['quality']
        )
        created_product = service.create_product(product)
        return created_product
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при добавлении товара: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)