from django.shortcuts import render
from django.views.generic import DetailView
from events.models import Event

class EventDetailView( DetailView ):
    model = Event
    context_object_name = "renginys"