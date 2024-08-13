from rest_framework import serializers

from grades.models import Subject


class ListCurrentSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'credits']
