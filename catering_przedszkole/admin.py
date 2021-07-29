from django.contrib import admin
from catering_przedszkole.models import Uzytkownik, Skladnik, Skladnik_dania, Danie, Zestaw_dan, Typ_dania, Zestaw, Zamowienie
from django.contrib.auth.admin import UserAdmin
# Register your models here.



class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'is_admin', 'phone_number')
    search_fields = ('email', 'username')
    readonly_fields = ('ID',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Uzytkownik, AccountAdmin)
admin.site.register(Skladnik)
admin.site.register(Typ_dania)
admin.site.register(Danie)
admin.site.register(Skladnik_dania)
admin.site.register(Zestaw)
admin.site.register(Zestaw_dan)
admin.site.register(Zamowienie)