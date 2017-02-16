from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Unit, Department, Rank, Campus, AreaOfDiscipline, Employee, Attainment, Expertise


class AreaOfDisciplineAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name',)

admin.site.register(AreaOfDiscipline, AreaOfDisciplineAdmin)


class CampusAdmin(admin.ModelAdmin):
    list_display = ('name', 'head', 'address')
    search_fields = ('name', )

admin.site.register(Campus, CampusAdmin)


class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'division')
    search_fields = ('name', )

admin.site.register(Unit, UnitAdmin)


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('title',)

admin.site.register(Department, DepartmentAdmin)


class RankAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Rank, RankAdmin)


class EmployeeInline(admin.StackedInline):
    model = Employee
    can_delete = False
    verbose_name_plural = 'Employee Profile'
    exclude = ('education', )
    fk_name = 'user'


class AttainmentInline(admin.StackedInline):
    model = Attainment
    can_delete = False
    verbose_name_plural = 'Educational Attainment'
    fk_name = 'user'


class ExpertiseInline(admin.StackedInline):
    model = Expertise
    can_delete = False
    verbose_name_plural = 'Expert Pool'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (EmployeeInline, AttainmentInline, ExpertiseInline)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'attainment', 'age', 'years')
    list_select_related = ('employee', 'attainment', 'expertise', )

    # obj here holds instance of Admin
    # example how to access other fields from other Apps
    #
    # def the_attainment(self, obj):
    #     return obj.attainment.get_highest_attainment()

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

    def age(self, obj):
        return obj.employee.age()

    def years(self, obj):
        return obj.employee.get_years_in_service()


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


