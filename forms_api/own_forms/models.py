from django.db import models
from django.utils.timezone import now


class Form(models.Model):
    email = models.CharField(max_length=200)
    url = models.CharField(max_length=500, unique=True)
    fullname = models.CharField(max_length=250)
    form_name = models.CharField(max_length=250)
    values = models.JSONField(default=dict)
    forms_count = models.IntegerField(default=0)
    image = models.ImageField(null=True, upload_to='media/images/')
    created_at = models.DateTimeField(default=now)

    class Meta:
        db_table = "own_forms"

    def __str__(self):
        return f'Email: {self.email} \nURL: {self.url} \nFullname: {self.fullname} \nForm name: {self.form_name} \nForm values: {self.values}'


class FilledForms(models.Model):
    email = models.CharField(max_length=200, null=True)
    fullname = models.CharField(max_length=250, null=True)
    filled_form = models.JSONField(default=dict)
    form_id = models.ForeignKey(Form, default=1, verbose_name="own_forms", on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now)
    counter = models.IntegerField(default=0)

    class Meta:
        db_table = "filled_forms"

    def __str__(self):
        return f'Form id: {self.form_id} \nForm: {self.filled_form}'