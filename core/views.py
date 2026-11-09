from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import MedicineForm, SupplierForm
from .models import Medicine, Sale, SaleItem, Supplier
@login_required
def dashboard(request):
    medicines = Medicine.objects.all()
    context={'medicine_count': medicines.count(),'supplier_count':Supplier.objects.count(),'sale_count':Sale.objects.count(),'revenue':Sale.objects.aggregate(v=Sum('total_amount'))['v'] or 0,'low_stock': medicines.filter(stock__lte=10).order_by('stock')[:6],'recent_sales':Sale.objects.order_by('-sold_at')[:6]}
    return render(request,'core/dashboard.html',context)
@login_required
def medicines(request):
    q=request.GET.get('q','').strip(); qs=Medicine.objects.select_related('supplier').order_by('name')
    if q: qs=qs.filter(Q(name__icontains=q)|Q(generic_name__icontains=q)|Q(batch_no__icontains=q))
    return render(request,'core/medicines.html',{'medicines':qs,'q':q})
@login_required
def medicine_add(request):
    form=MedicineForm(request.POST or None)
    if form.is_valid(): form.save(); messages.success(request,'Medicine added successfully.'); return redirect('medicines')
    return render(request,'core/medicine_form.html',{'form':form,'title':'Add Medicine'})
@login_required
def medicine_edit(request,pk):
    obj=get_object_or_404(Medicine,pk=pk); form=MedicineForm(request.POST or None,instance=obj)
    if form.is_valid(): form.save(); messages.success(request,'Medicine updated.'); return redirect('medicines')
    return render(request,'core/medicine_form.html',{'form':form,'title':'Edit Medicine'})
@login_required
def medicine_delete(request,pk):
    if request.method=='POST': get_object_or_404(Medicine,pk=pk).delete(); messages.success(request,'Medicine deleted.')
    return redirect('medicines')
@login_required
def suppliers(request): return render(request,'core/suppliers.html',{'suppliers':Supplier.objects.order_by('name')})
@login_required
def supplier_add(request):
    form=SupplierForm(request.POST or None)
    if form.is_valid(): form.save(); messages.success(request,'Supplier added.'); return redirect('suppliers')
    return render(request,'core/medicine_form.html',{'form':form,'title':'Add Supplier'})
@login_required
def sales(request): return render(request,'core/sales.html',{'sales':Sale.objects.order_by('-sold_at')})
@login_required
def sale_add(request):
    if request.method=='POST':
        med=get_object_or_404(Medicine,pk=request.POST.get('medicine')); qty=int(request.POST.get('quantity','0'))
        if qty<1 or qty>med.stock: messages.error(request,'Quantity is invalid or exceeds available stock.'); return redirect('sale_add')
        invoice=f'INV-{timezone.now().strftime("%Y%m%d%H%M%S")}'
        sale=Sale.objects.create(invoice_no=invoice,customer_name=request.POST.get('customer_name') or 'Walk-in Customer',customer_phone=request.POST.get('customer_phone',''),sold_by=request.user,total_amount=Decimal(qty)*med.selling_price)
        SaleItem.objects.create(sale=sale,medicine=med,quantity=qty,unit_price=med.selling_price); med.stock-=qty; med.save(update_fields=['stock']); messages.success(request,'Sale recorded successfully.'); return redirect('sale_detail',pk=sale.pk)
    return render(request,'core/sale_form.html',{'medicines':Medicine.objects.filter(stock__gt=0).order_by('name')})
@login_required
def sale_detail(request,pk): return render(request,'core/sale_detail.html',{'sale':get_object_or_404(Sale.objects.prefetch_related('items__medicine'),pk=pk)})
