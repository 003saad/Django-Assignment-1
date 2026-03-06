from django.urls import path
from . import views

urlpatterns = [
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("organizer-dashboard/", views.organizer_dashboard, name="organizer_dashboard"),
    path(
        "participant-dashboard/",
        views.participant_dashboard,
        name="participant_dashboard",
    ),
    path("", views.dashboard, name="dashboard"),
    path("dashboard-redirect/", views.dashboard_redirect, name="dashboard_redirect"),
    path("events/", views.event_list, name="event_list"),
    path("events/<int:pk>/", views.event_detail, name="event_detail"),
    path("events/<int:pk>/rsvp/", views.rsvp_event, name="rsvp_event"),
    path("events/create/", views.event_create, name="event_create"),
    path("events/<int:pk>/update/", views.event_update, name="event_update"),
    path("events/<int:pk>/delete/", views.event_delete, name="event_delete"),
    path("categories/", views.category_list, name="category_list"),
    path("categories/create/", views.category_create, name="category_create"),
    path("categories/<int:pk>/update/", views.category_update, name="category_update"),
    path("categories/<int:pk>/delete/", views.category_delete, name="category_delete"),
    path("participants/", views.participant_list, name="participant_list"),
    path("participants/create/", views.participant_create, name="participant_create"),
    path(
        "participants/<int:pk>/update/",
        views.participant_update,
        name="participant_update",
    ),
    path(
        "participants/<int:pk>/delete/",
        views.participant_delete,
        name="participant_delete",
    ),
]
