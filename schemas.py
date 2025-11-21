"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List

# Example schemas (you can keep or ignore if not used by your app)

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Bakery app schemas

class BakeryItem(BaseModel):
    """
    Bakery items available for sale
    Collection name: "bakeryitem"
    """
    name: str = Field(..., description="Item name, e.g., Croissant")
    description: Optional[str] = Field(None, description="Short description of the item")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Category, e.g., Bread, Pastry, Cake, Cookie")
    image_url: Optional[str] = Field(None, description="Image URL")
    is_available: bool = Field(True, description="Whether this item is currently available")

class OrderItem(BaseModel):
    item_id: str = Field(..., description="ID of the bakery item")
    quantity: int = Field(..., ge=1, description="Quantity ordered")

class Order(BaseModel):
    """
    Customer orders
    Collection name: "order"
    """
    customer_name: str = Field(..., description="Customer full name")
    customer_phone: str = Field(..., description="Contact phone number")
    items: List[OrderItem] = Field(..., description="List of items in the order")
    notes: Optional[str] = Field(None, description="Special instructions or notes")
