from rest_framework import serializers
from main.models import Program

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ['id', 'name', 'guidebox_id', 'rating', 'runtime', 'thumbnail', 'banner', 'overview', 'review', 'positive_message', 'positive_role_model', 'violence', 'sex', 'language', 'consumerism', 'substance']
