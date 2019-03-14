from django import forms
from django.db.models import Q
from course.models import Course, Subject


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        self.fields['total_marks'].widget.attrs['readonly'] = True

    def clean(self):
        cleaned_data = self.cleaned_data
        title = self.cleaned_data.get('title')
        number = self.cleaned_data.get('number')
        objects = Course.objects.all().filter(Q(title__iexact=str(title)) | Q(number=int(number)))
        if self._errors or objects:
            raise forms.ValidationError("Course with this name/id already exists")
        else:
            return cleaned_data


class Subject_Form(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'

    def clean(self):
        cleaned_data = self.cleaned_data
        name = self.cleaned_data.get('name')
        marks = self.cleaned_data.get('total_marks')
        objects = Subject.objects.all().filter(name__iexact=name)
        if self._errors or objects:
            raise forms.ValidationError("Subject with this name already exists")
        if marks <= 0:
            raise forms.ValidationError("Total marks can't be -ve or 0")
        else:
            return cleaned_data