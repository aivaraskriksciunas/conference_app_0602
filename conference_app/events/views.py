from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import DetailView
from events.models import Event, EventRegistration

class EventDetailView( DetailView ):
    model = Event
    context_object_name = "renginys"

# View, kurį pasiekus prie lankytojų skaičiaus bus pridėtas 1
class RegisterVisitorView( LoginRequiredMixin, View ):
    def get( self, request, renginio_id ):
        event = get_object_or_404( Event, id=renginio_id )

        registraciju_kiekis = EventRegistration.objects.filter(
            event = event, user = request.user ).count()

        # SELECT COUNT(*) FROM event_registration WHERE
        # event_id = 1 AND user_id = 1;

        if registraciju_kiekis > 0:
            return HttpResponse( "Jūs jau prisiregistravote!" )

        registration = EventRegistration()
        registration.event = event
        registration.user  = request.user
        registration.save()

        return redirect( f"/events/{renginio_id}" )

# Atlernatyva, ka padaro LoginRequiredMixin:
#     if not request.user.is_authenticated:
#         return redirect( 'login' )

class UserEventList( View ):
    def get( self, request ):

        # Apsauga nuo neprisijungusių vartotojų
        if not request.user.is_authenticated:
            return redirect( 'login' )

        user_events = EventRegistration.objects.filter(
            user = request.user
        )

        return render(
            request,
            "events/user_events.html",
            { "object_list": user_events }
        )

# def user_event_list( request ):
#     pass