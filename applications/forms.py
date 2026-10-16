from django import forms

from .models import Application, ApplicationFile, ApplicationStatus


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            "document_type",
            "college",
            "full_name",
            "symbol_no",
            "reg_no",
            "program",
            "passed_year",
            "copies",
            "phone",
            "delivery_province",
            "delivery_district",
            "delivery_municipality",
            "delivery_ward",
            "delivery_street",
            "delivery_notes",
        ]
        widgets = {
            "delivery_notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        input_cls = (
            "w-full rounded-lg border border-gray-300 px-3 py-2 "
            "focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
        )
        for name, field in self.fields.items():
            if not isinstance(field.widget, (forms.CheckboxInput, forms.SelectMultiple)):
                field.widget.attrs.setdefault("class", input_cls)
        self.fields["college"].required = False
        self.fields["college"].empty_label = "— Select college (optional) —"
        self.fields["passed_year"].required = False
        self.fields["delivery_ward"].required = False
        self.fields["delivery_street"].required = False
        self.fields["delivery_notes"].required = False


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", forms.ClearableFileInput(attrs={"allow_multiple_selected": True}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single = super().clean(data, initial)
        if isinstance(single, (list, tuple)):
            return single
        return data


class ApplicationFileForm(forms.Form):
    file_type = forms.ChoiceField(
        choices=[
            ("CITIZENSHIP", "Citizenship"),
            ("MARKSHEET", "Mark sheet"),
            ("PHOTO", "Photo"),
            ("REG_CARD", "Registration card"),
            ("VOUCHER", "Payment voucher"),
            ("OTHER", "Other"),
        ],
        widget=forms.Select(
            attrs={
                "class": "w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
            }
        ),
    )
    files = MultipleFileField(
        widget=forms.ClearableFileInput(
            attrs={
                "class": "w-full text-sm text-gray-600 file:mr-4 file:rounded-lg file:border-0 file:bg-blue-50 file:px-4 file:py-2 file:text-blue-700 hover:file:bg-blue-100"
            }
        ),
        required=False,
        help_text="Attach one or more files for this type (optional).",
    )


class StatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["status", "admin_remark", "tracking_no"]
        widgets = {"admin_remark": forms.Textarea(attrs={"rows": 3})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        input_cls = (
            "w-full rounded-lg border border-gray-300 px-3 py-2 "
            "focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
        )
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", input_cls)
        # Disallow going back to DRAFT via status updates
        self.fields["status"].choices = [
            c for c in ApplicationStatus.choices if c[0] != ApplicationStatus.DRAFT
        ]
