from django.contrib import admin
from badge.models import Badge
from badge.models import Award

class BadgeAdmin(admin.ModelAdmin):
    list_display = ('title', 'active', 'author_uri', 'date_created', )
    list_filter = ('date_created', 'author_uri', )

class AwardAdmin(admin.ModelAdmin):
    list_display = ('badge', 'user_uri', 'expert_uri', 'ob_date_published' )
    list_filter = ('badge', 'ob_date_published', )


admin.site.register(Badge, BadgeAdmin)
admin.site.register(Award, AwardAdmin)