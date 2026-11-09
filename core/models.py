from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
class Supplier(models.Model):
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name
class Medicine(models.Model):
    CATEGORY_CHOICES=[('Tablet','Tablet'),('Capsule','Capsule'),('Syrup','Syrup'),('Injection','Injection'),('Cream','Cream'),('Other','Other')]
    name = models.CharField(max_length=150)
    generic_name = models.CharField(max_length=150, blank=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='Tablet')
    batch_no = models.CharField(max_length=50)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    stock = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=10)
    expiry_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f'{self.name} ({self.batch_no})'
    @property
    def is_low_stock(self): return self.stock <= self.reorder_level
    @property
    def is_expired(self): return self.expiry_date < timezone.localdate()
class Sale(models.Model):
    invoice_no = models.CharField(max_length=30, unique=True)
    customer_name = models.CharField(max_length=120, default='Walk-in Customer')
    customer_phone = models.CharField(max_length=30, blank=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    sold_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    sold_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.invoice_no
class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, related_name='items', on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    @property
    def line_total(self): return self.quantity * self.unit_price
