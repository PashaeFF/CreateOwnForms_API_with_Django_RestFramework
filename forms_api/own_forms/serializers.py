from rest_framework import serializers

class FilledFormsSerializer(serializers.Serializer):
    email = serializers.CharField()
    fullname = serializers.CharField()
    filled_form = serializers.JSONField()
    # form_id = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    counter = serializers.IntegerField()

class FormSerializer(serializers.Serializer):
    email = serializers.EmailField()
    fullname = serializers.CharField()
    form_name = serializers.CharField()
    url = serializers.URLField()

class CreateValuesSerializer(serializers.Serializer):
    question_field_1 = serializers.DictField()
    # question_field_1_1_title = serializers.CharField()
    # question_field_1_1_description = serializers.CharField()
    # question_field_1_1_image = serializers.URLField()
    # question_field_1_1_uploaded_image = serializers.FileField()
    # question_field_1_1_youtube = serializers.URLField()
    # question_field_1_1_url = serializers.CharField()
    # question_field_1_1_button = serializers.CharField()
    # question_field_1_2_button = serializers.CharField()
    # question_field_1_1_input = serializers.CharField()
    # question_field_1_1_values = serializers.CharField()
    # question_field_1_2_values = serializers.CharField()
    # question_field_1_1_required = serializers.BooleanField()
    # question_field_1_1_allow = serializers.BooleanField()
    # question_field_1_1_one_selection = serializers.BooleanField()