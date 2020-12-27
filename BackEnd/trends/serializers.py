from rest_framework import serializers
from trends.models import Trend

class TrendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trend
        fields = ('uid',
                  'econ_count',
                  'econ_estimate',
                  'econ_random',
                  'econ_unobserved',
                  'econ_placebo',
                  'econ_subset',
                  'health_count',
                  'health_estimate',
                  'health_random',
                  'health_unobserved',
                  'health_placebo',
                  'health_subset',
                  'politics_count',
                  'politics_estimate',
                  'politics_random',
                  'politics_unobserved',
                  'politics_placebo',
                  'politics_subset'
                  )
