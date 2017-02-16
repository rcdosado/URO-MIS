from django.db import models
from django.utils import timezone
from employees.models import Employee

import datetime

from mis.base import BaseProfile


class Organizer(BaseProfile):
    name = models.CharField(max_length=255, verbose_name="Name of Organizer", unique=True)
    email = models.EmailField(blank=True, null=True, verbose_name="Email Address")
    url = models.URLField(blank=True, null=True, verbose_name="Website Address")

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


# generic event model
class Events(BaseProfile):
    LEVEL_CHOICES = (
        ('0', 'unknown'),
        ('1', 'institutional'),
        ('2', 'local'),
        ('3', 'national'),
        ('4', 'international'),
    )
    # http://www.evenues.com/event-planning-guide/types-of-meetings-and-events
    EVENT_TYPES = (
        ('0', 'Unknown'),
        ('1', 'Conference'),
        ('2', 'Meeting'),
        ('3', 'Banquet'),
        ('4', 'Seminar'),
        ('5', 'Conclave'),
        ('6', 'Workshop'),
        ('7', 'Convention'),
        ('8', 'Symposium'),
    )
    title = models.CharField(max_length=256,help_text="Enter the Event/Conference/Symposium name here")
    type = models.CharField(max_length=1, choices=EVENT_TYPES, default=0, help_text="What Type of Event is this?")
    venue = models.CharField(max_length=256, blank=True, help_text="Where did this happen (City,Province, Place)")
    start_date = models.DateField(default=timezone.now, verbose_name="Date Started")
    end_date = models.DateField(default=timezone.localtime(timezone.now()) + datetime.timedelta(days=2),
                                verbose_name="Date Ended")
    level = models.CharField(max_length=1, choices=LEVEL_CHOICES, default=0)
    organizers = models.ManyToManyField(Organizer, verbose_name="List of Organizers")

    class Meta:
        ordering = ('title',)
        unique_together = ('title', 'venue')
        abstract = True

    # method to return the number of duration of the event
    # manager to return all local, national, international

    def __str__(self):
        return self.title


class Presentation(Events):
    RESEARCH_TYPES = (
        ('0', 'unknown'),
        ('1', 'study'),
        ('2', 'project'),
    )

    PRESENTATION_TYPES = (
        ('0', 'unknown'),
        ('1', 'oral'),
        ('2', 'poster'),
    )

    research_title = models.CharField(max_length=256, help_text="Enter the Research Title")
    authors = models.ManyToManyField(Employee, blank=True, verbose_name="List of authors")
    presentor = models.ForeignKey(Employee, blank=True, related_name="presentor", verbose_name="Presented by", null=True)
    research_type = models.CharField(max_length=1,  verbose_name="Type of Research", choices=RESEARCH_TYPES, default=0)
    presentation_type = models.CharField(max_length=1, verbose_name="Type of Presentation", choices=PRESENTATION_TYPES,
                                         default=0)
    other_info = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('research_title',)
        verbose_name_plural = 'Research Presentations'

    def get_authors(self):
        ret = ",".join([str(author) for author in self.authors.all()])
        return ret


#class Conference(Events):
#    pass
