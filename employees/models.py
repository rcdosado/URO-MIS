import datetime


from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

#from education.models import Attainment, Undergrad, Masteral, Doctoral
from mis.base import BaseProfile


class AreaOfDiscipline(BaseProfile):
    name = models.CharField(max_length=64, help_text='e.g allied medicine, engineering, science etc.')
    remarks = models.CharField(max_length=64, blank=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Expertise(BaseProfile):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    area_of_discipline = models.ForeignKey(AreaOfDiscipline, related_name='area', null=True, blank=True)
    expertise = models.CharField(max_length=255, help_text='Separate expertise with comma..')

    class Meta:
        verbose_name_plural = 'Expertise'

    def __str__(self):
        return self.expertise


class Campus(BaseProfile):
    name = models.CharField(max_length=50, blank=True, verbose_name="Name of Campus")
    head = models.ForeignKey(User, null=True, blank=True, related_name='director', verbose_name="Campus Director")
    address = models.CharField(max_length=256, blank=True, verbose_name="Location of Campus")
    contact_no = models.CharField(max_length=30, blank=True, help_text="Follow this format e.g 02-433-0262")
    info = models.TextField(max_length=256, blank=True, help_text="Describe what information about the Campus")

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Campuses'

    def __str__(self):
        return self.name

class Unit(BaseProfile):
    DIVISION_CHOICES = (
        ('0', 'Unknown'),
        ('1', 'Academic Affairs'),
        ('2', 'Research & Extension'),
        ('3', 'Administration'),
    )
    name = models.CharField(max_length=30, verbose_name="Name of Unit", unique=True)
    campus = models.ForeignKey(Campus, null=True, blank=True, related_name='campus', verbose_name="Campus")
    division = models.CharField(max_length=1, choices=DIVISION_CHOICES, help_text="Choose Division", default=0)
    head = models.ForeignKey(User, null=True, blank=True, related_name='unithead', verbose_name="Head of Unit")
    contact_no = models.CharField(max_length=30, blank=True, help_text="Follow this format e.g 02-433-0262")
    info = models.TextField(max_length=256, blank=True, help_text="Describe what is about this Designation")

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Department(BaseProfile):
    title = models.CharField(max_length=50, help_text="Add a Designation")
    head = models.ForeignKey(User, null=True, blank=True, related_name='departmenthead',
                             verbose_name="Chairman/Head of the Department")
    unit = models.ForeignKey(Unit, related_name='unit',
                             help_text="Choose which Unit/Collegee this Department belongs to")
    contact_no = models.CharField(max_length=30, blank=True, help_text="Follow this format e.g 02-433-0262")
    info = models.TextField(max_length=256, blank=True, help_text="Describe what is about this Department")

    def __str__(self):
        return self.title

class Rank(BaseProfile):
    name = models.CharField(max_length=50, help_text="Add new rank here")
    info = models.TextField(max_length=256, blank=True, help_text="Information about this Rank")

    def __str__(self):
        return self.name


class Employee(BaseProfile):
    STATUS_CHOICES = (
        ('0', 'Unknown'),
        ('1', 'JO'),
        ('2', 'Regular'),
        ('3', 'COS'),
		)
    SCHOOL_CHOICES = (
        ('0', 'Unknown'),
        ('1', 'PSU'),
		)
    GENDER_CHOICES = (
        ('0', 'unknown'),
        ('1', 'male'),
        ('2', 'female'),
		)
    CIVIL_STATUS_CHOICES = (
        ('0', 'unknown'),
        ('1', 'single'),
        ('2', 'married'),
        ('3', 'widowed/widower')
	)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    employee_no = models.PositiveIntegerField(unique=True, null=True, blank=True, help_text="Your Employee Number")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=0)
    civil_status = models.CharField(max_length=1, choices=CIVIL_STATUS_CHOICES, default=0)
    address = models.TextField(max_length=256, blank=True)
    birth_date = models.DateField(auto_now=False, null=True, blank=True, auto_now_add=False, default=datetime.date.today)
    institution = models.CharField(max_length=1, choices=SCHOOL_CHOICES, help_text="Choose/Add Institution you belong to", default=1)
    work_status = models.CharField(max_length=1, choices=STATUS_CHOICES, help_text="Status of Appointment", default=0)
    designation = models.CharField(max_length=255, blank=True, help_text="e.g Chairman, Director, etc")
    department = models.ForeignKey(Department, null=True, blank=True, help_text="For Faculty Only")
    rank = models.ForeignKey(Rank, null=True, blank=True, help_text="Choose Staff/Faculty Rank")
    unit = models.ForeignKey(Unit, null=True, blank=True, help_text="Choose the Unit user is currently working")
    started = models.DateField(null=True, auto_now_add=True, help_text="Started working in the Institution")
    expertise = models.ForeignKey(Expertise, null=True, blank=True)
    #education = models.ForeignKey(Attainment, null=True, blank=True, help_text="Add your educational Attainment here")
    mobile_no = models.CharField(max_length=30, blank=True,help_text="Follow this format e.g +639399581237")
    landline_no = models.CharField(max_length=30, blank=True, help_text="Follow this format e.g 02-433-0262")
	
    def __str__(self):
        return self.get_display_name()
		
    def age(self):
        if not self.birth_date:
            return None
        today = datetime.date.today()
        delta = ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return today.year - self.birth_date.year - delta	

    def get_display_name(self):
        if self.user.first_name and self.user.last_name:  # and self.show_real_name:
            if self.unit:
                display_name = "%s %s/%s" % (
                    self.user.first_name,
                    self.user.last_name,
                    self.unit
                )
            else:
                display_name = "%s %s" % (
                    self.user.first_name,
                    self.user.last_name,
                )
            return display_name
        else:
            return self.user.username

    def get_years_in_service(self):
        pass
        #result = delta.relativedelta(datetime.datetime.now(), self.started)
        # "{0.years} years and {0.months} months".format(result)
        #return result.years

    def get_highest_attainment(self):
        return self.education.get_highest_attainment()


@receiver(post_save, sender=User)
def create_or_update_employee_profile(sender, instance, created, **kwargs):
    if created:
        Employee.objects.create(user=instance)
    instance.employee.save()
