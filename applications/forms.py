from django import forms

from .models import Application, ApplicationStatus, Courier, Shipment


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            "document_type",
            "college",
            "full_name",
            "phone",
            "pu_reference_no",
            "receipt",
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
            if not isinstance(field.widget, (forms.CheckboxInput, forms.SelectMultiple, forms.FileInput)):
                field.widget.attrs.setdefault("class", input_cls)
        self.fields["college"].required = False
        self.fields["college"].empty_label = "— Select college (optional) —"
        self.fields["delivery_ward"].required = False
        self.fields["delivery_street"].required = False
        self.fields["delivery_notes"].required = False
        self.fields["pu_reference_no"].label = "PU application reference no."
        self.fields["pu_reference_no"].help_text = (
            "Reference / application number shown on your services.pu.edu.np application, "
            "next to the pickup receipt."
        )
        self.fields["receipt"].label = "Pickup receipt"
        self.fields["receipt"].help_text = (
            "The pickup receipt generated on your PU application detail page after your "
            "college finishes processing. Upload it here (screenshot or PDF)."
        )
        self.fields["receipt"].widget.attrs.update(
            {
                "class": (
                    "w-full text-sm text-gray-600 file:mr-4 file:rounded-lg file:border-0 "
                    "file:bg-blue-50 file:px-4 file:py-2 file:text-blue-700 hover:file:bg-blue-100"
                ),
                "accept": "image/*,.pdf",
            }
        )


class StatusUpdateForm(forms.ModelForm):
    courier = forms.ChoiceField(
        choices=Courier.choices,
        required=False,
        initial=Courier.NEPAL_CAN_MOVE,
        widget=forms.Select(
            attrs={
                "class": "w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
            }
        ),
    )
    courier_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500",
                "placeholder": "Courier name (when Other)",
            }
        ),
    )
    tracking_id = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500",
                "placeholder": "e.g. NCM tracking ID",
            }
        ),
        help_text="Required when status is set to Dispatched.",
    )

    class Meta:
        model = Application
        fields = ["status", "admin_remark"]
        widgets = {"admin_remark": forms.Textarea(attrs={"rows": 3})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        input_cls = (
            "w-full rounded-lg border border-gray-300 px-3 py-2 "
            "focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
        )
        for field in self.fields.values():
            if not isinstance(field.widget, forms.Select):
                field.widget.attrs.setdefault("class", input_cls)
        self.fields["status"].widget.attrs.setdefault("class", input_cls)

        shipment = getattr(self.instance, "shipment", None)
        if shipment:
            self.fields["courier"].initial = shipment.courier
            self.fields["courier_name"].initial = shipment.courier_name
            self.fields["tracking_id"].initial = shipment.tracking_id

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("status") == ApplicationStatus.DISPATCHED and not cleaned.get("tracking_id"):
            raise forms.ValidationError(
                "Enter a tracking ID when marking an application as Dispatched."
            )
        return cleaned

    def shipment_data(self):
        return {
            "courier": self.cleaned_data.get("courier") or Courier.NEPAL_CAN_MOVE,
            "courier_name": self.cleaned_data.get("courier_name", ""),
            "tracking_id": self.cleaned_data.get("tracking_id", ""),
        }
