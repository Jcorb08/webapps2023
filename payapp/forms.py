from django import forms

from register.models import User


class PayForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(PayForm, self).__init__(*args, **kwargs)
        self.fields['form_user'].queryset = User.objects.exclude(id=user.id).exclude(is_staff=True)

    # All users apart from themselves, and not super admins
    # Functions as From for Request, and To for Sending Money
    form_user = forms.ModelChoiceField(
        queryset=None,
        help_text="Select the user",
        empty_label=None
    )
    # Min value is 1p as they have to request more than nothing
    form_amount = forms.DecimalField(decimal_places=2, max_digits=12, min_value=0.01)



