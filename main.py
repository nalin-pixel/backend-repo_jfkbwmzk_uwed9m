import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from database import db, create_document, get_documents
from schemas import BakeryItem, Order

app = FastAPI(title="Bakery API", description="Backend for a modern bakery website")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Bakery backend is running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["connection_status"] = "Connected"
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"
    return response

# Seed default bakery items if collection is empty
@app.post("/api/seed")
def seed_bakery_items():
    try:
        existing = get_documents("bakeryitem", {}, limit=1)
        if existing:
            return {"status": "ok", "message": "Items already seeded"}
        samples = [
            {
                "name": "Butter Croissant",
                "description": "Flaky, buttery layers baked fresh every morning",
                "price": 3.5,
                "category": "Pastry",
                "image_url": "https://images.unsplash.com/photo-1541781774459-bb2af2f05b55",
                "is_available": True
            },
            {
                "name": "Sourdough Loaf",
                "description": "Slow-fermented with a crisp crust and tender crumb",
                "price": 6.0,
                "category": "Bread",
                "image_url": "https://images.unsplash.com/photo-1608198093002-ad4e005484ec",
                "is_available": True
            },
            {
                "name": "Chocolate Chip Cookie",
                "description": "Chewy center with dark chocolate chunks",
                "price": 2.0,
                "category": "Cookie",
                "image_url": "https://images.unsplash.com/photo-1541976076758-347942db1970",
                "is_available": True
            },
            {
                "name": "Red Velvet Cupcake",
                "description": "With cream cheese frosting",
                "price": 3.0,
                "category": "Cake",
                "image_url": "https://images.unsplash.com/photo-1599785209796-9e77cab9f1d5",
                "is_available": True
            }
        ]
        for s in samples:
            create_document("bakeryitem", s)
        return {"status": "ok", "count": len(samples)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Public endpoints
@app.get("/api/items")
def list_items():
    try:
        items = get_documents("bakeryitem")
        # Convert ObjectId to str
        for it in items:
            if "_id" in it:
                it["id"] = str(it.pop("_id"))
        return {"items": items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class CreateOrderRequest(BaseModel):
    customer_name: str
    customer_phone: str
    notes: str | None = None
    items: List[dict]

@app.post("/api/orders")
def create_order(payload: CreateOrderRequest):
    try:
        # Basic validation: ensure each item has id and quantity
        for it in payload.items:
            if "item_id" not in it or "quantity" not in it:
                raise HTTPException(status_code=400, detail="Each item requires item_id and quantity")
        order_id = create_document("order", payload.model_dump())
        return {"status": "ok", "order_id": order_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
