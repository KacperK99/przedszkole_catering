from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from .forms import (
    RegisterForm,
    AccountAuthenticationForm,
    SkladnikCreate,
    DanieCreate,
    TypDaniaCreate,
    ZestawCreate,
    AnulowanoZamowienie,
    SkladnikiDaniaCreate,
    ZestawDanCreate,
    UzytkownikEdit,
    UzytkownikEditSaldo,
    AdminDodajZmienKomentarzAnulowania,
)
from catering_przedszkole.models import (
    Uzytkownik,
    Zestaw,
    Zamowienie,
    Skladnik,
    Danie,
    Typ_dania,
    Zestaw_dan,
    Skladnik_dania,
)
from catering_przedszkole.controller.controller import (
    get_all_visable_sets,
    get_data_of_sets,
    get_set_by_id,
    get_data_of_sets_by_id,
    get_data_of_ingredients,
    get_user_orders,
    get_order_by_id,
    get_all_ingredients,
    get_ingridient_by_id,
    get_dish_by_id,
    get_all_dishes,
    get_all_types,
    get_type_by_id,
    get_all_sets,
    change_set_visability,
    get_all_users,
    change_user_permissions,
    get_user_by_id,
    get_user_orders_by_id,
    change_order_confirm_status,
    change_order_cancel_status,
    change_order_payment_status,
    get_all_orders,
    get_ingridient_dish_by_id,
    get_all_ingridients_dishes,
    get_all_sets_dishes,
    get_set_dish_by_id,
)
from django.http import HttpResponse
import json
from datetime import date
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def registration_view(request, *args, **kwargs):
    context = {}
    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get("email").lower()
            raw_password = form.cleaned_data.get("password1")
            username = form.cleaned_data.get("username")
            phone_number = form.cleaned_data.get("phone_number")
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            destination = kwargs.get("next")
            if destination:
                return redirect(destination)
            return redirect("mainpage")
        else:
            context["registration_form"] = form
    else:
        form = RegisterForm()
        context["registration_form"] = form
    return render(request, "signup.html", context)


def adminpage_view(request):
    if request.user.is_anonymous == True:
        return redirect("mainpage")
    elif request.user.is_admin == False:
        return redirect("mainpage")
    return render(request, "adminpage.html")


def login_view(request, *args, **kwargs):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect("mainpage")
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST["email"]
            password = request.POST["password"]
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect("mainpage")
    else:
        form = AccountAuthenticationForm()
    context["login_form"] = form
    return render(request, "login.html", context)


def logout_view(request):
    logout(request)
    return redirect("login")


def mainpage_view(request, *args, **kwargs):
    sets = get_all_visable_sets(request)
    data_set = get_data_of_sets(request)
    today = date.today()
    return render(
        request, "mainpage.html", {"sets": sets, "data_set": data_set, "today": today}
    )


def zestaw_view(request, id_zestaw):
    try:
        singleset = get_set_by_id(request, id_zestaw)
    except Zestaw.DoesNotExist:
        return redirect("mainpage")
    if singleset.czy_widoczny == False:
        return redirect("mainpage")
    data = get_data_of_sets_by_id(request, id_zestaw)
    ingridients = get_data_of_ingredients(request)
    return render(
        request,
        "zestaw.html",
        {"singleset": singleset, "data": data, "ing": ingridients},
    )


def mojekonto_view(request):
    return render(request, "konto.html")


def mojekonto_update(request, id_uzytkownika):
    if request.user.is_anonymous == True:
        return redirect("login")
    id_uzytkownika = int(id_uzytkownika)
    if request.user.ID != id_uzytkownika:
        return redirect("mainpage")
    try:
        user = get_user_by_id(request, id_uzytkownika)
    except Uzytkownik.DoesNotExist:
        return redirect("konto")
    form = UzytkownikEdit(request.POST or None, request.FILES or None, instance=user)
    if form.is_valid():
        form.save()
        return redirect("konto")
    return render(request, "edytujkonto.html", {"edit_account": form})


def zamow_view(request, id_zestaw, *args, **kwargs):
    if request.user.is_anonymous == True:
        return redirect("login")
    try:
        zestaw_instance = get_set_by_id(request, id_zestaw)
    except Zestaw.DoesNotExist:
        return redirect("mainpage")
    if (request.method == "GET") and request.GET.get("numberInput"):
        com = request.GET.get("commentInput")
        num = request.GET.get("numberInput")
        pay = float(zestaw_instance.cena_zestawu) * float(num)
        zam = Zamowienie.objects.create(
            komentarz_zamowienia=com,
            zamawiajacy=request.user,
            ilosc_zestawow=num,
            zestaw=zestaw_instance,
            do_zaplaty=pay,
        )
        actual_waiting_balance = float(zam.zamawiajacy.waiting_balance)
        new_waiting_balance = float(actual_waiting_balance) + float(pay)
        user_email = zam.zamawiajacy.email
        user_to_update = Uzytkownik.objects.filter(email=user_email).update(
            waiting_balance=new_waiting_balance
        )
    return render(
        request, "zamow.html", {"zestaw_id": id_zestaw, "zestaw": zestaw_instance}
    )


def zamowienia_view(request):
    if request.user.is_anonymous == True:
        return redirect("login")
    orders = get_user_orders(request)

    page = request.GET.get("page", 1)
    paginator = Paginator(orders, 15)
    try:
        order = paginator.page(page)
    except PageNotAnInteger:
        order = paginator.page(1)
    except EmptyPage:
        order = paginator.page(paginator.num_pages)

    return render(request, "zamowienia.html", {"orders": order})


def zamowienie_anuluj(request, id_zam):
    if request.user.is_anonymous == True:
        return redirect("login")
    id_zam = int(id_zam)
    try:
        order = get_order_by_id(request, id_zam)
    except Zamowienie.DoesNotExist:
        return redirect("zamowienia")
    order.czy_anulowano = True
    order.powod_anulowania = "Anulowano przez użytkownika"
    order.save()
    actual_waiting_balance = float(order.zamawiajacy.waiting_balance)
    new_waiting_balance = float(actual_waiting_balance) - float(order.do_zaplaty)
    user_email = request.user.email
    user_to_update = Uzytkownik.objects.filter(email=user_email).update(
        waiting_balance=new_waiting_balance
    )
    return redirect("zamowienia")


def admin_skladniki_view(request):
    if request.user.is_anonymous == True:
        return redirect("login")
    elif request.user.is_admin == False:
        return redirect("mainpage")
    ingredients = get_all_ingredients(request)
    return render(request, "admin_skladniki.html", {"ingredients": ingredients})


def admin_skladnik_create(request):
    if request.user.is_anonymous == True:
        return redirect("login")
    elif request.user.is_admin == False:
        return redirect("mainpage")
    form = SkladnikCreate(request.POST or None, request.FILES)
    if form.is_valid():
        form.save()
        return redirect("admin_skladniki")
    return render(request, "admin_skladnik_add.html", {"add_ingridient": form})


def admin_skladnik_delete(request, id_skladnik):
    if request.user.is_anonymous == True:
        return redirect("login")
    elif request.user.is_admin == False:
        return redirect("mainpage")
    id_skladnik = int(id_skladnik)
    try:
        ingridient = get_ingridient_by_id(request, id_skladnik)
    except Skladnik.DoesNotExist:
        return redirect("admin_skladniki")
    ingridient.delete()
    return redirect("admin_skladniki")


def admin_skladnik_update(request, id_skladnik):
    if request.user.is_anonymous == True:
        return redirect("login")
    elif request.user.is_admin == False:
        return redirect("mainpage")
    id_skladnik = int(id_skladnik)
    try:
        ingridient = get_ingridient_by_id(request, id_skladnik)
    except Skladnik.DoesNotExist:
        return redirect("admin_skladniki")
    form = SkladnikCreate(
        request.POST or None, request.FILES or None, instance=ingridient
    )
    if form.is_valid():
        form.save()
        return redirect("admin_skladniki")
    return render(request, "admin_skladnik_add.html", {"add_ingridient": form})


def admin_dania_view(request):
    if request.user.is_anonymous == True:
        return redirect("login")
    elif request.user.is_admin == False:
        return redirect("mainpage")
    dishes = get_all_dishes(request)

    type_query = request.GET.get("typ")
    name_query = request.GET.get("nazwa")

    if type_query != "" and type_query is not None:
        dishes = dishes.filter(
            typ_dania__nazwa_typu_dania__icontains=type_query.strip()
        )
    if name_query != "" and name_query is not None:
        dishes = dishes.filter(nazwa_dania__icontains=name_query.strip())

    return render(request, "admin_dania.html", {"dishes": dishes})


def admin_danie_create(request):
    if request.user.is_anonymous == True:
        return redirect("login")
    elif request.user.is_admin == False:
        return redirect("mainpage")
    form = DanieCreate(request.POST or None, request.FILES)
    if form.is_valid():
        form.save()
        return redirect("admin_dania")
    return render(request, "admin_danie_add.html", {"add_dish": form})


def admin_danie_delete(request, id_dania):
    if request.user.is_anonymous == True:
        return redirect("login")
    elif request.user.is_admin == False:
        return redirect("mainpage")
    id_dania = int(id_dania)
    try:
        dish = get_dish_by_id(request, id_dania)
    except Danie.DoesNotExist:
        return redirect("admin_dania")
    dish.delete()
    return redirect("admin_dania")


def admin_danie_update(request, id_dania):
    if request.user.is_anonymous == True:
        return redirect("login")
    elif request.user.is_admin == False:
        return redirect("mainpage")
    id_dania = int(id_dania)
    try:
        dish = get_dish_by_id(request, id_dania)
    except Danie.DoesNotExist:
        return redirect("admin_dania")
    form = DanieCreate(request.POST or None, request.FILES or None, instance=dish)
    if form.is_valid():
        form.save()
        return redirect("admin_dania")
    return render(request, "admin_danie_add.html", {"add_dish": form})


def admin_typy_dan_view(request):
    if request.user.is_anonymous == True:
        return redirect("login")
    elif request.user.is_admin == False:
        return redirect("mainpage")
    types = get_all_types(request)
    return render(request, "admin_typy_dan.html", {"types": types})


def admin_typ_dania_create(request):
    if request.user.is_anonymous == True:
        return redirect("login")
    elif request.user.is_admin == False:
        return redirect("mainpage")
    form = TypDaniaCreate(request.POST or None, request.FILES)
    if form.is_valid():
        form.save()
        return redirect("admin_typy_dan")
    return render(request, "admin_typ_dania_add.html", {"add_type": form})


def admin_typ_dania_delete(request, id_typu_dania):
    if request.user.is_anonymous == True:
        return redirect("login")
    elif request.user.is_admin == False:
        return redirect("mainpage")
    id_typu_dania = int(id_typu_dania)
    try:
        type_ = get_type_by_id(request, id_typu_dania)
    except Typ_dania.DoesNotExist:
        return redirect("admin_typy_dan")
    type_.delete()
    return redirect("admin_typy_dan")


def admin_typ_dania_update(request, id_typu_dania):
    if request.user.is_anonymous == True:
        return redirect("login")
    elif request.user.is_admin == False:
        return redirect("mainpage")
    id_typu_dania = int(id_typu_dania)
    try:
        type_ = get_type_by_id(request, id_typu_dania)
    except Typ_dania.DoesNotExist:
        return redirect("admin_typy_dan")
    form = TypDaniaCreate(request.POST or None, request.FILES or None, instance=type_)
    if form.is_valid():
        form.save()
        return redirect("admin_typy_dan")
    return render(request, "admin_typ_dania_add.html", {"add_type": form})


def admin_zestawy_view(request):
    if request.user.is_anonymous == True:
        return redirect("login")
    elif request.user.is_admin == False:
        return redirect("mainpage")
    sets = get_all_sets(request)
    return render(request, "admin_zestawy.html", {"sets": sets})


def admin_zestaw_create(request):
    if request.user.is_anonymous == True:
        return redirect("login")
    elif request.user.is_admin == False:
        return redirect("mainpage")
    form = ZestawCreate(request.POST or None, request.FILES)
    if form.is_valid():
        form.save()
        return redirect("admin_zestawy")
    return render(request, "admin_zestaw_add.html", {"add_set": form})


def admin_zestaw_delete(request, id_zestawu):
    if request.user.is_anonymous == True:
        return redirect("login")
    elif request.user.is_admin == False:
        return redirect("mainpage")
    id_zestawu = int(id_zestawu)
    try:
        set_ = get_set_by_id(request, id_zestawu)
    except Zestaw.DoesNotExist:
        return redirect("admin_zestawy")
    set_.delete()
    return redirect("admin_zestawy")


def admin_zestaw_update(request, id_zestawu):
    if request.user.is_anonymous == True:
        return redirect("login")
    elif request.user.is_admin == False:
        return redirect("mainpage")
    id_zestawu = int(id_zestawu)
    try:
        set_ = get_set_by_id(request, id_zestawu)
    except Zestaw.DoesNotExist:
        return redirect("admin_zestawy")
    form = ZestawCreate(request.POST or None, request.FILES or None, instance=set_)
    if form.is_valid():
        form.save()
        return redirect("admin_zestawy")
    return render(request, "admin_zestaw_add.html", {"add_set": form})


def admin_zmien_widocznosc(request, id_zestawu):
    if request.user.is_anonymous == True:
        return redirect("login")
    elif request.user.is_admin == False:
        return redirect("mainpage")
    change_set_visability(request, id_zestawu)
    return redirect("admin_zestawy")


def admin_uzytkownicy_view(request):
    if request.user.is_anonymous == True:
        return redirect("login")
    elif request.user.is_admin == False:
        return redirect("mainpage")
    users = get_all_users(request)
    return render(request, "admin_uzytkownicy.html", {"users": users})


def admin_uzytkownik_delete(request, id_uzytkownika):
    if request.user.is_anonymous == True:
        return redirect("login")
    elif request.user.is_admin == False:
        return redirect("mainpage")
    id_uzytkownika = int(id_uzytkownika)
    try:
        u = get_user_by_id(request, id_uzytkownika)
    except Uzytkownik.DoesNotExist:
        return redirect("admin_uzytkownicy")
    u.delete()
    return redirect("admin_uzytkownicy")


def admin_zmien_prawa(request, id_uzytkownika):
    if request.user.is_anonymous == True:
        return redirect("login")
    elif request.user.is_admin == False:
        return redirect("mainpage")
    change_user_permissions(request, id_uzytkownika)
    return redirect("admin_uzytkownicy")


def admin_zamowienia_uzytkownika(request, id_uzytkownika):
    if request.user.is_anonymous == True:
        return redirect("login")
    elif request.user.is_admin == False:
        return redirect("mainpage")
    user_orders = get_user_orders_by_id(request, id_uzytkownika)

    page = request.GET.get("page", 1)
    paginator = Paginator(user_orders, 15)
    try:
        order = paginator.page(page)
    except PageNotAnInteger:
        order = paginator.page(1)
    except EmptyPage:
        order = paginator.page(paginator.num_pages)

    return render(request, "admin_zamowienia_uzytkownika.html", {"user_orders": order})


def admin_zmien_status_potwierdzenia(request, id_zamowienia):
    if request.user.is_anonymous == True:
        return redirect("login")
    elif request.user.is_admin == False:
        return redirect("mainpage")
    change_order_confirm_status(request, id_zamowienia)
    order = get_order_by_id(request, id_zamowienia)
    if order.czy_potwierdzone == True:
        actual_balance = float(order.zamawiajacy.balance)
        new_balance = float(actual_balance) - float(order.do_zaplaty)
        actual_waiting_balance = float(order.zamawiajacy.waiting_balance)
        new_waiting_balance = float(actual_waiting_balance) - float(order.do_zaplaty)
        user_email = order.zamawiajacy.email
        user_to_update = Uzytkownik.objects.filter(email=user_email).update(
            balance=new_balance, waiting_balance=new_waiting_balance
        )
    else:
        actual_balance = float(order.zamawiajacy.balance)
        new_balance = float(actual_balance) + float(order.do_zaplaty)
        actual_waiting_balance = float(order.zamawiajacy.waiting_balance)
        new_waiting_balance = float(actual_waiting_balance) + float(order.do_zaplaty)
        user_email = order.zamawiajacy.email
        user_to_update = Uzytkownik.objects.filter(email=user_email).update(
            balance=new_balance, waiting_balance=new_waiting_balance
        )
    return redirect("admin_zamowienia_uzytkownika", id_uzytkownika=order.zamawiajacy.ID)


def admin_zmien_status_anulowania(request, id_zamowienia):
    if request.user.is_anonymous == True:
        return redirect("login")
    elif request.user.is_admin == False:
        return redirect("mainpage")
    change_order_cancel_status(request, id_zamowienia)
    order = get_order_by_id(request, id_zamowienia)
    if order.czy_anulowano == True:
        actual_waiting_balance = float(order.zamawiajacy.waiting_balance)
        new_waiting_balance = float(actual_waiting_balance) - float(order.do_zaplaty)
        user_email = order.zamawiajacy.email
        user_to_update = Uzytkownik.objects.filter(email=user_email).update(
            waiting_balance=new_waiting_balance
        )
    else:
        actual_waiting_balance = float(order.zamawiajacy.waiting_balance)
        new_waiting_balance = float(actual_waiting_balance) + float(order.do_zaplaty)
        user_email = order.zamawiajacy.email
        user_to_update = Uzytkownik.objects.filter(email=user_email).update(
            waiting_balance=new_waiting_balance
        )
    return redirect("admin_zamowienia_uzytkownika", id_uzytkownika=order.zamawiajacy.ID)


def admin_zamowienia_view(request):
    if request.user.is_anonymous == True:
        return redirect("login")
    elif request.user.is_admin == False:
        return redirect("mainpage")
    orders = get_all_orders(request)

    confirmed_query = request.GET.get("confirmed")
    canceled_query = request.GET.get("canceled")
    paid_query = request.GET.get("paid")
    username_query = request.GET.get("username")
    email_query = request.GET.get("email")
    if (
        confirmed_query != ""
        and confirmed_query != "---"
        and confirmed_query is not None
    ):
        orders = orders.filter(czy_potwierdzone__icontains=confirmed_query.strip())
    if canceled_query != "" and canceled_query != "---" and canceled_query is not None:
        orders = orders.filter(czy_anulowano__icontains=canceled_query.strip())
    if paid_query != "" and paid_query != "---" and paid_query is not None:
        orders = orders.filter(czy_oplacone__icontains=paid_query.strip())
    if username_query != "" and username_query is not None:
        orders = orders.filter(zamawiajacy__username__icontains=username_query.strip())
    if email_query != "" and email_query is not None:
        orders = orders.filter(zamawiajacy__email__icontains=email_query.strip())

    page = request.GET.get("page", 1)
    paginator = Paginator(orders, 10)
    try:
        order = paginator.page(page)
    except PageNotAnInteger:
        order = paginator.page(1)
    except EmptyPage:
        order = paginator.page(paginator.num_pages)

    return render(request, "admin_zamowienia.html", {"orders": order})


def admin_skladniki_dania_view(request):
    if request.user.is_anonymous == True:
        return redirect("login")
    elif request.user.is_admin == False:
        return redirect("mainpage")
    skladniki_dania = get_all_ingridients_dishes(request)

    ingridient_query = request.GET.get("skladnik")
    dish_query = request.GET.get("danie")

    if ingridient_query != "" and ingridient_query is not None:
        skladniki_dania = skladniki_dania.filter(
            skladnik__nazwa_skladnika__icontains=ingridient_query.strip()
        )
    if dish_query != "" and dish_query is not None:
        skladniki_dania = skladniki_dania.filter(
            danie__nazwa_dania__icontains=dish_query.strip()
        )

    return render(
        request, "admin_skladniki_dania.html", {"skladniki_dania": skladniki_dania}
    )


def admin_skladniki_dania_create(request):
    if request.user.is_anonymous == True:
        return redirect("login")
    elif request.user.is_admin == False:
        return redirect("mainpage")
    form = SkladnikiDaniaCreate(request.POST or None, request.FILES)
    if form.is_valid():
        form.save()
        return redirect("admin_skladniki_dania")
    return render(
        request, "admin_skladniki_dania_add.html", {"add_skladnik_dania": form}
    )


def admin_skladniki_dania_delete(request, id_skladniki_dania):
    if request.user.is_anonymous == True:
        return redirect("login")
    elif request.user.is_admin == False:
        return redirect("mainpage")
    id_skladniki_dania = int(id_skladniki_dania)
    try:
        skladnik_danie = get_ingridient_dish_by_id(request, id_skladniki_dania)
    except Skladnik_dania.DoesNotExist:
        return redirect("admin_skladniki_dania")
    skladnik_danie.delete()
    return redirect("admin_skladniki_dania")


def admin_skladniki_dania_update(request, id_skladniki_dania):
    if request.user.is_anonymous == True:
        return redirect("login")
    elif request.user.is_admin == False:
        return redirect("mainpage")
    id_skladniki_dania = int(id_skladniki_dania)
    try:
        skladnik_danie = get_ingridient_dish_by_id(request, id_skladniki_dania)
    except Skladnik_dania.DoesNotExist:
        return redirect("admin_skladniki_dania")
    form = SkladnikiDaniaCreate(
        request.POST or None, request.FILES or None, instance=skladnik_danie
    )
    if form.is_valid():
        form.save()
        return redirect("admin_skladniki_dania")
    return render(
        request, "admin_skladniki_dania_add.html", {"add_skladnik_dania": form}
    )


def admin_dania_zestawy_view(request):
    if request.user.is_anonymous == True:
        return redirect("login")
    elif request.user.is_admin == False:
        return redirect("mainpage")
    dania_zestawy = get_all_sets_dishes(request)

    dish_query = request.GET.get("danie")
    set_query = request.GET.get("zestaw")

    if set_query != "" and set_query is not None:
        dania_zestawy = dania_zestawy.filter(
            zestaw__nazwa_zestawu__icontains=set_query.strip()
        )
    if dish_query != "" and dish_query is not None:
        dania_zestawy = dania_zestawy.filter(
            danie__nazwa_dania__icontains=dish_query.strip()
        )

    return render(request, "admin_dania_zestawy.html", {"dania_zestawy": dania_zestawy})


def admin_dania_zestawy_create(request):
    if request.user.is_anonymous == True:
        return redirect("login")
    elif request.user.is_admin == False:
        return redirect("mainpage")
    form = ZestawDanCreate(request.POST or None, request.FILES)
    if form.is_valid():
        form.save()
        return redirect("admin_dania_zestawy")
    return render(request, "admin_dania_zestawy_add.html", {"add_danie_zestaw": form})


def admin_dania_zestawy_delete(request, id_dania_zestawy):
    if request.user.is_anonymous == True:
        return redirect("login")
    elif request.user.is_admin == False:
        return redirect("mainpage")
    id_dania_zestawy = int(id_dania_zestawy)
    try:
        zestaw_danie = get_set_dish_by_id(request, id_dania_zestawy)
    except Zestaw_dan.DoesNotExist:
        return redirect("admin_dania_zestawy")
    zestaw_danie.delete()
    return redirect("admin_dania_zestawy")


def admin_dania_zestawy_update(request, id_dania_zestawy):
    if request.user.is_anonymous == True:
        return redirect("login")
    elif request.user.is_admin == False:
        return redirect("mainpage")
    id_dania_zestawy = int(id_dania_zestawy)
    try:
        zestaw_danie = get_set_dish_by_id(request, id_dania_zestawy)
    except Zestaw_dan.DoesNotExist:
        return redirect("admin_dania_zestawy")
    form = ZestawDanCreate(
        request.POST or None, request.FILES or None, instance=zestaw_danie
    )
    if form.is_valid():
        form.save()
        return redirect("admin_dania_zestawy")
    return render(request, "admin_dania_zestawy_add.html", {"add_danie_zestaw": form})


def admin_zmien_status_pot(request, id_zamowienia):
    if request.user.is_anonymous == True:
        return redirect("login")
    elif request.user.is_admin == False:
        return redirect("mainpage")
    change_order_confirm_status(request, id_zamowienia)
    order = get_order_by_id(request, id_zamowienia)
    if order.czy_potwierdzone == True:
        actual_balance = float(order.zamawiajacy.balance)
        new_balance = float(actual_balance) - float(order.do_zaplaty)
        actual_waiting_balance = float(order.zamawiajacy.waiting_balance)
        new_waiting_balance = float(actual_waiting_balance) - float(order.do_zaplaty)
        user_email = order.zamawiajacy.email
        user_to_update = Uzytkownik.objects.filter(email=user_email).update(
            balance=new_balance, waiting_balance=new_waiting_balance
        )
    else:
        actual_balance = float(order.zamawiajacy.balance)
        new_balance = float(actual_balance) + float(order.do_zaplaty)
        actual_waiting_balance = float(order.zamawiajacy.waiting_balance)
        new_waiting_balance = float(actual_waiting_balance) + float(order.do_zaplaty)
        user_email = order.zamawiajacy.email
        user_to_update = Uzytkownik.objects.filter(email=user_email).update(
            balance=new_balance, waiting_balance=new_waiting_balance
        )
    return redirect("admin_zamowienia")


def admin_zmien_status_anul(request, id_zamowienia):
    if request.user.is_anonymous == True:
        return redirect("login")
    elif request.user.is_admin == False:
        return redirect("mainpage")
    change_order_cancel_status(request, id_zamowienia)
    order = get_order_by_id(request, id_zamowienia)
    if order.czy_anulowano == True:
        actual_waiting_balance = float(order.zamawiajacy.waiting_balance)
        new_waiting_balance = float(actual_waiting_balance) - float(order.do_zaplaty)
        user_email = order.zamawiajacy.email
        user_to_update = Uzytkownik.objects.filter(email=user_email).update(
            waiting_balance=new_waiting_balance
        )
    else:
        actual_waiting_balance = float(order.zamawiajacy.waiting_balance)
        new_waiting_balance = float(actual_waiting_balance) + float(order.do_zaplaty)
        user_email = order.zamawiajacy.email
        user_to_update = Uzytkownik.objects.filter(email=user_email).update(
            waiting_balance=new_waiting_balance
        )
    return redirect("admin_zamowienia")


def admin_uzytkownik_zmien_saldo(request, id_uzytkownika):
    if request.user.is_anonymous == True:
        return redirect("login")
    elif request.user.is_admin == False:
        return redirect("mainpage")
    try:
        user = get_user_by_id(request, id_uzytkownika)
    except Uzytkownik.DoesNotExist:
        return redirect("admin_uzytkownicy")
    form = UzytkownikEditSaldo(
        request.POST or None, request.FILES or None, instance=user
    )
    if form.is_valid():
        form.save()
        return redirect("admin_uzytkownicy")
    return render(request, "admin_uzytkownik_saldo.html", {"edit_balance": form})


def admin_dodaj_zmien_komentarz1(request, id_zamowienia):
    if request.user.is_anonymous == True:
        return redirect("login")
    elif request.user.is_admin == False:
        return redirect("mainpage")
    try:
        order = get_order_by_id(request, id_zamowienia)
    except Zamowienie.DoesNotExist:
        return redirect(
            "admin_zamowienia_uzytkownika", id_uzytkownika=order.zamawiajacy.ID
        )
    form = AdminDodajZmienKomentarzAnulowania(
        request.POST or None, request.FILES or None, instance=order
    )
    if form.is_valid():
        form.save()
        return redirect(
            "admin_zamowienia_uzytkownika", id_uzytkownika=order.zamawiajacy.ID
        )
    return render(request, "admin_dodaj_zmien_komentarz1.html", {"comment": form})


def admin_dodaj_zmien_komentarz2(request, id_zamowienia):
    if request.user.is_anonymous == True:
        return redirect("login")
    elif request.user.is_admin == False:
        return redirect("mainpage")
    try:
        order = get_order_by_id(request, id_zamowienia)
    except Zamowienie.DoesNotExist:
        return redirect("admin_zamowienia")
    form = AdminDodajZmienKomentarzAnulowania(
        request.POST or None, request.FILES or None, instance=order
    )
    if form.is_valid():
        form.save()
        return redirect("admin_zamowienia")
    return render(request, "admin_dodaj_zmien_komentarz1.html", {"comment": form})


def admin_zmien_status_oplacenia(request, id_zamowienia):
    if request.user.is_anonymous == True:
        return redirect("login")
    elif request.user.is_admin == False:
        return redirect("mainpage")
    change_order_payment_status(request, id_zamowienia)
    order = get_order_by_id(request, id_zamowienia)
    if order.czy_oplacone == True:
        actual_balance = float(order.zamawiajacy.balance)
        new_balance = float(actual_balance) + float(order.do_zaplaty)
        user_email = order.zamawiajacy.email
        user_to_update = Uzytkownik.objects.filter(email=user_email).update(
            balance=new_balance
        )
    else:
        actual_balance = float(order.zamawiajacy.balance)
        new_balance = float(actual_balance) - float(order.do_zaplaty)
        actual_waiting_balance = float(order.zamawiajacy.waiting_balance)
        user_email = order.zamawiajacy.email
        user_to_update = Uzytkownik.objects.filter(email=user_email).update(
            balance=new_balance
        )
    return redirect("admin_zamowienia_uzytkownika", id_uzytkownika=order.zamawiajacy.ID)


def admin_zmien_status_oplac(request, id_zamowienia):
    if request.user.is_anonymous == True:
        return redirect("login")
    elif request.user.is_admin == False:
        return redirect("mainpage")
    change_order_payment_status(request, id_zamowienia)
    order = get_order_by_id(request, id_zamowienia)
    if order.czy_oplacone == True:
        actual_balance = float(order.zamawiajacy.balance)
        new_balance = float(actual_balance) + float(order.do_zaplaty)
        user_email = order.zamawiajacy.email
        user_to_update = Uzytkownik.objects.filter(email=user_email).update(
            balance=new_balance
        )
    else:
        actual_balance = float(order.zamawiajacy.balance)
        new_balance = float(actual_balance) - float(order.do_zaplaty)
        actual_waiting_balance = float(order.zamawiajacy.waiting_balance)
        user_email = order.zamawiajacy.email
        user_to_update = Uzytkownik.objects.filter(email=user_email).update(
            balance=new_balance
        )
    return redirect("admin_zamowienia")
