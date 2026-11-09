from django.contrib import admin
from .models import Supplier, Medicine, Sale, SaleItem
admin.site.register([Supplier, Medicine, Sale, SaleItem])
