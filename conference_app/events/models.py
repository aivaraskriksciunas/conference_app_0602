from django.contrib.auth.models import User
from django.db import models
from conferences.models import Conference

# Create your models here.
class Event( models.Model ):
    date = models.DateTimeField( null = True )
    title = models.CharField( max_length = 100 )
    # TODO: Ištrinti ateityje
    visitors = models.IntegerField( default = 0 )

    conference = models.ForeignKey( Conference, on_delete = models.CASCADE )

    created_at = models.DateTimeField( auto_now_add = True )
    updated_at = models.DateTimeField( auto_now = True )

    def __str__(self):
        return self.title

class EventRegistration( models.Model ):
    event = models.ForeignKey(
        Event,
        on_delete = models.CASCADE,
    )
    user = models.ForeignKey( User, on_delete = models.CASCADE )

    created_at = models.DateTimeField( auto_now_add = True )

class CompanyRegistration( models.Model ):
    company_name = models.CharField( max_length=100 )
    people_count = models.IntegerField()
    remarks = models.TextField()
    event = models.ForeignKey( Event, on_delete = models.CASCADE )

    created_at = models.DateTimeField( auto_now_add = True )