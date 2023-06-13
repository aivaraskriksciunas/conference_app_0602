from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from .models import Conference, Comment


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
    def post( self, request, konferencijos_id ):
        # 0. išsirašyti visas reikšmes
        komentaro_tekstas = request.POST.get( 'komentaras' )
        # 1. Validacija
        if len( komentaro_tekstas ) == 0:
            return HttpResponse( "Klaida! negali būti tuščias" )
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
        komentaras.save()
        # 3. Rezultatas vartotojui
        return redirect( f"/conferences/{konferencijos_id}" )