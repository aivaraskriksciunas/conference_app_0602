from .views import (
    ConferenceListView,
    ConferenceDetailView, CreateCommentView, CreateConferenceView
)
from django.urls import path

urlpatterns = [
    # Visi views kurie yra ne funkcijos, o klases,
    # juos kvieciam su papildoma as_view()
    path( "", ConferenceListView.as_view() ), # /conferences/
    path( "<int:pk>/", ConferenceDetailView.as_view(), name = "conference-detail" ), # /conferences/1/, /conferences/10/
    path( "<int:konferencijos_id>/comments/", CreateCommentView.as_view(), name='create-comment' ),
    path( "new/", CreateConferenceView.as_view(), name = 'create-conference' ),
]