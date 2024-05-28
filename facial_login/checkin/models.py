from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.IntegerField(verbose_name="employee id",unique=True)
    employee_photo = models.ImageField(blank=True, null=True, upload_to='photos')
    employee_name = models.CharField(max_length=75, null=True, verbose_name="Employee Name",)
    employee_dept = models.CharField(max_length=50, null=True, verbose_name="Employee Department")
    employee_dob = models.DateField(verbose_name="Employee Date of Birth", null=True)
    
    def __str__(self) -> str:
        return f"{self.employee_name}'s profile"
    
class CheckinLogs(models.Model):
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE)
    checkin_time = models.TimeField(verbose_name="Employee Checkin Time", default=datetime.now().time())
    checkout_time = models.TimeField(verbose_name="Employee Checkout Time",null=True, default=None)
    checkin_date = models.DateField(auto_now_add=True)
    checkin_photo = models.ImageField(blank=True, null=True, upload_to='photos')
    checkout_photo = models.ImageField(blank=True, null=True, upload_to='photos')
    
class CheckinStatus(models.Model):
    employee = models.OneToOneField(EmployeeProfile, on_delete=models.CASCADE)
    is_checked_in = models.BooleanField(default=False)
    checkin_id = models.IntegerField(default=0)