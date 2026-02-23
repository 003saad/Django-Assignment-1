from django import forms
from .models import Event, Participant, Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description"]

        base = "w-full bg-[#0f1116] border border-white/10 rounded px-3 py-2 text-gray-100 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-red-400/40"

        widgets = {
            "name": forms.TextInput(attrs={"class": base}),
            "description": forms.Textarea(attrs={"class": base, "rows": 4}),
        }


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ["name", "email"]

        base = "w-full bg-[#0f1116] border border-white/10 rounded px-3 py-2 text-gray-100 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-red-400/40"

        widgets = {
            "name": forms.TextInput(attrs={"class": base}),
            "email": forms.EmailInput(attrs={"class": base}),
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "name",
            "description",
            "date",
            "time",
            "location",
            "category",
            "participants",
        ]
        base = "w-full bg-[#0f1116] border border-white/10 rounded px-3 py-2 text-gray-100 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-red-400/40"

        widgets = {
            "name": forms.TextInput(attrs={"class": base}),
            "description": forms.Textarea(attrs={"class": base, "rows": 4}),
            "date": forms.DateInput(attrs={"type": "date", "class": base}),
            "time": forms.TimeInput(attrs={"type": "time", "class": base}),
            "location": forms.TextInput(attrs={"class": base}),
            "category": forms.Select(attrs={"class": base}),
            "participants": forms.SelectMultiple(attrs={"class": base, "size": 10}),
        }

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()
        if len(name) < 3:
            raise forms.ValidationError("Event name must be at least 3 characters.")
        return name
