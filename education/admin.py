from django.contrib import admin

from education.models import Undergrad, Masteral, Doctoral, Attainment


class UndergradAdmin(admin.ModelAdmin):
    list_display = ('degree', 'employee_count')
    list_filter = ('degree',)
    search_fields = ('degree', 'updated')


admin.site.register(Undergrad, UndergradAdmin)


class MasteralAdmin(admin.ModelAdmin):
    list_display = ('degree', 'remarks', 'employee_count')
    list_filter = ('degree',)
    search_fields = ('degree', 'updated')


admin.site.register(Masteral, MasteralAdmin)


class DoctoralAdmin(admin.ModelAdmin):
    list_display = ('degree', 'remarks', 'employee_count')
    list_filter = ('degree',)
    search_fields = ('degree', 'updated')

admin.site.register(Doctoral, DoctoralAdmin)


# class AttainmentAdmin(admin.ModelAdmin):
#     list_display = ('user', 'undergrad', 'masteral', 'doctorate', )
#     list_filter = ('user', )
#     search_fields = ('undergrad.degree', 'masteral.degree', 'doctorate.degree', )
#
# admin.site.register(Attainment, AttainmentAdmin)
