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
        return reverse('subjects:subject_list')


class Course(models.Model):
    number = models.IntegerField(default=0)
    title = models.CharField(max_length=100)
    subject = models.ManyToManyField(Subject, related_name='subjects')
    total_marks = models.IntegerField(default=0)

    def calculate_total_marks(self):
        total = 0
        if self.subject:
            total = self.subject.aggregate(Sum('marks'))['marks__sum']
            print("total: ",total)
            print("first:",self.subject.all())
            print(self.number)
        return total

    def get_absolute_url(self):
        return reverse('subjects:subject_combination_list')

    def __str__(self):
        return self.title


# def post_save_course_receiver(sender, instance, **kwargs):
#     instance.calculate_total_marks()
#     # total = instance.subject.aggregate(Sum('marks'))['marks__sum']
#     # print(instance.subject.all())
#     # print(total)
#     # if total:
#     #     instance.total_marks = total
#     #     instance.save()
#
# post_save.connect(post_save_course_receiver, sender=Course)



def post_save_mymodel(sender, instance, action, reverse, *args, **kwargs):
    if action == 'post_add' and not reverse:
        instance.total_marks = instance.calculate_total_marks()
        instance.save()
        # for e in instance.my_m2mfield.all():
        #     # Query including "e"
m2m_changed.connect(post_save_mymodel, sender=Course.subject.through)