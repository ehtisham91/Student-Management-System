from django.db import models
from django.urls import reverse
from django.db.models import Sum
from django.db.models.signals import post_save
from django.db.models.signals import m2m_changed


class Subject(models.Model):
    name = models.CharField(max_length=100)
    total_marks = models.IntegerField(default=0)

    @property
    def get_marks(self):
        return self.marks

    @property
    def marks(self):
        return self.total_marks

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home')


class Course(models.Model):
    number = models.IntegerField(default=0)
    title = models.CharField(max_length=100)
    subject = models.ManyToManyField(Subject, related_name='subjects')
    total_marks = models.IntegerField(default=0)

    def calculate_total_marks(self):
        total = 0
        if self.subject:
            total = self.subject.aggregate(Sum('total_marks'))['total_marks__sum']
            print(total)
        return total

    def get_absolute_url(self):
        return reverse('home')

    def __str__(self):
        return self.title


def post_save_mymodel(sender, instance, action, reverse, *args, **kwargs):
    if action == 'post_add' and not reverse:
        instance.total_marks = instance.calculate_total_marks()
        instance.save()


m2m_changed.connect(post_save_mymodel, sender=Course.subject.through)