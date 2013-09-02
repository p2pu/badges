from django.contrib import admin
from django.db.models import F
from django.db.models import Q
from badge.models import Badge
from badge.models import Award

class BadgePublishedFilter(admin.SimpleListFilter):
    title = ('Published')
    parameter_name = 'published'
    def lookups(self, request, model_admin):

         return (
            ('published',           'Published'),
            ('unpublished',         'Not published'),
            ('publishedeleted',     'Published but deleted'),
            ('unpublishedeleted',   'Not published and deleted'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'published':
            return queryset.filter(date_published__isnull=False)

        if self.value() == 'unpublished':
            return queryset.filter(date_published__isnull=True)

        if self.value() == 'publishedeleted':
            return queryset.filter(date_published__isnull=False, deleted=True)

        if self.value() == 'unpublishedeleted':
            return queryset.filter(date_published__isnull=True, deleted=True)


class AwardsEarnedAndPushedFilter(admin.SimpleListFilter):
    title = 'Earned'
    parameter_name = 'project'

    def lookups(self, request, model_admin):
         return (
            ('pushed',          'Pushed to backpack'),
            ('earned',          'Earned by project'),
            ('earnedandpushed', 'Earned by project and pushed'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'pushed':
            return queryset.filter(ob_date_published__isnull=False)

        if self.value() == 'earned':
            return queryset.filter(~Q(user_uri__exact=F('expert_uri')))

        if self.value() == 'earnedandpushed':
            return queryset.filter(~Q(user_uri__exact=F('expert_uri')), ob_date_published__isnull=False)


class BadgeAdmin(admin.ModelAdmin):
    list_display = ('title', 'deleted', 'author_uri', 'pk', 'partner_name', 'date_created', )
    list_filter = ('date_created', BadgePublishedFilter, )


class AwardAdmin(admin.ModelAdmin):
    list_display = ('badge', 'user_uri', 'expert_uri', 'evidence_url', 'ob_date_published' )
    list_filter = (AwardsEarnedAndPushedFilter, 'badge',)


admin.site.register(Badge, BadgeAdmin)
admin.site.register(Award, AwardAdmin)