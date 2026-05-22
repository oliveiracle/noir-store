from django import forms
from .models import Product, Category, Review


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'category', 'sku', 'name', 'description',
            'price', 'rating', 'image', 'is_new',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [
            (c.id, c.get_friendly_name() or c.name)
            for c in categories
        ]
        self.fields['category'].choices = (
            [('', 'Select Category')] + friendly_names
        )
        for field in self.fields.values():
            field.widget.attrs['class'] = 'checkout-input'


class ReviewForm(forms.ModelForm):
    """Form for submitting or editing a product review."""
    class Meta:
        model = Review
        fields = ['rating', 'comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].widget.attrs['class'] = 'checkout-input'
        self.fields['comment'].widget.attrs.update({
            'class': 'checkout-input',
            'rows': 3,
            'placeholder': 'Share your thoughts...',
        })
        self.fields['comment'].label = False
        self.fields['rating'].label = False
