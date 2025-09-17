from product import Product
from database import DatabaseConnection

class ProductRepository:
    def __init__(self, connection: DatabaseConnection):
        self.connection = connection

    def create_product(self, product: Product) -> Product:
        conn = self.connection.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''
            INSERT INTO products (name, price, count, quality)
            VALUES (%s, %s, %s, %s)
            RETURNING id
            ''',
            (product.name, product.price, product.count, product.quality)
        )
        product.id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return product

    def get_all(self):
        conn = self.connection.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, price, count, quality FROM products ORDER BY id")
        rows = cursor.fetchall()
        products = []
        for row in rows:
            products.append(Product(
                id=row[0],
                name=row[1],
                price=row[2],
                count=row[3],
                quality=row[4]
            ))
        cursor.close()
        conn.close()
        return products

    def get_by_id(self, product_id: int):
        conn = self.connection.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, price, count, quality FROM products WHERE id = %s", (product_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return Product(
                id=row[0],
                name=row[1],
                price=row[2],
                count=row[3],
                quality=row[4]
            )
        return None

    def update_product(self, product: Product) -> Product:
        conn = self.connection.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''
            UPDATE products
            SET name = %s, price = %s, count = %s, quality = %s
            WHERE id = %s
            ''',
            (product.name, product.price, product.count, product.quality, product.id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return product

    def delete_product(self, product_id: int) -> bool:
        conn = self.connection.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''
            DELETE FROM products WHERE id = %s
            ''',
            (product_id,)
        )
        conn.commit()
        deleted = cursor.rowcount
        cursor.close()
        conn.close()
        return deleted > 0