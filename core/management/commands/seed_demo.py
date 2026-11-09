from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from datetime import date, timedelta
from core.models import Supplier, Medicine
class Command(BaseCommand):
    help='Create demo login and sample pharmacy data'
    def handle(self,*args,**kwargs):
        user,_=User.objects.get_or_create(username='admin',defaults={'email':'admin@example.com','first_name':'Pharmacy Admin','is_staff':True,'is_superuser':True})
        user.set_password('admin123'); user.save()
        s1,_=Supplier.objects.get_or_create(name='HealthCare Distributors',defaults={'phone':'01700000000','email':'sales@healthcare.test','address':'Dhaka, Bangladesh'})
        s2,_=Supplier.objects.get_or_create(name='MediSupply Ltd.',defaults={'phone':'01800000000','address':'Chattogram, Bangladesh'})
        data=[('Napa 500mg','Paracetamol','Tablet','NAPA-24',s1,2.5,3.0,120,10),('Seclo 20mg','Omeprazole','Capsule','SEC-24',s2,4,5.5,8,10),('Syrup X','Cough Relief','Syrup','SYR-25',s1,80,110,35,8),('Azithro 500mg','Azithromycin','Tablet','AZI-25',s2,18,25,55,10)]
        for name,generic,cat,batch,sup,buy,sell,stock,reorder in data:
            Medicine.objects.get_or_create(batch_no=batch,defaults={'name':name,'generic_name':generic,'category':cat,'supplier':sup,'purchase_price':buy,'selling_price':sell,'stock':stock,'reorder_level':reorder,'expiry_date':date.today()+timedelta(days=365)})
        self.stdout.write(self.style.SUCCESS('Demo data ready. Login: admin / admin123'))
