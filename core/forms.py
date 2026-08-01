from django import forms
from .models import ContactMessage, PaymentProof


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "phone", "email", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Your name"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Your phone number"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "you@example.com"}),
            "message": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "How can we help?"}),
        }


class PaymentProofForm(forms.ModelForm):
    class Meta:
        model = PaymentProof
        fields = ["name", "phone", "note", "screenshot"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Your name"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Your phone number"}),
            "note": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Munnar Family Trip - 15 Aug"}),
            "screenshot": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
