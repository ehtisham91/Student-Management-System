from datetime import date
from django.db import models
from course.models import Course
from student.models import Student
from django.shortcuts import reverse
from django.db.models.signals import post_save


class MarkSheet(models.Model):
    student = models.ForeignKey(Student, related_name='resultsheets', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='marksheets', on_delete=models.CASCADE)
    date_from = models.DateField(default=date.today)
    date_to = models.DateField(default=date.today)

    @property
    def get_student_name(self):
        return self.student.name

    @property
    def get_course_name(self):
        return self.course.title

    @property
    def calculate_percentage(self):
        return self.calculate_final_marks.get('obtained_marks')*100/self.calculate_final_marks.get('total_marks')

    @property
    def calculate_final_marks(self):
        final_obtained_marks = 0
        final_total_marks = 0
        for obj in self.detail.all():
            final_obtained_marks = final_obtained_marks + obj.obtained_marks
            final_total_marks = final_total_marks + obj.total_marks
        percentage = final_obtained_marks*100/final_total_marks
        return [final_obtained_marks, final_total_marks, percentage]

    @staticmethod
    def get_absolute_url():
        return reverse('home')

    def __str__(self):
        return '{}-{}'.format(self.student.name, self.course.title)


class MarkSheetDetail(models.Model):
    markSheet = models.ForeignKey(MarkSheet, related_name='detail', on_delete=models.CASCADE)
    obtained_marks = models.IntegerField(default=0)
    total_marks = models.IntegerField(default=0)
    subject = models.CharField(max_length=100)

    @property
    def calculate_percentage(self):
        return self.obtained_marks * 100 / self.total_marks

    @staticmethod
    def get_absolute_url():
        return reverse('home')

    def __str__(self):
        return '{}-{}'.format(self.markSheet.student.name, self.subject)


def post_save_marksheet_receiver(sender, instance, created, **kwargs):
    if created:
        for subj in instance.course.subject.all():
            detail_obj = MarkSheetDetail(markSheet = instance, obtained_marks = 0, subject = subj.name.lower(), total_marks = subj.marks)
            detail_obj.save()


post_save.connect(post_save_marksheet_receiver, sender=MarkSheet)
