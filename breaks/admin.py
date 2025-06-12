from django.contrib import admin
from django.db.models import Count

from breaks.models import groups
from breaks.models.breaks import Break
from breaks.models.dicts import BreakStatus, ReplacementStatus
from breaks.models.organisations import Organisation
from breaks.models.groups import Group
from breaks.models.replacements import Replacement, ReplacementEmployee


##############################
# INLINES
##############################
class ReplacementEmployeeInline(admin.TabularInline):
    model = ReplacementEmployee
    fields = ('employee', 'status')


##############################
# MODELS
##############################
@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'director')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'manager', 'min_active')
    # list_display = ('id', 'name', 'manager', 'min_active', 'replacement_count')

    # def replacement_count(self, obj):
    #     return obj.replacement_count
    #
    # replacement_count.short_description = "Кол-во смен"
    #
    # def get_gueryset(self, request):
    #     queryset = groups.Group.objects.annotate(
    #         replacement_count=Count('replacements__id')
    #     )
    #     return queryset


@admin.register(Replacement)
class ReplacementAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'group',
        'date',
        'break_start',
        'break_end',
        'break_max_duration'
    )
    inlines = (ReplacementEmployeeInline,)


@admin.register(ReplacementStatus)
class ReplacementStatusAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'sort', 'active')


@admin.register(BreakStatus)
class BreakStatusAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'sort', 'active')


@admin.register(ReplacementEmployee)
class ReplacementEmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee', 'replacement', 'status')


@admin.register(Break)
class BreakAdmin(admin.ModelAdmin):
    list_display = ('replacement', 'employee', 'break_start','break_end')
