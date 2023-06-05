from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from events.models import Event

class EventDetailView( DetailView ):
    model = Event
    context_object_name = "renginys"

# View, kurį pasiekus prie lankytojų skaičiaus bus pridėtas 1
def register_visitor( request, renginio_id ):
    event = get_object_or_404( Event, id = renginio_id )
    event.visitors += 1
    event.save() # UPDATE events SET visitors = 2 WHERE id = 1

    return HttpResponse( event.title )