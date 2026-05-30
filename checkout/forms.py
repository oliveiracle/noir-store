from django import forms
from .models import Order


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        # Only include the fields the customer needs to fill in
        fields = (
            'full_name', 'email', 'phone_number',
            'street_address1', 'street_address2',
            'town_or_city', 'postcode', 'country', 'county',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Placeholder text to show inside each input field
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'town_or_city': 'Town or City',
            'postcode': 'Postcode',
            'country': 'Country',
            'county': 'County / State',
        }

        for field in self.fields:
            placeholder = placeholders[field]
            # Add an asterisk to required fields so users know they're needed
            if self.fields[field].required:
                placeholder += ' *'
            self.fields[field].widget.attrs['placeholder'] = placeholder
            # Apply the same CSS class to all fields for consistent styling
            self.fields[field].widget.attrs['class'] = 'checkout-input'
            # Hide the labels since we're using placeholders instead
            self.fields[field].label = False
