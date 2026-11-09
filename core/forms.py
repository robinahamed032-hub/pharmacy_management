from django import forms
from .models import Medicine, Supplier
class StyledModelForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields.values(): field.widget.attrs.setdefault('class','form-control')
class MedicineForm(StyledModelForm):
    class Meta:
        model = Medicine
        fields = '__all__'
        widgets = {'expiry_date': forms.DateInput(attrs={'type':'date','class':'form-control'})}
class SupplierForm(StyledModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'
