from django.contrib import admin
from .models import (
    User, Role, Category, Product, CustomerType,
    Member, Payment, Sale, SaleDetail, PointsUsage,
    StockMovement, Receipt, CartItem
)

admin.site.register(User)
admin.site.register(Role)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(CustomerType)
admin.site.register(Member)
admin.site.register(Payment)
admin.site.register(Sale)
admin.site.register(SaleDetail)
admin.site.register(PointsUsage)
admin.site.register(StockMovement)
admin.site.register(Receipt)
admin.site.register(CartItem)
