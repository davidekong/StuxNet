from django.contrib import admin
from django.contrib.sites.models import Site
from stux_auth.models import CustomUser, OneTimePassword

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(OneTimePassword)