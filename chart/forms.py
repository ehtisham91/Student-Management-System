from django import forms
from student.models import Student


class StudentForm(forms.Form):
    name = forms.ModelChoiceField(queryset=Student.objects.all())