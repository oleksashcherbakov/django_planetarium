from django import forms
from core_app.models import ShowTheme


class ShowThemeForm(forms.ModelForm):
    class Meta:
        model = ShowTheme
        fields = "__all__"
