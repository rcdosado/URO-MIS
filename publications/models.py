from __future__ import unicode_literals

from django.db import models
from employees.models import Employee
from mis.base import BaseProfile

class Publisher(BaseProfile):
    title = models.CharField(max_length=256)


    def __str__(self):
        return self.title

class Publication(BaseProfile):
    PUBLICATION_TYPES = (
        ('0', 'zero'),
        ('1', 'one'),
        ('2', 'two'),
        ('3', 'three')
    )
    title = models.CharField(max_length=256, blank=True)
    type = models.CharField(max_length=1, choices=PUBLICATION_TYPES, help_text="Types of Publication")
    editor = models.ForeignKey(Employee, null=True, help_text="Choose the editor, or leave blank if unknown")
    issn = models.CharField(max_length=8, blank=True,help_text="Enter the 8 Digit ISSN Number of the publication")
    vol_num = models.PositiveIntegerField(blank=True)
    issue_num = models.PositiveIntegerField(blank=True)
    date_published = models.DateField(blank=True, help_text="Date Published (make sure year is accurate)")
    doi = models.CharField(max_length=60, blank=True, help_text="Enter the DOI of the publication")


    def list_articles(self):
        return ", ".join([article.title for article in Article.objects.filter(publication__id=self.id)])
        # import pdb; pdb.set_trace()
        # pass

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)


class Discipline(BaseProfile):
    name = models.CharField(max_length=256, help_text='Add discipline here i.e Marketing, InfoTech, Engineering ')

    def __str__(self):
        return self.name

class Article(BaseProfile):
    title = models.CharField(max_length=256, help_text="Title of Article")
    abstract = models.TextField(max_length=256, blank=True, help_text="Enter Abstract here")
    start_page = models.PositiveIntegerField(blank=True, help_text="Start page in the publication")
    end_page = models.PositiveIntegerField(blank=True, help_text="End page in the publication")
    publication = models.ForeignKey(Publication, null=True, blank=True, related_name='publication')
    disciplines = models.ManyToManyField(Discipline, through='articlediscipline', related_name='discipline')
    keywords = models.CharField(max_length=256, blank=True, help_text="Enter keywords here")


    def __str__(self):
        return "{} by {}".format(self.title, self.list_authors())

    def list_authors(self):
        return ", ".join([str(author.author.employee) for author in ArticleAuthors.objects.filter(article__id=self.id)])

    def save(self, *args, **kwargs):
        # put code here to set authors order
        print(" article saved!!")
        super(Article, self).save(*args, **kwargs)

    class Meta:
        ordering = ('title',)


class ArticleDiscipline(BaseProfile):
    discipline = models.ForeignKey(Discipline, help_text="Choose Discipline")
    article = models.ForeignKey(Article, help_text="Choose the article")
    info = models.CharField(max_length=50, help_text="Info")

    def __str__(self):
        return self.article + ' ' + self.discipline


class Author(BaseProfile):
    employee = models.OneToOneField(Employee, related_name='authors')
    articles = models.ManyToManyField(Article, through='articleauthors', related_name='articles')
    info = models.TextField(max_length=256, blank=True, help_text="Add info here")

    def __str__(self): return self.employee.get_display_name()


class ArticleAuthors(BaseProfile):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    authorship = models.IntegerField(null=True, blank=True)

    @classmethod
    def create(cls, article, author, authorship):
        #import pdb;pdb.set_trace()
        article =cls(article=article)
        return articleauthors

    class Meta:
        ordering = ('authorship',)
