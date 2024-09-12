from rest_framework import serializers


class UsersListSerializer(serializers.Serializer):
    class Meta:
        fields = ['username', 'password1', 'password2']
        write_only_fields = ['password1', 'password2']


class SubjectSerializer(serializers.Serializer):
    subject_name = serializers.CharField()
    subject_score = serializers.IntegerField()
    subject_credit = serializers.IntegerField()

    class Meta:
        fields = ['id', 'subject_name', 'subject_score', 'subject_credit']

