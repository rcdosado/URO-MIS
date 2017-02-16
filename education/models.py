from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from mis.base import BaseProfile

		
# EDUCATION
class Undergrad(BaseProfile):
    ini = models.CharField(max_length=32, default='None', help_text='e.g BSIT, BSECE, BSBA etc')
    degree = models.CharField(max_length=128, default='None', help_text='Enter Undergrad course here')
    units = models.PositiveIntegerField(null=True, blank=True)
    year_graduated = models.PositiveIntegerField(null=True, blank=True)
    school = models.CharField(max_length=128, blank=True, help_text='School')
    remarks = models.CharField(max_length=128, blank=True)

    class Meta:
        ordering = ('degree',)
        unique_together = ('ini', 'degree')

        # def get_query_set(self):
        #     return super(UserProfileManager, self).get_query_set().select_related(
        #         'user', 'organization'
        #     )

    def employee_count(self):
        return User.objects.filter(attainment__undergrad__degree=self.degree).count()

    def __str__(self):
        return self.degree


class Masteral(BaseProfile):
    ini = models.CharField(max_length=32, default='None', help_text='e.g MSIT, MBA, MIS etc')
    degree = models.CharField(max_length=128, default='None', help_text='Enter Masters title here')
    units = models.PositiveIntegerField(null=True, blank=True)
    year_graduated = models.PositiveIntegerField(null=True, blank=True)
    school = models.CharField(max_length=128, blank=True, help_text='School')
    remarks = models.CharField(max_length=128, blank=True)

    class Meta:
        ordering = ('degree',)
        unique_together = ('ini', 'degree')

    def employee_count(self):
        return User.objects.filter(attainment__masteral__degree=self.degree).count()

    def __str__(self):
        return self.degree


class Doctoral(BaseProfile):
    degree = models.CharField(max_length=128, default='None', unique=True, help_text='Enter PhD title here')
    units = models.PositiveIntegerField(null=True, blank=True)
    year_graduated = models.PositiveIntegerField(null=True, blank=True)
    school = models.CharField(max_length=128, blank=True, help_text='School')
    remarks = models.CharField(max_length=128, blank=True)

    class Meta:
        ordering = ('degree',)

    def employee_count(self):
        return User.objects.filter(attainment__doctoral__degree=self.degree).count()

    def __str__(self):
        return self.degree


class Attainment(BaseProfile):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    undergrad = models.ForeignKey(Undergrad,  null=True, blank=True, verbose_name="Undergrad Degrees", help_text='Choose only 1 if (multi course)')
    masteral = models.ForeignKey(Masteral, null=True, blank=True, verbose_name="Masteral Degrees")
    doctorate = models.ForeignKey(Doctoral, null=True, blank=True, verbose_name="Doctoral Degrees")

    class Meta:
        ordering = ('undergrad',)

    def __str__(self):
        return self.get_highest_attainment()

    def get_highest_attainment(self):
        # import pdb; pdb.set_trace()
        if self.doctorate:
            return self.doctorate.degree
        if self.masteral:
            return self.masteral.degree
        if self.undergrad:
            return self.undergrad.degree
        return 'None'
