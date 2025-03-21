# Little Lemon API  

## ⭐ Overview  
This project is a fully functional **REST API** for the **Little Lemon** restaurant, enabling client applications to manage **menu items, orders, and user roles**. The API supports **customers, managers, and delivery crew** with authentication and authorization.  

## 🚀 Features  
- ✅ **User registration & authentication** (Djoser)  
- ✅ **Role-based access control** (Manager, Delivery Crew, Customer)  
- ✅ **Menu management**  
- ✅ **Order placement & tracking**  
- ✅ **Cart system**  
- ✅ **Filtering, pagination, and sorting**  
- ✅ **API throttling**  

## 🛠 Tech Stack  
- **Backend:** Django, Django REST Framework (DRF)  
- **Auth:** Djoser, Token Authentication  
- **Database:** PostgreSQL  

## 📌 API Endpoints  

### 🔹 User Management  
- `POST /api/users/` → **Register a user**  
- `POST /token/login/` → **Generate auth token**  
- `GET /api/users/me/` → **View current user**  

### 🔹 Menu Management  
- `GET /api/menu-items/` → **View all menu items**  
- `POST /api/menu-items/` *(Manager only)* → **Add a new menu item**  
- `PUT /api/menu-items/{id}/` *(Manager only)* → **Update menu item**  
- `DELETE /api/menu-items/{id}/` *(Manager only)* → **Delete menu item**  

### 🔹 Order Management  
- `POST /api/orders/` → **Place an order**  
- `GET /api/orders/` → **View user orders**  
- `GET /api/orders/` *(Manager only)* → **View all orders**  
- `PATCH /api/orders/{id}/` *(Manager/Delivery Crew only)* → **Update order status**  

## ⚙ Installation  
1. **Clone the repository**  
   
   git clone https://github.com/your-username/little-lemon-api.git  
   cd little-lemon-api  

2. **Create a virtual environment**
   pipenv install  
   pipenv shell

3. **Apply migrations**
   python manage.py migrate  

4. **Run the server**
   python manage.py runserver  


