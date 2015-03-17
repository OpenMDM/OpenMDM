from django.contrib import admin
from public_gate.models import PropertyList, EmailAccountProperty, RestrictionsProperty
# Register your models here.


class EmailInLine(admin.StackedInline):
    model = EmailAccountProperty
    extra = 0


class RestrictionInLine(admin.StackedInline):
    model = RestrictionsProperty
    extra = 0


class PropertyAdmin(admin.ModelAdmin):
    inlines = [EmailInLine, RestrictionInLine]


admin.site.register(PropertyList, PropertyAdmin)