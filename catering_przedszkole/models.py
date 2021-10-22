from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.dispatch import receiver
import os

# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Musisz podac adres e-mail.")
        if not username:
            raise ValueError("Musisz podac adres nazwe uzytkownika.")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Uzytkownik(AbstractBaseUser):
    ID = models.AutoField(primary_key=True)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=30)
    address = models.CharField(max_length=80, default=" ")
    username = models.CharField(max_length=50, unique=True)
    balance = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    waiting_balance = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    objects = MyAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def _str_(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def status(self):
        if self.is_admin == False:
            return "Nie"
        else:
            return "Tak"


class Skladnik(models.Model):
    ID = models.AutoField(primary_key=True)
    nazwa_skladnika = models.CharField(max_length=50)
    wielkosc_porcji_skladnika = models.FloatField()
    energia_skladnika_kcal = models.FloatField()

    def __str__(self):
        data = self.nazwa_skladnika
        return data


class Typ_dania(models.Model):
    ID = models.AutoField(primary_key=True)
    nazwa_typu_dania = models.CharField(max_length=50)

    def __str__(self):
        data = self.nazwa_typu_dania
        return data


class Danie(models.Model):
    ID = models.AutoField(primary_key=True)
    typ_dania = models.ForeignKey(Typ_dania, on_delete=models.CASCADE)
    nazwa_dania = models.CharField(max_length=100)
    zdjecie = models.ImageField(upload_to="image", blank=True, max_length=300)
    komentarz = models.TextField(blank=True, null=True)

    def __str__(self):
        data = self.nazwa_dania
        return data


class Skladnik_dania(models.Model):
    ID = models.AutoField(primary_key=True)
    danie = models.ForeignKey(Danie, on_delete=models.CASCADE)
    skladnik = models.ForeignKey(Skladnik, on_delete=models.CASCADE)


class Zestaw(models.Model):
    ID = models.AutoField(primary_key=True)
    nazwa_zestawu = models.CharField(max_length=100)
    data_zestawu = models.DateField()
    czy_widoczny = models.BooleanField(default=False)
    cena_zestawu = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        data = self.nazwa_zestawu
        return data

    def status(self):
        if self.czy_widoczny == False:
            return "Niewidoczny"
        else:
            return "Widoczny"


class Zestaw_dan(models.Model):
    ID = models.AutoField(primary_key=True)
    zestaw = models.ForeignKey(Zestaw, on_delete=models.CASCADE)
    danie = models.ForeignKey(Danie, on_delete=models.CASCADE)


class Zamowienie(models.Model):
    ID = models.AutoField(primary_key=True)
    data_zamowienia = models.DateTimeField(default=timezone.now)
    czy_potwierdzone = models.BooleanField(default=False)
    komentarz_zamowienia = models.TextField(blank=True, null=True)
    zamawiajacy = models.ForeignKey(Uzytkownik, on_delete=models.CASCADE)
    ilosc_zestawow = models.DecimalField(max_digits=5, decimal_places=0, default=1)
    zestaw = models.ForeignKey(Zestaw, on_delete=models.CASCADE, default=1)
    czy_anulowano = models.BooleanField(default=False)
    powod_anulowania = models.TextField(blank=True, null=True)
    czy_oplacone = models.BooleanField(default=False)
    do_zaplaty = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def status(self):
        if self.czy_potwierdzone == False:
            return "Nie"
        else:
            return "Tak"

    def anulowano(self):
        if self.czy_anulowano == False:
            return "Nie"
        else:
            return "Tak"

    def oplacono(self):
        if self.czy_oplacone == False:
            return "Nie"
        else:
            return "Tak"


@receiver(models.signals.post_delete, sender=Danie)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.zdjecie:
        if os.path.isfile(instance.zdjecie.path):
            os.remove(instance.zdjecie.path)


@receiver(models.signals.pre_save, sender=Danie)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).zdjecie
    except sender.DoesNotExist:
        return False

    new_file = instance.zdjecie
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
