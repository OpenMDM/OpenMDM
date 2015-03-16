from django.contrib import admin
from public_gate.models import PropertyList, EmailAccount, Restrictions
# Register your models here.


class EmailInLine(admin.StackedInline):
    model = EmailAccount
    extra = 0


class RestrictionInLine(admin.StackedInline):
    model = Restrictions
    extra = 0


class PropertyAdmin(admin.ModelAdmin):
    inlines = [EmailInLine, RestrictionInLine]


admin.site.register(PropertyList, PropertyAdmin)