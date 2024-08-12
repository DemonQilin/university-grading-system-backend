from rest_framework import serializers

from grades.models import Course, Subject, Professor


class ListCourseSerializer(serializers.ModelSerializer):
    """
    Serializer for the list of courses.
    """

    class SubjectSerializer(serializers.ModelSerializer):
        """
        Serializer for the subject in list of courses.
        """
        class Meta:
            model = Subject
            fields = ['name', 'credits']

    class ProfessorSerializer(serializers.ModelSerializer):
        """
        Serializer for the professor in list of courses.
        """

        class Meta:
            model = Professor
            fields = ['first_name', 'last_name']

    subject = SubjectSerializer(read_only=True)
    professor = ProfessorSerializer(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'subject', 'professor']
