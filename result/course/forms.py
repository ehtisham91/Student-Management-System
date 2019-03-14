from django import forms
from student.models import Student


class SubjectForm(forms.Form):
    name = forms.ModelChoiceField(queryset=Student.objects.all())
