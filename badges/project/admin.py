from django.contrib import admin
from project.processors import Project
from project.processors import Revision
from project.processors import Feedback

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'work_url', 'badge_uri', 'author_uri', 'date_created', 'date_updated', )
    list_filter = ('title', 'badge_uri', 'date_created', 'author_uri', )

class RevisionAdmin(admin.ModelAdmin):
    list_display = ('project', 'date_created' )
    list_filter = ('project', 'date_created', )

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('project', 'revision', 'expert_uri', 'date_created', 'badge_awarded' )
    list_filter = ('project', 'badge_awarded', 'date_created', )


admin.site.register(Project, ProjectAdmin)
admin.site.register(Revision, RevisionAdmin)
admin.site.register(Feedback, FeedbackAdmin)