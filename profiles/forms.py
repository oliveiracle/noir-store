from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        # Exclude the user field — it's set automatically, not by the user
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Placeholder text shown inside each input field
        placeholders = {
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
            self.fields[field].widget.attrs['placeholder'] = placeholder
            # Apply consistent input styling from the CSS
            self.fields[field].widget.attrs['class'] = 'checkout-input'
            # Hide labels — the placeholders serve as labels
            self.fields[field].label = False
