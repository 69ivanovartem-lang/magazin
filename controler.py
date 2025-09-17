from database import DatabaseConfig, DatabaseConnection
from migrations import MigrationManager
from repository import OZONRepository
from service import OZONService
from fastapi import FastAPI, HTTPException
from OZON import OZON

#Initialize
## DB config
db_config= DatabaseConfig(
    'OZONsdb',
    'postgres',
    'postgres',
    '123Secret_a',
    5432
)
db_connection = DatabaseConnection(db_config)
## Migrations
migration_manager = MigrationManager(db_config)
migration_manager.create_tables()
# Repository and Service
repository = OZONRepository(db_connection)
service = OZONService(repository)

app = FastAPI(
    title="OZON API"
)

@app.get("/")
async def root():
    return {"message":"Hello from FastAPI"}

@app.get("/OZONs")
async def get_OZON():
    try:
        return service.get_all()
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Ошибка при получении полётов: {str(e)}")

@app.post("/OZONs")
async def create_OZON(OZON_data: dict):
    try:
        #Validation
        required_fields = ["price","plane"]
        for field in required_fields:
            if field not in OZON_data:
                raise HTTPException(status_code=400,detail=f"Отсутствует обязательное поле {field}")
        
        OZON = OZON(
            price=OZON_data['price'],
            plane=OZON_data['plane']
        )

        created_OZON = service.create_OZON(OZON)
        return created_OZON

    except Exception as e:
        return HTTPException(status_code=500, detail=f"Ошибка при добавлении полёта: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0", port=8080)