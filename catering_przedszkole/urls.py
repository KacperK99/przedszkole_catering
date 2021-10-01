from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('signup/', views.registration_view, name="signup"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('mainpage/', views.mainpage_view, name="mainpage"),
    path('mainpage/zestaw/<int:id_zestaw>', views.zestaw_view, name="zestaw"),
    path('mainpage/zestaw/zamow/<int:id_zestaw>', views.zamow_view, name="zamow"),
    path('mainpage/zamowienia/', views.zamowienia_view, name="zamowienia"),
    path('mainpage/konto/', views.mojekonto_view, name="konto"),
    path('mainpage/konto/edytujkonto/<int:id_uzytkownika>', views.mojekonto_update, name="edytujkonto"),
    path('mainpage/zamowienia/edytujzamowienie/<int:id_zamowienia>', views.zamowienie_update, name="edytujzamowienie"),
    path('mainpage/zamowienia/zamowienie_anuluj/<int:id_zam>', views.zamowienie_anuluj),

    path('adminpage/', views.adminpage_view, name="adminpage"),

    path('adminpage/admin_skladniki', views.admin_skladniki_view, name="admin_skladniki"),
    path('adminpage/admin_skladniki/admin_skladnik_add', views.admin_skladnik_create, name='admin_skladnik_add'),
    path('adminpage/admin_skladniki/admin_skladnik_delete/<int:id_skladnik>', views.admin_skladnik_delete),
    path('adminpage/admin_skladniki/admin_skladnik_update/<int:id_skladnik>', views.admin_skladnik_update, name='admin_skladnik_update'),

    path('adminpage/admin_dania', views.admin_dania_view, name="admin_dania"),
    path('adminpage/admin_dania/admin_danie_add', views.admin_danie_create, name='admin_danie_add'),
    path('adminpage/admin_dania/admin_danie_delete/<int:id_dania>', views.admin_danie_delete),
    path('adminpage/admin_dania/admin_danie_update/<int:id_dania>', views.admin_danie_update, name='admin_danie_update'),

    path('adminpage/admin_typy_dan', views.admin_typy_dan_view, name="admin_typy_dan"),
    path('adminpage/admin_typy_dan/admin_typ_dania_add', views.admin_typ_dania_create, name='admin_typ_dania_add'),
    path('adminpage/admin_typy_dan/admin_typ_dania_delete/<int:id_typu_dania>', views.admin_typ_dania_delete),
    path('adminpage/admin_typy_dan/admin_typ_dania_update/<int:id_typu_dania>', views.admin_typ_dania_update, name='admin_typ_dania_update'),

    path('adminpage/admin_zestawy', views.admin_zestawy_view, name="admin_zestawy"),
    path('adminpage/admin_zestawy/admin_zestaw_add', views.admin_zestaw_create, name='admin_zestaw_add'),
    path('adminpage/admin_zestawy/admin_zestaw_delete/<int:id_zestawu>', views.admin_zestaw_delete),
    path('adminpage/admin_zestawy/admin_zestaw_update/<int:id_zestawu>', views.admin_zestaw_update, name='admin_typ_zestaw_update'),
    path('adminpage/admin_zestawy/admin_zmien_widocznosc/<int:id_zestawu>', views.admin_zmien_widocznosc, name='admin_zmien_widocznosc'),

    path('adminpage/admin_uzytkownicy', views.admin_uzytkownicy_view, name="admin_uzytkownicy"),
    path('adminpage/admin_uzytkownicy/admin_uzytkownik_delete/<int:id_uzytkownika>', views.admin_uzytkownik_delete),
    path('adminpage/admin_uzytkownicy/admin_zmien_prawa/<int:id_uzytkownika>', views.admin_zmien_prawa, name='admin_zmien_prawa'),
    path('adminpage/admin_uzytkownicy/admin_edytuj_saldo/<int:id_uzytkownika>', views.admin_uzytkownik_zmien_saldo, name='admin_edytuj_saldo'),
    path('adminpage/admin_uzytkownicy/admin_zamowienia_uzytkownika/<int:id_uzytkownika>', views.admin_zamowienia_uzytkownika, name='admin_zamowienia_uzytkownika'),
    path('adminpage/admin_uzytkownicy/admin_zamowienia_uzytkownika/admin_zmien_status_potwierdzenia/<int:id_zamowienia>', views.admin_zmien_status_potwierdzenia, name='admin_zmien_status_potwierdzenia'),
    path('adminpage/admin_uzytkownicy/admin_zamowienia_uzytkownika/admin_zmien_status_oplacenia/<int:id_zamowienia>', views.admin_zmien_status_oplacenia, name='admin_zmien_status_oplacenia'),
    path('adminpage/admin_uzytkownicy/admin_zamowienia_uzytkownika/admin_zmien_status_anulowania/<int:id_zamowienia>', views.admin_zmien_status_anulowania, name='admin_zmien_status_anulowania'),
    path('adminpage/admin_uzytkownicy/admin_zamowienia_uzytkownika/admin_dodaj_zmien_komentarz1/<int:id_zamowienia>', views.admin_dodaj_zmien_komentarz1, name='admin_dodaj_zmien_komentarz1'),
    
    path('adminpage/admin_zamowienia', views.admin_zamowienia_view, name="admin_zamowienia"),
    path('adminpage/admin_zamowienia/admin_zmien_status_pot/<int:id_zamowienia>', views.admin_zmien_status_pot, name='admin_zmien_status_pot'),
    path('adminpage/admin_zamowienia/admin_zmien_status_oplac/<int:id_zamowienia>', views.admin_zmien_status_oplac, name='admin_zmien_status_oplac'),
    path('adminpage/admin_zamowienia/admin_zmien_status_anul/<int:id_zamowienia>', views.admin_zmien_status_anul, name='admin_zmien_status_anul'),
    path('adminpage/admin_zamowienia/admin_dodaj_zmien_komentarz2/<int:id_zamowienia>', views.admin_dodaj_zmien_komentarz2, name='admin_dodaj_zmien_komentarz2'),
        
    path('adminpage/admin_skladniki_dania', views.admin_skladniki_dania_view, name="admin_skladniki_dania"),
    path('adminpage/admin_skladniki_dania/admin_skladniki_dania_add', views.admin_skladniki_dania_create, name='admin_skladniki_dania_add'),
    path('adminpage/admin_skladniki_dania/admin_skladniki_dania_delete/<int:id_skladniki_dania>', views.admin_skladniki_dania_delete),
    path('adminpage/admin_skladniki_dania/admin_skladniki_dania_update/<int:id_skladniki_dania>', views.admin_skladniki_dania_update, name='admin_skladniki_dania_update'),

    path('adminpage/admin_dania_zestawy', views.admin_dania_zestawy_view, name="admin_dania_zestawy"),
    path('adminpage/admin_dania_zestawy/admin_dania_zestawy_add', views.admin_dania_zestawy_create, name='admin_dania_zestawy_add'),
    path('adminpage/admin_dania_zestawy/admin_dania_zestawy_delete/<int:id_dania_zestawy>', views.admin_dania_zestawy_delete),
    path('adminpage/admin_dania_zestawy/admin_dania_zestawy_update/<int:id_dania_zestawy>', views.admin_dania_zestawy_update, name='admin_dania_zestawy_update'),

]