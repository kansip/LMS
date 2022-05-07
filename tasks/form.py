from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from tasks.models import Task

class TaskForms(forms.ModelForm):
    desc = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Task
        fields = ['desc']
  