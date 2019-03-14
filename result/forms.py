from django import forms
from student.models import Student
from course.models import Course, Subject
from .models import MarkSheet, MarkSheetDetail


class DateInput(forms.DateInput):
    input_type = 'date'


class MarkSheetForm(forms.ModelForm):
    class Meta:
        model = MarkSheet
        fields = '__all__'
        widgets = {
            'date_from': DateInput(),
            'date_to': DateInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['final_marks'].widget.attrs['readonly'] = True
        self.fields['course'].queryset = Course.objects.none()

        if 'student' in self.data:
            try:
                student_id = int(self.data.get('student'))
                student_obj = Student.objects.get(registrationNo=student_id)
                self.fields['course'].queryset = student_obj.course.all()
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['course'].queryset = self.instance.student.course_set

    def clean(self):
        cleaned_data = self.cleaned_data
        course_obj = self.cleaned_data.get("course")
        student_obj = self.cleaned_data.get("student")
        date_to = self.cleaned_data.get("date_to")
        date_from = self.cleaned_data.get("date_from")
        obj = MarkSheet.objects.filter(student=student_obj, course=course_obj)
        # if self._errors or obtainedMarks > totalMarks:
        if obj.count() > 0:
            raise forms.ValidationError("Marksheet of the student against this course is already present in system")
        if date_from > date_to:
            raise forms.ValidationError("From_Date should be early than To_Date")
        else:
            date_from_obj = MarkSheet.objects.filter(date_from__lt=date_from, date_to__gt=date_from)
            if date_from_obj:
                raise forms.ValidationError("Student is already enrolled during these dates")
            else:
                date_to_obj = MarkSheet.objects.filter(date_from__lte=date_to, date_to__gte=date_to)
                if date_to_obj:
                    raise forms.ValidationError("Student is already enrolled on these dates")
            return cleaned_data


class MarkSheetDetailForm(forms.ModelForm):
    class Meta:
        model = MarkSheetDetail
        fields = ('subject', 'obtained_marks', 'total_marks',)

    def __init__(self, *args, **kwargs):
        super(MarkSheetDetailForm, self).__init__(*args, **kwargs)
        if self.instance.id:
            self.fields['subject'].widget.attrs['readonly'] = True
            self.fields['total_marks'].widget.attrs['readonly'] = True

    def clean(self):
        cleaned_data = self.cleaned_data
        obtained_marks = self.cleaned_data.get('obtained_marks')
        total_marks = self.cleaned_data.get('total_marks')
        if self._errors or obtained_marks > total_marks:
            raise forms.ValidationError("obtained marks should be less than total marks")
        else:
            return cleaned_data


class CreateMarkSheetForm(forms.Form):
    student = forms.ModelChoiceField(queryset=Student.objects.none())
    course = forms.ModelChoiceField(queryset=Course.objects.none())

    def __init__(self, *args, **kwargs):
        super(CreateMarkSheetForm, self).__init__(*args, **kwargs)
        id_list = MarkSheet.objects.values_list('student').distinct()
        self.fields['student'].queryset = Student.objects.filter(registrationNo__in=id_list)
        self.fields['course'].queryset = Course.objects.none()

        if 'student' in self.data:
            try:
                student_id = int(self.data.get('student'))
                student_obj = Student.objects.get(registrationNo=student_id)
                self.fields['course'].queryset = student_obj.course.all().order_by('title')
            except (ValueError, TypeError):
                pass
        elif self.data.get('student'):
                student_id = int(self.data.get('student'))
                student_obj = Student.objects.get(registrationNo=student_id)
                self.fields['course'].queryset = student_obj.course.all().order_by('title')


class SubjectForm(forms.Form):
    name = forms.ModelChoiceField(queryset=Subject.objects.all())
