from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import DetailView
from events.models import Event, EventRegistration, CompanyRegistration


class EventDetailView( DetailView ):
    model = Event
    context_object_name = "renginys"

    def post( self, request, pk ):
        # Apdoroti requestą
        # 0. Išsitraukti duomenis į kintamuosius
        # (nebūtina bet gera praktika)
        company_name = request.POST.get( 'imones_pavadinimas' )
        zmoniu_skaicius = request.POST.get( 'zmoniu_skaicius' )
        pastaba = request.POST.get( 'pastabos' )
        # 1. Patikrinti vartotojo įvestus duomenis
        if not zmoniu_skaicius.isnumeric():
            messages.error( request, "Žmonių skaičius turi būti skaitinė vertė :(" )
            return redirect( f"/events/{pk}")
        if len( company_name ) == 0:
            messages.error( request, "Įmonės pavadinimas turi būti užpildytas" )
            return redirect( f"/events/{pk}")
        # 1a. Patikrinti ar pk egzistuoja (ar yra Event su tuo pk)
        renginys = get_object_or_404( Event, pk = pk )
        # 2. Veiksmas: įrašymas į duomenų bazę (kursime naują registraciją)
        registration = CompanyRegistration()
        registration.company_name = company_name
        registration.people_count = zmoniu_skaicius
        registration.remarks = pastaba
        registration.event = renginys
        registration.save()
        # 3. Rezultatas: HTML arba redirect
        return redirect( f"/events/{pk}")

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