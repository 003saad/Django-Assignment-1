from datetime import date as dt_date
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from .models import Category, Event, Participant
from .forms import CategoryForm, EventForm, ParticipantForm


# -------------------------
# Dashboard (Module 8)
# -------------------------
def dashboard(request):
    today = dt_date.today()

    total_events = Event.objects.count()
    total_participants_unique = Participant.objects.count()

    upcoming_count = Event.objects.filter(date__gte=today).count()
    past_count = Event.objects.filter(date__lt=today).count()

    # total participant "registrations" across all events (can count duplicates if same participant joins multiple events)
    total_participant_registrations = Event.participants.through.objects.count()

    # section below stats grid changes by query param
    mode = request.GET.get("mode", "today")  # today | all | upcoming | past

    qs = (
        Event.objects.select_related("category")
        .prefetch_related("participants")
        .annotate(participant_count=Count("participants", distinct=True))
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


# -------------------------
# Event CRUD + Search + Filters + Optimized Queries
# -------------------------
def event_list(request):
    events = (
        Event.objects.select_related("category")
        .prefetch_related("participants")
        .annotate(participant_count=Count("participants", distinct=True))
        .order_by("date", "time")
    )

    categories = Category.objects.all().order_by("name")

    # Search by name or location (icontains)
    search = request.GET.get("search")
    if search:
        events = events.filter(
            Q(name__icontains=search) | Q(location__icontains=search)
        )

    # Filter by category
    category_id = request.GET.get("category")
    if category_id:
        events = events.filter(category_id=category_id)

    # Filter by date range
    start = request.GET.get("start")
    end = request.GET.get("end")
    if start and end:
        events = events.filter(date__range=[start, end])

    context = {
        "events": events,
        "categories": categories,
        "search": search or "",
        "category_id": category_id or "",
        "start": start or "",
        "end": end or "",
    }
    return render(request, "events/event_list.html", context)


def event_detail(request, pk):
    event = get_object_or_404(
        Event.objects.select_related("category").prefetch_related("participants"), pk=pk
    )
    return render(request, "events/event_detail.html", {"event": event})


def event_create(request):
    form = EventForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("event_list")
    return render(
        request, "events/event_form.html", {"form": form, "title": "Create Event"}
    )


def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    form = EventForm(request.POST or None, instance=event)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("event_detail", pk=pk)
    return render(
        request, "events/event_form.html", {"form": form, "title": "Update Event"}
    )


def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        event.delete()
        return redirect("event_list")
    return render(request, "events/event_confirm_delete.html", {"event": event})


# -------------------------
# Category CRUD
# -------------------------
def category_list(request):
    categories = Category.objects.all().order_by("name")
    return render(request, "events/category_list.html", {"categories": categories})


def category_create(request):
    form = CategoryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("category_list")
    return render(
        request, "events/category_form.html", {"form": form, "title": "Create Category"}
    )


def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, instance=category)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("category_list")
    return render(
        request, "events/category_form.html", {"form": form, "title": "Update Category"}
    )


def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.delete()
        return redirect("category_list")
    return render(
        request, "events/category_confirm_delete.html", {"category": category}
    )


# -------------------------
# Participant CRUD
# -------------------------
def participant_list(request):
    participants = Participant.objects.all().order_by("name")
    return render(
        request, "events/participant_list.html", {"participants": participants}
    )


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


def participant_delete(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == "POST":
        participant.delete()
        return redirect("participant_list")
    return render(
        request, "events/participant_confirm_delete.html", {"participant": participant}
    )
