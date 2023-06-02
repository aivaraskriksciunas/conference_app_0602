from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Conference


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