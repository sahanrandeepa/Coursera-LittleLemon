"""
URL configuration for little_lemon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'menu-items', views.MenuItemViewSet, basename='menu-items')
router.register(r'orders', views.OrderViewSet, basename='orders')
router.register(r'categories', views.CategoryViewSet, basename='categories')

urlpatterns = [
    # Djoser endpoints
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    
    # Custom endpoints
    path('groups/manager/users/', views.ManagerUsersView.as_view()),
    path('groups/manager/users/<int:userId>/', views.ManagerUserDetailView.as_view()),
    path('groups/delivery-crew/users/', views.DeliveryCrewUsersView.as_view()),
    path('groups/delivery-crew/users/<int:userId>/', views.DeliveryCrewUserDetailView.as_view()),
    path('cart/menu-items/', views.CartView.as_view()),
    
    # Router endpoints
    path('', include(router.urls)),
]
