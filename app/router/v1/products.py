from fastapi import APIRouter, HTTPException, Query
from app.models.models import ProductCreate, ProductResponse, ProductUpdate
from app.services.product_service import product_service

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", response_model=ProductResponse, status_code=201)
async def create_product(product: ProductCreate):
    """
    Create a new product.
    
    - **name**: Product name (required)
    - **description**: Product description (optional)
    - **price**: Product price (must be > 0)
    - **in_stock**: Availability status (default: true)
    """
    return await product_service.create_product(product)

@router.get("/", response_model=list[ProductResponse])
async def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    in_stock_only: bool = Query(False, description="Filter to show only in-stock products")
):
    """
    Get all products with pagination and optional filtering.
    """
    return await product_service.get_all_products(
        skip=skip, 
        limit=limit, 
        in_stock_only=in_stock_only
    )

@router.get("/search", response_model=list[ProductResponse])
async def search_products(
    q: str = Query(..., min_length=1, description="Search query")
):
    """
    Search products by name or description.
    """
    return await product_service.search_products(q)

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int):
    """
    Get a specific product by ID.
    """
    product = await product_service.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found")
    return product

@router.patch("/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, product_update: ProductUpdate):
    """
    Update a product's information.
    Only provided fields will be updated.
    """
    product = await product_service.update_product(product_id, product_update)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found")
    return product

@router.delete("/{product_id}", status_code=204)
async def delete_product(product_id: int):
    """
    Delete a product.
    """
    success = await product_service.delete_product(product_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found")
    return None
