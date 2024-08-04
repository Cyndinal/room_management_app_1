from django.forms import ModelForm

from crud_app.models import Room


class FormCreation(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
