from catering_przedszkole.models import Uzytkownik, Skladnik, Skladnik_dania, Danie, Zestaw_dan, Typ_dania, Zestaw, Zamowienie

def get_all_visable_sets(request):
    sets=Zestaw.objects.all().filter(czy_widoczny=True).order_by('data_zestawu')
    return sets

def get_all_sets(request):
    sets=Zestaw.objects.all().order_by('data_zestawu')
    return sets

def get_data_of_sets(request):
    set_data = Zestaw_dan.objects.all()
    return set_data

def get_set_by_id(request, id_zestaw):
    singleset = Zestaw.objects.get(ID = id_zestaw)
    return singleset

def get_data_of_sets_by_id(request, id_zestaw):
    data = Zestaw_dan.objects.all().filter(zestaw = id_zestaw)
    return data

def get_data_of_ingredients(request):
    data = Skladnik_dania.objects.all()
    return data

def get_user_orders(request):
    user_id = request.user.ID
    data = Zamowienie.objects.all().filter(zamawiajacy=user_id).order_by('-data_zamowienia')
    return data

def get_order_by_id(request, id_zam):
    order = Zamowienie.objects.get(ID = id_zam)
    return order

def get_all_ingredients(request):
    ing=Skladnik.objects.all()
    return ing

def get_ingridient_by_id(request, id_skladnik):
    ingridient = Skladnik.objects.get(ID = id_skladnik)
    return ingridient

def get_all_dishes(request):
    dishes=Danie.objects.all().order_by('ID')
    return dishes

def get_dish_by_id(request, id_dania):
    dish = Danie.objects.get(ID = id_dania)
    return dish

def get_all_types(request):
    types=Typ_dania.objects.all().order_by('ID')
    return types

def get_type_by_id(request, id_typu_dania):
    type_ = Typ_dania.objects.get(ID = id_typu_dania)
    return type_

def change_set_visability(request, id_zestawu):
    id_zestawu = int(id_zestawu)
    zestaw=Zestaw.objects.get(pk=id_zestawu)
    if zestaw.czy_widoczny == True:
        zestaw.czy_widoczny = False
    else:
        zestaw.czy_widoczny = True
    zestaw.save()

def get_all_users(request):
    users=Uzytkownik.objects.all().order_by('ID')
    return users

def get_user_by_id(request, id_uzytkownika):
    user=Uzytkownik.objects.get(ID = id_uzytkownika)
    return user

def change_user_permissions(request, id_uzytkownika):
    id_uzytkownika = int(id_uzytkownika)
    u=Uzytkownik.objects.get(pk=id_uzytkownika)
    if u.is_admin == True:
        u.is_admin = False
    else:
        u.is_admin = True
    u.save()

def get_user_orders_by_id(request, id_uzytkownika):
    data = Zamowienie.objects.all().filter(zamawiajacy=id_uzytkownika).order_by('-data_zamowienia')
    return data

def change_order_status(request, id_zamowienia):
    id_zamowienia = int(id_zamowienia)
    order=Zamowienie.objects.get(pk=id_zamowienia)
    if order.czy_potwierdzone == True:
        order.czy_potwierdzone = False
    else:
        order.czy_potwierdzone = True
    order.save()

def get_all_orders(request):
    orders=Zamowienie.objects.all().order_by('-data_zamowienia')
    return orders

def get_ingridient_dish_by_id(request, id_skladniki_dania):
    data = Skladnik_dania.objects.get(ID = id_skladniki_dania)
    return data

def get_all_ingridients_dishes(request):
    data=Skladnik_dania.objects.all()
    return data

def get_all_sets_dishes(request):
    data=Zestaw_dan.objects.all()
    return data


def get_set_dish_by_id(request, id_dania_zestawy):
    data = Zestaw_dan.objects.get(ID = id_dania_zestawy)
    return data