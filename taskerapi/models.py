from django.db import models
import datetime
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
# Create your models here.


class Task(models.Model):
    class Meta:
        ordering = ['-activates_on']
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    desc = models.TextField(blank=True)
    is_interval = models.BooleanField()
    interval_days = models.PositiveSmallIntegerField(
        blank=True, null=True)
    activates_on = models.DateField(blank=True)

    def __str__(self):
        return self.name

    def clean(self):
        if self.is_interval == False and self.activates_on != None and self.interval_days == None:
            pass
        elif self.is_interval == True and self.activates_on == None and self.interval_days != None:
            self.activates_on = now().date() + \
                datetime.timedelta(self.interval_days)
        else:
            raise ValidationError(
                "If is_interval is true, you should send interval_days and shouldn't send activates_on. If is_interval is false, you shouldn't send interval_days and send activates_on.")
