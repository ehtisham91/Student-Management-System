from __future__ import unicode_literals
from django.db import models
from datetime import date
from course.models import Course
from django.shortcuts import reverse


class Student(models.Model):
    name = models.CharField(max_length=200)
    registrationNo = models.AutoField(primary_key=True)
    fatherName = models.CharField(max_length=200, blank=True, null=True)
    birthDay = models.DateField(default=date.today)
    qualification = models.CharField(max_length=100)
    course = models.ManyToManyField(Course, related_name='students')

    def __str__(self):
        return '{}-{}'.format(self.registrationNo, self.name)

    @staticmethod
    def get_absolute_url():
        return reverse("home")
