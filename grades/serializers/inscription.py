from rest_framework import serializers

from grades.serializers import course


class InscriptionCreationInputSerializer(serializers.Serializer):
    course_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False
    )


class InscriptionCreationOutputSerializer(serializers.Serializer):
    inscription_id = serializers.IntegerField()
    courses = course.ListCourseSerializer(many=True)
