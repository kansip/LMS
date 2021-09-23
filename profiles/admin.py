from django.contrib import admin
from django.contrib.auth.models import User,Group

# Register your models here.
class MyUserAdmin(admin.ModelAdmin):
    pass
admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)

class MyGroupAdmin(admin.ModelAdmin):
    pass
admin.site.unregister(Group)
admin.site.register(Group, MyGroupAdmin)

