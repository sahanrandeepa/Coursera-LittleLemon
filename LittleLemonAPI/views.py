from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User, Group
from .models import MenuItem, Cart, Order, OrderItem
from .serializers import MenuItemSerializer, CartSerializer, OrderSerializer
from .permissions import IsManager, IsDeliveryCrew, IsCustomer

# Menu Items
class MenuItemViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'price']
    search_fields = ['name']
    ordering_fields = ['price', 'name']
    pagination_class = PageNumberPagination
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated(), IsManager()]
        return [IsAuthenticated()]

# User Group Management
class ManagerUsersView(APIView):
    permission_classes = [IsAuthenticated, IsManager]
    
    def get(self, request):
        managers = User.objects.filter(groups__name='Manager')
        return Response({'managers': [user.username for user in managers]}, status=status.HTTP_200_OK)
    
    def post(self, request):
        user = User.objects.get(id=request.data['user_id'])
        group = Group.objects.get(name='Manager')
        group.user_set.add(user)
        return Response(status=status.HTTP_201_CREATED)

class ManagerUserDetailView(APIView):
    permission_classes = [IsAuthenticated, IsManager]
    
    def delete(self, request, userId):
        try:
            user = User.objects.get(id=userId)
            group = Group.objects.get(name='Manager')
            group.user_set.remove(user)
            return Response(status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

# Similar logic for DeliveryCrewUsersView and DeliveryCrewUserDetailView

# Cart Management
class CartView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]
    
    def get(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CartSerializer(data={**request.data, 'user': request.user.id})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        Cart.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_200_OK)

# Orders
class OrderViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'price']
    search_fields = ['name']
    ordering_fields = ['price', 'name']
    pagination_class = PageNumberPagination
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        if self.request.user.groups.filter(name='Manager').exists():
            return Order.objects.all()
        elif self.request.user.groups.filter(name='Delivery crew').exists():
            return Order.objects.filter(delivery_crew=self.request.user)
        return Order.objects.filter(user=self.request.user)
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsCustomer()]
        elif self.request.method in ['PUT', 'PATCH']:
            return [IsAuthenticated(), IsManager() | IsDeliveryCrew()]
        elif self.request.method == 'DELETE':
            return [IsAuthenticated(), IsManager()]
        return [IsAuthenticated()]
    
    def create(self, request, *args, **kwargs):
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items:
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)
        
        order = Order.objects.create(user=request.user, total=0)
        total = 0
        for item in cart_items:
            OrderItem.objects.create(order=order, menu_item=item.menu_item, quantity=item.quantity)
            total += item.menu_item.price * item.quantity
        order.total = total
        order.save()
        cart_items.delete()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
