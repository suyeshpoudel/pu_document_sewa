from django import forms
from django.utils.text import slugify

from catalog.models import DocumentType
from colleges.models import College

INPUT_CLS = (
    "w-full rounded-lg border border-gray-300 px-3 py-2 "
    "focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
)


class OfficeDocumentForm(forms.ModelForm):
    required_docs_text = forms.CharField(
        label="Required documents",
        required=False,
        widget=forms.Textarea(attrs={"rows": 3, "class": INPUT_CLS}),
        help_text="One per line (e.g. CITIZENSHIP, MARKSHEET). Guidance only.",
    )
    includes = forms.ModelMultipleChoiceField(
        label="Bundle components",
        required=False,
        queryset=DocumentType.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        help_text=(
            "Tick the certificates included in this item to make it a bundle "
            "(e.g. TMP = Transcript + Migration + Provisional). Leave empty for a normal document."
        ),
    )

    class Meta:
        model = DocumentType
        fields = [
            "name",
            "slug",
            "fee_rs",
            "description",
            "processing_days",
            "is_active",
            "includes",
        ]
        widgets = {"description": forms.Textarea(attrs={"rows": 3})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxSelectMultiple):
                continue
            field.widget.attrs.setdefault("class", INPUT_CLS)
        self.fields["slug"].required = False
        self.fields["slug"].help_text = "Leave blank to auto-generate from the name."
        qs = DocumentType.objects.all()
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        self.fields["includes"].queryset = qs
        if self.instance.pk and self.instance.required_docs:
            self.fields["required_docs_text"].initial = "\n".join(
                self.instance.required_docs
            )

    def clean_slug(self):
        slug = self.cleaned_data.get("slug") or slugify(self.cleaned_data.get("name", ""))
        if not slug:
            raise forms.ValidationError("Could not generate a slug from the name.")
        qs = DocumentType.objects.all()
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.filter(slug=slug).exists():
            n = 2
            while qs.filter(slug=f"{slug}-{n}").exists():
                n += 1
            slug = f"{slug}-{n}"
        return slug

    def save(self, commit=True):
        doc = super().save(commit=False)
        doc.required_docs = [
            line.strip()
            for line in self.cleaned_data["required_docs_text"].splitlines()
            if line.strip()
        ]
        if commit:
            doc.save()
            self._save_m2m()
        return doc


class OfficeCollegeForm(forms.ModelForm):
    class Meta:
        model = College
        fields = ["name", "code", "district", "address", "contact_email", "contact_phone"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", INPUT_CLS)
