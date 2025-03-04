from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
admin.site.register(Worker)
admin.site.register(Company)
admin.site.register(Work)
admin.site.register(Progress)
admin.site.register(ProgressItem)
admin.site.register(Expanses)
admin.site.register(DateforProgress)
admin.site.register(Progresstype)
admin.site.register(User)