# Party Gear Rental System API

A FastAPI-based backend system for managing party equipment rentals, including items like chairs, tables, party tents, and inflatables.

## Features

### Authentication & User Management
- User registration and login
- JWT-based authentication
- Role-based access control (Admin/Customer)

### Product Management
- Product catalog with categories
- Inventory tracking
- Product availability management
- Image handling for products

### Booking System
- Create and manage bookings
- Date-based availability checking
- Delivery address management
- Booking status tracking

### Invoice Generation
- Automatic invoice generation from bookings
- Price calculation based on rental duration
- Invoice status tracking

### Admin Features
- Sales reporting
- Popular items analytics
- Inventory availability reports
- User management

## Technical Stack

- **Framework**: FastAPI
- **Database**: MongoDB
- **Authentication**: JWT
- **Documentation**: Swagger/OpenAPI

## API Endpoints

### Authentication
- POST `/auth/register` - Register new user
- POST `/auth/login` - User login
- GET `/auth/me` - Get current user info

### Products
- GET `/products` - List all products
- POST `/products` - Create new product (Admin)
- GET `/products/{id}` - Get product details

### Bookings
- POST `/bookings` - Create new booking
- GET `/bookings` - List all bookings
- GET `/bookings/{id}` - Get booking details

### Invoices
- POST `/invoices/generate/{booking_id}` - Generate invoice
- GET `/invoices` - List all invoices
- GET `/invoices/{id}` - Get invoice details

### Admin
- GET `/admin/reports/sales` - Get sales report
- GET `/admin/reports/popular-items` - Get popular items
- GET `/admin/reports/availability` - Get availability report

### Local Setup

1. Install MongoDB
2. Run `python app/db_init.py` to initialize the database
3. Run `uvicorn app.main:app --reload` to start the server

### MongoDB Setup
# Update Homebrew
brew update

# Install MongoDB Community Edition
brew tap mongodb/brew
brew install mongodb-community

# Create the data directory if it doesn't exist
sudo mkdir -p /data/db
sudo chown -R $(whoami) /data/db

# Start MongoDB service
brew services start mongodb-community

For management is suggested to use MongoDB Compass

# Connect to MongoDB
mongosh

# You should see MongoDB shell prompt
# Exit with 'exit' command