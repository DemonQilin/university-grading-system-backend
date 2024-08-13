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


class AssignGradeInputSerializer(serializers.Serializer):
    student = serializers.CharField()
    grade = serializers.FloatField(min_value=0, max_value=5)


class StudentsBySubjectParamSerializer(serializers.Serializer):
    current = serializers.BooleanField(default=False)


class StudentsBySubjectSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()

    class Meta:
        model = CourseInscription
        fields = ['first_name', 'last_name', 'grade', 'date']

    def get_first_name(self, obj):
        return obj.inscription.student.first_name

    def get_last_name(self, obj):
        return obj.inscription.student.last_name

    def get_date(self, obj):
        return obj.inscription.date
