from django.urls import path
from events.views import (
    EventDetailView,
    register_visitor
)

urlpatterns = [
    # /events/2/
    path( '<int:pk>/', EventDetailView.as_view(), name = "event-detail" ),
    path( 'register/<int:renginio_id>/', register_visitor, name = "register-visitor" ),
]