from datetime import date as dt_date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from accounts.role_decorators import role_required
from .forms import CategoryForm, EventForm, ParticipantForm
from .models import Category, Event, Participant


# Role-based redirect
@login_required
def dashboard_redirect(request):
    user = request.user

    if user.is_superuser or user.groups.filter(name="Admin").exists():
        return redirect("admin_dashboard")

    if user.groups.filter(name="Organizer").exists():
        return redirect("organizer_dashboard")

    if user.groups.filter(name="Participant").exists():
        return redirect("participant_dashboard")

    return redirect("dashboard")


# Main dashboard
@login_required
def dashboard(request):
    today = dt_date.today()

    total_events = Event.objects.count()
    total_participants_unique = (
        User.objects.filter(groups__name="Participant").distinct().count()
    )
    upcoming_count = Event.objects.filter(date__gte=today).count()
    past_count = Event.objects.filter(date__lt=today).count()
    total_participant_registrations = Event.rsvps.through.objects.count()

    mode = request.GET.get("mode", "today")

    qs = (
        Event.objects.select_related("category")
        .prefetch_related("participants", "rsvps")
        .annotate(participant_count=Count("rsvps", distinct=True))
        .order_by("date", "time")
    )

    if mode == "all":
        events_section = qs
        section_title = "All Events"
    elif mode == "upcoming":
        events_section = qs.filter(date__gte=today)
        section_title = "Upcoming Events"
    elif mode == "past":
        events_section = qs.filter(date__lt=today)
        section_title = "Past Events"
    else:
        events_section = qs.filter(date=today)
        section_title = "Today's Events"

    context = {
        "total_events": total_events,
        "total_participants_unique": total_participants_unique,
        "total_participant_registrations": total_participant_registrations,
        "upcoming_count": upcoming_count,
        "past_count": past_count,
        "section_title": section_title,
        "mode": mode,
        "events_section": events_section,
    }
    return render(request, "events/dashboard.html", context)


# Role dashboards
@login_required
@role_required("Admin")
def admin_dashboard(request):
    total_events = Event.objects.count()
    total_categories = Category.objects.count()
    total_users = User.objects.count()

    context = {
        "total_events": total_events,
        "total_categories": total_categories,
        "total_users": total_users,
    }
    return render(request, "events/admin_dashboard.html", context)


@login_required
@role_required("Organizer", "Admin")
def organizer_dashboard(request):
    total_events = Event.objects.count()
    total_categories = Category.objects.count()

    context = {
        "total_events": total_events,
        "total_categories": total_categories,
    }
    return render(request, "events/organizer_dashboard.html", context)


@login_required
@role_required("Participant", "Organizer", "Admin")
def participant_dashboard(request):
    events = (
        request.user.rsvp_events.select_related("category")
        .all()
        .order_by("date", "time")
    )

    context = {
        "events": events,
    }
    return render(request, "events/participant_dashboard.html", context)


# Event views
@login_required
def event_list(request):
    events = (
        Event.objects.select_related("category")
        .prefetch_related("participants", "rsvps")
        .annotate(participant_count=Count("rsvps", distinct=True))
        .order_by("date", "time")
    )

    categories = Category.objects.all().order_by("name")

    search = request.GET.get("search")
    if search:
        events = events.filter(
            Q(name__icontains=search) | Q(location__icontains=search)
        )

    category_id = request.GET.get("category")
    if category_id:
        events = events.filter(category_id=category_id)

    start = request.GET.get("start") or request.GET.get("start_date")
    end = request.GET.get("end") or request.GET.get("end_date")

    if start and end:
        events = events.filter(date__range=[start, end])

    context = {
        "events": events,
        "categories": categories,
        "search": search or "",
        "category_id": category_id or "",
        "start": start or "",
        "end": end or "",
        "start_date": start or "",
        "end_date": end or "",
    }
    return render(request, "events/event_list.html", context)


@login_required
def event_detail(request, pk):
    event = get_object_or_404(
        Event.objects.select_related("category").prefetch_related(
            "participants", "rsvps"
        ),
        pk=pk,
    )

    has_rsvped = event.rsvps.filter(id=request.user.id).exists()

    context = {
        "event": event,
        "has_rsvped": has_rsvped,
    }
    return render(request, "events/event_detail.html", context)


@login_required
@role_required("Participant", "Organizer", "Admin")
def rsvp_event(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.method == "POST":
        if event.rsvps.filter(id=request.user.id).exists():
            messages.warning(request, "You have already RSVP’d to this event.")
        else:
            event.rsvps.add(request.user)
            messages.success(request, "RSVP successful.")

    return redirect("event_detail", pk=pk)


@login_required
@role_required("Organizer", "Admin")
def event_create(request):
    form = EventForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("event_list")

    return render(
        request, "events/event_form.html", {"form": form, "title": "Create Event"}
    )


@login_required
@role_required("Organizer", "Admin")
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    form = EventForm(request.POST or None, instance=event)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("event_detail", pk=pk)

    return render(
        request, "events/event_form.html", {"form": form, "title": "Update Event"}
    )


@login_required
@role_required("Organizer", "Admin")
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.method == "POST":
        event.delete()
        return redirect("event_list")

    return render(request, "events/event_confirm_delete.html", {"event": event})


# Category views
@login_required
def category_list(request):
    categories = Category.objects.all().order_by("name")
    return render(request, "events/category_list.html", {"categories": categories})


@login_required
@role_required("Organizer", "Admin")
def category_create(request):
    form = CategoryForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("category_list")

    return render(
        request,
        "events/category_form.html",
        {"form": form, "title": "Create Category"},
    )


@login_required
@role_required("Organizer", "Admin")
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, instance=category)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("category_list")

    return render(
        request,
        "events/category_form.html",
        {"form": form, "title": "Update Category"},
    )


@login_required
@role_required("Admin")
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == "POST":
        category.delete()
        return redirect("category_list")

    return render(
        request,
        "events/category_confirm_delete.html",
        {"category": category},
    )


# Participant views
@login_required
@role_required("Admin")
def participant_list(request):
    participants = Participant.objects.all().order_by("name")
    return render(
        request, "events/participant_list.html", {"participants": participants}
    )


@login_required
@role_required("Admin")
def participant_create(request):
    form = ParticipantForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("participant_list")

    return render(
        request,
        "events/participant_form.html",
        {"form": form, "title": "Create Participant"},
    )


@login_required
@role_required("Admin")
def participant_update(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    form = ParticipantForm(request.POST or None, instance=participant)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("participant_list")

    return render(
        request,
        "events/participant_form.html",
        {"form": form, "title": "Update Participant"},
    )


@login_required
@role_required("Admin")
def participant_delete(request, pk):
    participant = get_object_or_404(Participant, pk=pk)

    if request.method == "POST":
        participant.delete()
        return redirect("participant_list")

    return render(
        request,
        "events/participant_confirm_delete.html",
        {"participant": participant},
    )
