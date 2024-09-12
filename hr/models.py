from django.db import models
from account.models import UserProfile
from datetime import date, datetime
from .choices import *

# Create your models here.
class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Attendance(Base):
    employee = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='employee_attendance')
    workplace = models.CharField(choices=WORK_PLACES, max_length=10, null=True,)
    date = models.DateField(default=date.today)
    type = models.CharField(choices=ATTENDANCE_TYPE, max_length=10, default='absent')
    
    def __str__(self):
        return f'{self.employee}-{self.id}'

    class Meta:
        unique_together = ('workplace', 'date', 'employee')
        verbose_name = 'Attendance'
        ordering = ['-date']

class AttendanceDetail(Base):
    attendance = models.ForeignKey(Attendance,on_delete=models.CASCADE, related_name='attendance_detail')
    entry_type = models.CharField(choices=(('IN','IN'),('OUT','OUT')), max_length=4, null=False, blank=False)
    date = models.DateField(default=date.today)
    time = models.TimeField()

    def __str__(self):
        return f"{self.id}"