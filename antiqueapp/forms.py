from django import forms




from .models import Address

class AddressForm(forms.ModelForm):

    STATE_CHOICES = [
            ('Andhra Pradesh', 'Andhra Pradesh'),
            ('Arunachal Pradesh', 'Arunachal Pradesh'),
            ('Assam', 'Assam'),
            ('Bihar', 'Bihar'),
            # and so on...
        ]

    DISTRICT_CHOICES = [
            ('District 1', 'District 1'),
            ('District 2', 'District 2'),
            ('District 3', 'District 3'),
            # and so on...
        ]


    fname = forms.CharField(max_length=250)
    lname = forms.CharField(max_length=250)
    street = forms.CharField(max_length=250, required=True)
    city = forms.CharField(max_length=250, required=True)
    state = forms.ChoiceField(choices=STATE_CHOICES)
    district = forms.ChoiceField(choices=DISTRICT_CHOICES)
    zip = forms.IntegerField(required=True)
    phone = forms.IntegerField(required=True)
    


   