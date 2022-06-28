from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Participant, Team

# Register your models here.

##Team##
class TeamResource(resources.ModelResource):
    class Meta:
        model = Team
        exclude = ('id',)
        import_id_fields = ('uuid',)


class TeamAdmin(ImportExportModelAdmin):
    resource_class = TeamResource
    list_display = ('uuid','teamName', 'points', 'position', 'board')
    list_display_links = ('uuid', 'teamName')
    list_filter = ('position',)
    search_fields = ('uuid','teamName', 'position')
    list_per_page = 25

admin.site.register(Team, TeamAdmin)

##Participant##
class ParticipantResource(resources.ModelResource):
    class Meta:
        model = Participant

class ParticipantAdmin(ImportExportModelAdmin):
    resource_class = ParticipantResource
    list_display = ('id', 'name', 'email', 'rollno', 'team')
    list_display_links = ('id', 'name')
    list_filter = ('team',)
    search_fields = ('name', 'email', 'rollno', 'team')
    list_per_page = 25

admin.site.register(Participant, ParticipantAdmin)

