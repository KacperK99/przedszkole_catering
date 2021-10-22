from catering_przedszkole.models import (
    Uzytkownik,
    Zamowienie,
    Skladnik,
    Danie,
    Typ_dania,
    Zestaw,
    Skladnik_dania,
    Zestaw_dan,
)
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=60, help_text="Adres e-mail wymagany")
    phone_number = forms.CharField(max_length=30)
    address = forms.CharField(max_length=80)

    class Meta:
        model = Uzytkownik
        fields = [
            "email",
            "username",
            "phone_number",
            "address",
            "password1",
            "password2",
        ]

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        try:
            account = Uzytkownik.objects.get(email=email)
        except Uzytkownik.DoesNotExist:
            return email
        raise forms.ValidationError('Adres e-mail "%s"  jest już w użytku.' % account)

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            account = Uzytkownik.objects.get(username=username)
        except Uzytkownik.DoesNotExist:
            return username
        raise forms.ValidationError(
            'Nazwa użytkownika "%s" jest już w użytku.' % username
        )


class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput)

    class Meta:
        model = Uzytkownik
        fields = ("email", "password")

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data["email"]
            password = self.cleaned_data["password"]
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Błąd logowania")


class SkladnikCreate(forms.ModelForm):
    class Meta:
        model = Skladnik
        fields = "__all__"
        labels = {
            "wielkosc_porcji_skladnika": "Wielkość porcji składnika [g]",
            "energia_skladnika_kcal": "Energia składnika [kcal]",
        }


class DanieCreate(forms.ModelForm):
    class Meta:
        model = Danie
        fields = "__all__"


class TypDaniaCreate(forms.ModelForm):
    class Meta:
        model = Typ_dania
        fields = "__all__"


class ZestawCreate(forms.ModelForm):
    class Meta:
        model = Zestaw
        fields = "__all__"


class AnulowanoZamowienie(forms.ModelForm):
    class Meta:
        model = Zamowienie
        fields = ("czy_anulowano", "powod_anulowania")


class SkladnikiDaniaCreate(forms.ModelForm):
    class Meta:
        model = Skladnik_dania
        fields = "__all__"


class ZestawDanCreate(forms.ModelForm):
    class Meta:
        model = Zestaw_dan
        fields = "__all__"


class UzytkownikEdit(forms.ModelForm):
    class Meta:
        model = Uzytkownik
        fields = ("username", "email", "phone_number", "address")
        labels = {
            "username": "Nazwa użytkownika",
            "email": "Adres e-mail",
            "phone_number": "Numer telefonu",
            "address": "Pełny adres",
        }


class UzytkownikEditSaldo(forms.ModelForm):
    class Meta:
        model = Uzytkownik
        fields = ("balance",)
        labels = {
            "balance": "Saldo użytkownika",
        }


class AdminDodajZmienKomentarzAnulowania(forms.ModelForm):
    class Meta:
        model = Zamowienie
        fields = ("powod_anulowania",)
        labels = {
            "powod_anulowania": "Powód anulowania zamówienia",
        }


class ZamowienieEdit(forms.ModelForm):
    class Meta:
        model = Zamowienie
        fields = ("ilosc_zestawow", "komentarz_zamowienia")
        labels = {
            "ilosc_zestawow": "Ilość zamówionych zestawów",
            "komentarz_zamowienia": "Komentarz do zamówienia",
        }
