from django import forms
from .models import Product, Category


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'sku', 'name', 'description', 'price', 'rating', 'image', 'is_new']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name() or c.name) for c in categories]
        self.fields['category'].choices = [('', 'Select Category')] + friendly_names
        for field in self.fields.values():
            field.widget.attrs['class'] = 'checkout-input'
