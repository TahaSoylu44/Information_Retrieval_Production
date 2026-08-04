from django import forms

class CustomQueryForm(forms.Form):
    q = forms.CharField(
        label="",
        max_length=500,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your query...',
            'class': 'form-control',
            'style': 'width: 60%; padding: 10px; font-size: 16px;'
        })
    )