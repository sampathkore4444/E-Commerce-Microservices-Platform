from fastapi import APIRouter, Query
from app.services.indexing_service import search_products
from typing import List, Dict


router = APIRouter()


@router.get("/search", response_model=List[Dict])
def search(
    query: str = Query(
        "", min_length=1, description="Search query for products and promotions"
    ),
    category_id: int = Query(None, description="Optional category filter"),
    tag_id: int = Query(None, description="Optional tag filter"),
    min_price: float = Query(None, description="Optional minimum price filter"),
    max_price: float = Query(None, description="Optional maximum price filter"),
    in_stock: bool = Query(False, description="Optional stock availability filter"),
):
    results = search_products(
        query,
        category_id=category_id,
        tag_id=tag_id,
        min_price=min_price,
        max_price=max_price,
        in_stock=in_stock,
    )
    return {"results": results}


"""
Front-end or Product API can call this endpoint

Supports filtered, full-text search

This code defines a search endpoint for the search and indexing service in an e-commerce microservices platform.
The endpoint accepts various query parameters for searching products and promotions, and returns a list of matching results

"""
