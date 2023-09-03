from django.db import models
from django.contrib.auth.models import User

class student(models.Model):
    stu_id = models.CharField(max_length=10,blank=True,null=True)
    roll_no = models.CharField(max_length=5,blank=True,null=True)
    full_name = models.CharField(max_length=40,blank=True,null=True)
    email = models.EmailField(max_length=254,null=True)

    def __str__(self):
        return self.full_name
##

class faculty(models.Model):
    fac_name = models.CharField(max_length=40,blank=True,null=True)
    email = models.CharField(max_length=40,blank=True,null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.fac_name
##

class subject(models.Model):
    sub_id = models.CharField(max_length=10,blank=True,null=True)
    sub_name = models.CharField(max_length=40,blank=True,null=True)
    faculty = models.ForeignKey(faculty, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.sub_name
##

class attendance(models.Model):
    date = models.DateField(blank=True, null=True)
    subject = models.ForeignKey(subject, on_delete=models.CASCADE, null=False)
    student = models.ForeignKey(student, on_delete=models.CASCADE, null=False)
    is_present = models.BooleanField(default=False)

    class Meta:
        unique_together = (('date', 'subject', 'student'))

    def __str__(self):
        return str(self.date)
##