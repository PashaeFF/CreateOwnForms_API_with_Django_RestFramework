from rest_framework import serializers

class FilledFormsSerializer(serializers.Serializer):
    email = serializers.CharField()
    fullname = serializers.CharField()
    filled_form = serializers.JSONField()
    # form_id = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    counter = serializers.IntegerField()