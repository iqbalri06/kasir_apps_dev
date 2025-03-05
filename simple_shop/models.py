import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.ForeignKey('Role', on_delete=models.PROTECT, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.username

class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class CustomerType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    points_multiplier = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Stored as percentage (e.g., 5.00 for 5%)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Member(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True)
    points = models.IntegerField(default=0)
    points_used = models.IntegerField(default=0)
    total_purchases = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    customer_type = models.ForeignKey(CustomerType, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def add_points(self, purchase_amount):
        # Add 1 point for every 10000 spent
        new_points = int(purchase_amount / 10000)
        self.points += new_points
        self.total_purchases += purchase_amount
        self.save()
        return new_points

    def use_points(self, points_to_use):
        if points_to_use <= self.points:
            self.points -= points_to_use
            self.points_used += points_to_use
            self.save()
            # Convert points to rupiah (1 point = Rp 1000 discount)
            return points_to_use * 1000
        return 0

    def __str__(self):
        return self.name

class Payment(models.Model):
    PAYMENT_CHOICES = [
        ('cash', 'Tunai'),
        ('qris', 'QRIS'),
        ('debit', 'Debit')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    method = models.CharField(max_length=50, choices=PAYMENT_CHOICES)

    def __str__(self):
        return dict(self.PAYMENT_CHOICES).get(self.method, self.method)

class Sale(models.Model):
    STATUS_CHOICES = [
        ('completed', 'Selesai'),
        ('pending', 'Pending'),
        ('cancelled', 'Dibatalkan')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='sales')
    member = models.ForeignKey(Member, on_delete=models.PROTECT, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=0)
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)  # Add db_index
    points_earned = models.IntegerField(default=0)
    points_used = models.IntegerField(default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    payment_details = models.JSONField(default=dict)  # Add this field
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='completed',
        db_index=True
    )
    transaction_number = models.CharField(max_length=20, unique=True, editable=False)  # Add new field for formatted transaction number
    
    @property
    def status_color(self):
        return {
            'pending': 'warning',
            'completed': 'success',
            'cancelled': 'danger',
        }.get(self.status, 'secondary')

    @property
    def cashier(self):
        return self.user  # Use the user field as cashier

    def save(self, *args, **kwargs):
        # Always ensure created_at is timezone aware
        if not self.created_at:
            self.created_at = timezone.localtime(timezone.now())
            
        # Generate transaction number
        if not self.transaction_number:
            date_string = self.created_at.strftime('%y%m%d')
            last_transaction = Sale.objects.filter(
                transaction_number__startswith=f"INV/{date_string}"
            ).order_by('-transaction_number').first()
            
            if last_transaction:
                last_sequence = int(last_transaction.transaction_number.split('/')[-1])
                sequence = str(last_sequence + 1).zfill(4)
            else:
                sequence = '0001'
            
            self.transaction_number = f"INV/{date_string}/{sequence}"
        
        if not self.payment_details:
            self.payment_details = {}
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Sale {self.id} by {self.user.username}"

class SaleDetail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='details')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.price
        super().save(*args, **kwargs)

class PointsUsage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    member = models.ForeignKey(Member, on_delete=models.PROTECT)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    points_used = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class StockMovement(models.Model):
    MOVEMENT_TYPES = [
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    type = models.CharField(max_length=10, choices=MOVEMENT_TYPES)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.type == 'IN':
            self.product.stock += self.quantity
        else:
            self.product.stock -= self.quantity
        self.product.save()
        super().save(*args, **kwargs)

class Receipt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sale = models.OneToOneField(Sale, on_delete=models.PROTECT)
    printed_at = models.DateTimeField(auto_now_add=True)
    printed_by = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f"Receipt for sale {self.sale.id}"

    class Meta:
        ordering = ['-printed_at']

class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"
