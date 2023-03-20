from django import forms


class PayForm(forms.Form):
    # All users apart from themselves, and not super admins
    # Functions as From for Request, and To for Sending Money
    user = forms.ModelChoiceField()
    # Min value is 1p as they have to request more than nothing
    amount = forms.DecimalField(decimal_places=2, max_digits=12, default=0, min_value=0.01)

