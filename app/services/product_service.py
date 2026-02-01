from datetime import datetime
from app.models.models import ProductCreate, ProductResponse, ProductUpdate

class ProductService:
    """
    Product service handling business logic for product operations.
    This demonstrates CRUD operations pattern.
    """
    
    def __init__(self):
        # Simulated in-memory database
        self.products_db: list[ProductResponse] = []
        self.next_id = 1
    
    async def create_product(self, product: ProductCreate) -> ProductResponse:
        """Create a new product"""
        new_product = ProductResponse(
            id=self.next_id,
            name=product.name,
            description=product.description,
            price=product.price,
            in_stock=product.in_stock,
            created_at=datetime.now()
        )
        
        self.products_db.append(new_product)
        self.next_id += 1
        return new_product
    
    async def get_product(self, product_id: int) -> ProductResponse | None:
        """Get a product by ID"""
        return next((p for p in self.products_db if p.id == product_id), None)
    
    async def get_all_products(
        self, 
        skip: int = 0, 
        limit: int = 100, 
        in_stock_only: bool = False
    ) -> list[ProductResponse]:
        """Get all products with optional filtering"""
        products = self.products_db
        
        if in_stock_only:
            products = [p for p in products if p.in_stock]
        
        return products[skip : skip + limit]
    
    async def update_product(
        self, 
        product_id: int, 
        product_update: ProductUpdate
    ) -> ProductResponse | None:
        """Update a product's information"""
        product = await self.get_product(product_id)
        if not product:
            return None
        
        # Update only provided fields
        if product_update.name is not None:
            product.name = product_update.name
        if product_update.description is not None:
            product.description = product_update.description
        if product_update.price is not None:
            product.price = product_update.price
        if product_update.in_stock is not None:
            product.in_stock = product_update.in_stock
        
        return product
    
    async def delete_product(self, product_id: int) -> bool:
        """Delete a product"""
        product = await self.get_product(product_id)
        if not product:
            return False
        
        self.products_db.remove(product)
        return True
    
    async def search_products(self, query: str) -> list[ProductResponse]:
        """Search products by name or description"""
        query_lower = query.lower()
        return [
            p for p in self.products_db
            if query_lower in p.name.lower() or 
               (p.description and query_lower in p.description.lower())
        ]

# Singleton instance
product_service = ProductService()
