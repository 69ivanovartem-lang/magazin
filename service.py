from repository import ProductRepository
from products import Product

class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def create_product(self, product: Product) -> Product:
        return self.repository.create_product(product)

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, product_id: int):
        return self.repository.get_by_id(product_id)

    def update_product(self, product: Product) -> Product:
        return self.repository.update_product(product)

    def delete_product(self, product_id: int) -> bool:
        return self.repository.delete_product(product_id)