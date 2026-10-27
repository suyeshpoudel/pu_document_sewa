from django import forms

from config.pricing import MINIMUM_SERVICE_FEE_RS

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
            "urgency",
        ]
        widgets = {
            "delivery_notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if not isinstance(field.widget, (forms.CheckboxInput, forms.SelectMultiple, forms.FileInput)):
                field.widget.attrs.setdefault("class", "input")
        self.fields["full_name"].label = "Full name"
        self.fields["phone"].label = "Phone number"
        self.fields["full_name"].widget.attrs.setdefault("placeholder", "As shown on your PU documents")
        self.fields["phone"].widget.attrs.setdefault("placeholder", "98XXXXXXXX")
        self.fields["pu_reference_no"].widget.attrs.setdefault("placeholder", "e.g. PU-APP-123456")
        self.fields["delivery_municipality"].widget.attrs.setdefault("placeholder", "Municipality / city")
        self.fields["delivery_street"].widget.attrs.setdefault("placeholder", "Street, landmark, or house no. (optional)")
        self.fields["delivery_notes"].widget.attrs.setdefault("placeholder", "Delivery instructions or landmarks (optional)")
        self.fields["college"].required = False
        self.fields["college"].empty_label = "— Select college (optional) —"
        self.fields["delivery_ward"].required = False
        self.fields["delivery_street"].required = False
        self.fields["delivery_notes"].required = False
        self.fields["urgency"].label = "Delivery urgency"
        self.fields["urgency"].help_text = (
            "Choose Urgent if you need the document handled as quickly as possible. "
            f"The minimum delivery fee is Rs. {MINIMUM_SERVICE_FEE_RS}; your final fee "
            "is confirmed after receipt verification."
        )
        self.fields["urgency"].widget.attrs.update({"class": "input"})
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
            {"class": "input", "accept": "image/*,.pdf"}
        )


class StatusUpdateForm(forms.ModelForm):
    courier = forms.ChoiceField(
        label="Courier",
        choices=Courier.choices,
        required=False,
        initial=Courier.NEPAL_CAN_MOVE,
        widget=forms.Select(attrs={"class": "input"}),
    )
    courier_name = forms.CharField(
        label="Courier name (if Other)",
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "input", "placeholder": "Courier name (when Other)"},
        ),
    )
    tracking_id = forms.CharField(
        label="Tracking ID",
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "input", "placeholder": "e.g. NCM tracking ID"},
        ),
        help_text="Required when status is set to Dispatched.",
    )

    class Meta:
        model = Application
        fields = ["status", "service_fee_rs", "admin_remark"]
        widgets = {"admin_remark": forms.Textarea(attrs={"rows": 3})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, forms.Select):
                field.widget.attrs.setdefault("class", "input")
        self.fields["status"].widget.attrs.setdefault("class", "input")
        self.fields["status"].label = "Application status"
        self.fields["service_fee_rs"].label = "Final service fee (Rs.)"
        self.fields["service_fee_rs"].help_text = (
            f"Minimum Rs. {MINIMUM_SERVICE_FEE_RS}. Set the final fee based on the "
            "document, delivery location, and the student's urgency. This amount is "
            "collected cash on delivery."
        )
        self.fields["service_fee_rs"].widget.attrs.update(
            {"class": "input", "min": MINIMUM_SERVICE_FEE_RS, "step": 50}
        )
        self.fields["admin_remark"].label = "Note to student"
        self.fields["admin_remark"].help_text = (
            "Visible on the student's application page. Use it to explain a rejection or share updates."
        )

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
