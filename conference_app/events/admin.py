from django.contrib import admin
from .models import Event, CompanyRegistration  # Tas pats kaip from events.models import Event
# Taip galim daryti nes esame tam paciam aplanke

class CompanyRegistrationAdmin( admin.ModelAdmin ):
    list_display = [ 'company_name', 'event_title', 'people_count' ]

    def event_title( self, model ):
        return f"Renginys: {model.event.title}"

# Register your models here.
admin.site.register( Event )
admin.site.register( CompanyRegistration, CompanyRegistrationAdmin )