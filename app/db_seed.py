import asyncio
import random
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from app.core.config import settings
from app.utils.auth import get_password_hash

async def seed_database():
    print("Starting database seeding...")
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(settings.MONGO_URI)
    db = client[settings.MONGO_DB]
    
    # Drop existing collections to start fresh
    collections = await db.list_collection_names()
    for collection in collections:
        await db[collection].drop()
    
    print("Creating collections and indexes...")
    
    # Create collections
    await db.command({"create": "products"})
    await db.command({"create": "users"})
    await db.command({"create": "bookings"})
    await db.command({"create": "invoices"})
    
    # Create indexes
    await db.products.create_index("name")
    await db.users.create_index("email", unique=True)
    await db.bookings.create_index("product_id")
    await db.invoices.create_index("booking.id")
    
    print("Adding users...")
    
    # Create admin and test users
    users = [
        {
            "_id": str(ObjectId()),
            "email": "admin@example.com",
            "full_name": "Admin User",
            "password": get_password_hash("admin123"),
            "role": "admin",
            "phone": "555-1234"
        },
        {
            "_id": str(ObjectId()),
            "email": "customer@example.com",
            "full_name": "Test Customer",
            "password": get_password_hash("customer123"),
            "role": "customer",
            "phone": "555-5678"
        }
    ]
    
    await db.users.insert_many(users)
    
    print("Adding products...")
    
    # Create product data
    products = [
        {
            "_id": str(ObjectId()),
            "name": "Party Tent",
            "description": "Large party tent, 10x20 feet, waterproof",
            "type": "tent",
            "price_per_day": 100.0,
            "available_quantity": 5,
            "image_url": "https://example.com/tent.jpg"
        },
        {
            "_id": str(ObjectId()),
            "name": "Folding Chair",
            "description": "Comfortable folding chair with padded seat",
            "type": "furniture",
            "price_per_day": 5.0,
            "available_quantity": 50,
            "image_url": "https://example.com/chair.jpg"
        },
        {
            "_id": str(ObjectId()),
            "name": "Round Table",
            "description": "60-inch round table, seats 8 people",
            "type": "furniture",
            "price_per_day": 15.0,
            "available_quantity": 20,
            "image_url": "https://example.com/table.jpg"
        },
        {
            "_id": str(ObjectId()),
            "name": "Bouncy Castle",
            "description": "Kids' bouncy castle, 15x15 feet",
            "type": "inflatable",
            "price_per_day": 80.0,
            "available_quantity": 3,
            "image_url": "https://example.com/bouncy.jpg"
        },
        {
            "_id": str(ObjectId()),
            "name": "Sound System",
            "description": "Professional sound system with speakers and mixer",
            "type": "electronics",
            "price_per_day": 120.0,
            "available_quantity": 2,
            "image_url": "https://example.com/sound.jpg"
        },
    ]
    
    await db.products.insert_many(products)
    
    print("Creating bookings and invoices...")
    
    # Create sample bookings and invoices
    for i in range(10):
        # Select random product
        product = random.choice(products)
        
        # Generate random dates
        start_date = datetime.now() + timedelta(days=random.randint(-30, 30))
        end_date = start_date + timedelta(days=random.randint(1, 7))
        
        # Create booking
        booking_id = str(ObjectId())
        booking = {
            "_id": booking_id,
            "product_id": product["_id"],
            "start_date": start_date,
            "end_date": end_date,
            "status": random.choice(["pending", "confirmed", "completed", "cancelled"]),
            "delivery_address": f"{random.randint(100, 999)} Example St, City, State",
            "user_id": users[random.randint(0, 1)]["_id"],
            "quantity": random.randint(1, 3)
        }
        
        await db.bookings.insert_one(booking)
        
        # Only create invoices for non-cancelled bookings
        if booking["status"] != "cancelled":
            # Calculate days difference for the booking
            days_diff = (end_date - start_date).days
            if days_diff < 1:
                days_diff = 1
                
            # Create invoice item
            item = {
                "product": product,
                "quantity": booking["quantity"],
                "total_days": days_diff,
                "sub_total": product["price_per_day"] * days_diff * booking["quantity"]
            }
            
            # Create invoice
            invoice = {
                "_id": str(ObjectId()),
                "booking": booking,
                "total_amount": item["sub_total"],
                "created_at": datetime.now(),
                "status": random.choice(["pending", "paid"]),
                "items": [item]
            }
            
            await db.invoices.insert_one(invoice)
    
    print("Database seeding completed successfully!")

if __name__ == "__main__":
    # Check if settings are available
    if not hasattr(settings, "MONGO_URI") or not settings.MONGO_URI:
        print("Error: MONGO_URI not found in settings. Make sure your .env file is properly configured.")
        exit(1)
    
    asyncio.run(seed_database()) 