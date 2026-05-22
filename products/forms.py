from django import forms
from .models import Product, Category, Review


class ProductForm(forms.ModelForm):
    """Form for adding or editing a product — used by admin only."""

    class Meta:
        model = Product
        fields = [
            'category', 'sku', 'name', 'description',
            'price', 'rating', 'image', 'is_new',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Replace category IDs with friendly names in the dropdown
        categories = Category.objects.all()
        friendly_names = [
            (c.id, c.get_friendly_name() or c.name)
            for c in categories
        ]
        self.fields['category'].choices = (
            [('', 'Select Category')] + friendly_names
        )

        # Apply the same input style to all fields
        for field in self.fields.values():
            field.widget.attrs['class'] = 'checkout-input'


class ReviewForm(forms.ModelForm):
    """Form for submitting or editing a product review."""

    class Meta:
        model = Review
        # The product and user are set in the view, not by the user
        fields = ['rating', 'comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Style the rating dropdown to match the rest of the site
        self.fields['rating'].widget.attrs['class'] = 'checkout-input'

        # Style the comment textarea and add a placeholder
        self.fields['comment'].widget.attrs.update({
            'class': 'checkout-input',
            'rows': 3,
            'placeholder': 'Share your thoughts...',
        })

        # Hide labels — placeholders handle the hints instead
        self.fields['comment'].label = False
        self.fields['rating'].label = False
