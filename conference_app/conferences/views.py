from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from .models import Conference, Comment
from datetime import datetime

# 	Sukurkite ListView, kuris atvaizduotų visas konferencijas
class ConferenceListView( ListView ):
    model = Conference

# Alternatyva ListView klasei:
# def conference_list( request ):
#     conferences = Conference.objects.all()
#     return render( request, "conferences/conference_list.html", { "object_list": conferences })

class ConferenceDetailView( DetailView ):
    model = Conference


# Alternatyva DetailView
# def conference_detail( request, pk ): # pk ateina iš urls failo: path( "<int:pk>/", ... )
#     conference = get_object_or_404( Conference, pk = pk )
#     return render( request, "conferences/conference_detail.html", { "object": conference } )

class CreateCommentView( View, LoginRequiredMixin ):
    # konferencijos_id -> turi sutapti su pavadinimu urls.py faile!
    def get( self, request ):
        return render( ... )

    def post( self, request, konferencijos_id ):
        # 0. išsirašyti visas reikšmes
        komentaro_tekstas = request.POST.get( 'komentaras' )
        # 1. Validacija
        if len( komentaro_tekstas ) == 0:
            messages.error( request, "Komentaras negali būti tuščias!" )
            return redirect( f"/conferences/{konferencijos_id}" )
        # tikrinam ar vartotojas prisijungęs
        # Tikrinimo nereikia jei naudojam LoginRequiredMixin
        # if request.user.is_authenticated == False:
        #     return HttpResponse( "Klaida! Jums reikia prisijungti" )

        # Vienu metu patikriname, ar yra konferencija su konferencijos_id, ir
        # taip pat išsaugome Conference objektą su tuo konferencijos_id
        konferencija = get_object_or_404( Conference, id=konferencijos_id )

        # 2. Veiksmas - įrašyti komentarą į duomenų bazę
        komentaras = Comment()
        komentaras.author = request.user
        komentaras.conference = konferencija
        komentaras.comment = komentaro_tekstas
        # Sukurtą modelį įrašom į DB. Be šitos eilutės jis liks tik kompiuterio atmintyje, bet nebus išsaugotas
        komentaras.save()
        # 3. Rezultatas vartotojui
        return redirect( f"/conferences/{konferencijos_id}" )


class CreateConferenceView( View ):
    def get( self, request ):
        return render(
            request,
            "conferences/conference_create.html"
        )

    def post( self, request ):
        # 0. Išsikelti duomenis
        start_date = request.POST.get( 'start_date' )
        end_date = request.POST.get( 'end_date' )
        title = request.POST.get( 'title' )

        # 1. Validacija
        if len( title ) == 0:
            messages.error( request, "Būtina įvesti pavadinimą" )
            return redirect( "/conferences/new" )

        try:
            # from datetime import datetime
            start_date = datetime.strptime( start_date, "%Y-%m-%d" )
            end_date = datetime.strptime( end_date, "%Y-%m-%d" )
        except ValueError:
            messages.error( request, "Blogai įvestos datos!" )
            return redirect( "/conferences/new" )

        # 2. Veiksmas - sukuriame įrašą
        conference = Conference()
        conference.start_date = start_date
        conference.end_date = end_date
        conference.title = title
        conference.save()

        # 3. Rezultatas
        return redirect( f"/conferences/{conference.id}/" )