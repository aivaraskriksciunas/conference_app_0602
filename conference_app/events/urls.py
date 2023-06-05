from django.urls import path
from events.views import EventDetailView

urlpatterns = [
    # /events/2/
    path( '<int:pk>/', EventDetailView.as_view() )
]