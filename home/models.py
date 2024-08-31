from django.db import models
from django.utils import timezone

class Group(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name



class Teacher(models.Model):
    name = models.CharField(max_length=100)
    groups = models.ManyToManyField(Group, related_name='teachers')

    def __str__(self):
        return self.name


from django.db import models
class Student(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True)
    payment_status = models.BooleanField(default=False)
    group_payment = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    group = models.ForeignKey(Group, related_name='students', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
