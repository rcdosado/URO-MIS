from django.contrib import admin
from employees.admin import CustomUserAdmin
from employees.models import Employee
from publications.models import Article, Publication, Author, ArticleAuthors, Discipline, Publisher


class PublisherAdmin(admin.ModelAdmin):
    model = Publisher 

admin.site.register(Publisher, PublisherAdmin)


class DisciplineAdmin(admin.ModelAdmin):
    model = Discipline

admin.site.register(Discipline, DisciplineAdmin)


class EmployeeAdmin(admin.ModelAdmin):
    model = CustomUserAdmin

admin.site.register(Employee, EmployeeAdmin)


class AuthorAdmin(admin.ModelAdmin):
    model = Employee
    exclude = ('articles', )

admin.site.register(Author, AuthorAdmin)


class AuthorInline(admin.TabularInline):
    model = ArticleAuthors
    can_delete = True
    verbose_name_plural = 'Authors'
    extra = 1


class ArticleAdmin(admin.ModelAdmin):
    inlines = [AuthorInline, ]
    list_display = ('title', 'publication', 'list_authors',)


admin.site.register(Article, ArticleAdmin)

'''
class ArticleInline(admin.StackedInline):
    model = Article
    can_delete = False
    verbose_name_plural = 'Articles'
    extra = 1
'''


class PublicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'list_articles',)
    model = Publication


admin.site.register(Publication, PublicationAdmin)

