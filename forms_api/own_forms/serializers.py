from rest_framework import serializers

class FilledFormsSerializer(serializers.Serializer):
    email = serializers.CharField()
    fullname = serializers.CharField()
    filled_form = serializers.JSONField()
    created_at = serializers.DateTimeField()
    counter = serializers.IntegerField()

class FormSerializer(serializers.Serializer):
    email = serializers.EmailField()
    fullname = serializers.CharField()
    form_name = serializers.CharField()
    url = serializers.URLField()

class CreateValuesSerializer(serializers.Serializer):
    question_field_1 = serializers.DictField()