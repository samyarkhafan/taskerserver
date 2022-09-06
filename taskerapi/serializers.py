from rest_framework import serializers
from .models import Task
from django.utils.timezone import now
import datetime


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Task
        fields = '__all__'

    def validate(self, data):
        if 'activates_on' not in data:
            data['activates_on'] = None
        if 'interval_days' not in data:
            data['interval_days'] = None
        if data['is_interval'] == False and data['activates_on'] != None and data['interval_days'] == None:
            return data
        elif data['is_interval'] == True and data['activates_on'] == None and data['interval_days'] != None:
            data['activates_on'] = now().date() + \
                datetime.timedelta(data['interval_days'])
            return data
        else:
            raise serializers.ValidationError(
                "If is_interval is true, you should send interval_days and shouldn't send activates_on. If is_interval is false, you shouldn't send interval_days and send activates_on.")
