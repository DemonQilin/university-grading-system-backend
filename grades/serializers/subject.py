from rest_framework import serializers

from grades.models import Subject, CourseInscription


class ListCurrentSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'credits']


class StudentSummarySerializer(serializers.Serializer):

    class CourseInscriptionSerializer(serializers.ModelSerializer):
        subject = serializers.SerializerMethodField()
        professor = serializers.SerializerMethodField()

        class Meta:
            model = CourseInscription
            fields = ['id', 'subject', 'professor', 'grade']

        def get_subject(self, obj):
            return obj.course.subject.name

        def get_professor(self, obj):
            return f'{obj.course.professor.first_name} {obj.course.professor.last_name}'

    average = serializers.FloatField()
    approved = CourseInscriptionSerializer(many=True)
    reprobated = CourseInscriptionSerializer(many=True)
    canceled = CourseInscriptionSerializer(many=True)
