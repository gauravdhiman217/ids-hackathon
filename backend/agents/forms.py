# forms.py
from django import forms
from datetime import date
from .models import Roster

class WeekPickerWidget(forms.TextInput):
    input_type = 'week'

class RosterForm(forms.ModelForm):
    # HTML `input type="week"` returns values like "2025-W47".
    # Use a CharField here so we can parse that format into a `date`.
    week_start = forms.CharField(widget=WeekPickerWidget())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only set the week picker initial when the form is NOT bound (i.e. GET).
        if not self.is_bound:
            # Prefer explicit initial provided by caller
            initial_ws = None
            if 'initial' in kwargs and kwargs['initial'] and kwargs['initial'].get('week_start'):
                initial_ws = kwargs['initial'].get('week_start')
            elif getattr(self, 'instance', None) and getattr(self.instance, 'week_start', None):
                dt = self.instance.week_start
                y, w, _ = dt.isocalendar()
                initial_ws = f"{y}-W{w:02d}"

            if initial_ws:
                self.initial['week_start'] = initial_ws

    class Meta:
        model = Roster
        fields = '__all__'
        widgets = {}

    def clean(self):
        cleaned = super().clean()

        day_fields = [
            ("mon_start", "mon_end", "mon_status"),
            ("tue_start", "tue_end", "tue_status"),
            ("wed_start", "wed_end", "wed_status"),
            ("thu_start", "thu_end", "thu_status"),
            ("fri_start", "fri_end", "fri_status"),
            ("sat_start", "sat_end", "sat_status"),
            ("sun_start", "sun_end", "sun_status"),
        ]

        for start_f, end_f, stat_f in day_fields:
            s = cleaned.get(start_f)
            e = cleaned.get(end_f)
            st = cleaned.get(stat_f)

            # if LEAVE or OFF, start/end MUST BE blank
            if st in ["LEAVE", "OFF"]:
                cleaned[start_f] = None
                cleaned[end_f] = None

            # if ON but start/end provided
            if st == "ON" and s and e:
                if s >= e:
                    self.add_error(end_f, "End time must be after start time.")

            # if start/end given but status not ON
            if st != "ON" and (s or e):
                self.add_error(stat_f, "Clear times or set status = ON.")

        return cleaned

    def clean_week_start(self):
        val = self.cleaned_data.get('week_start')
        if isinstance(val, date):
            return val
        if not val:
            return val

        # Parse YYYY-W## → Monday date
        try:
            if "-W" in val:
                y, w = val.split("-W")
                return date.fromisocalendar(int(y), int(w), 1)
            return date.fromisoformat(val)
        except:
            raise forms.ValidationError("Invalid week format (YYYY-W##)")
