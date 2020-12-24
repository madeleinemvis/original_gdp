from rest_framework import serializers
from trends.models import Trend

class TrendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trend
        fields = ('uid',
                  'econ', 
                  'health', 
                  'politics')
