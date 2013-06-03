from django.contrib import admin
from .models import User
from .models import Partner

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'image_url', )
    list_filter = ('date_joined', 'date_updated', )

class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_filter = ('name', )


admin.site.register(User, UserAdmin)
admin.site.register(Partner, PartnerAdmin)