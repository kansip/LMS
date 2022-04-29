""" Формы, каким либо способом связанные с пользователем """
from django import forms

class AddBlockForm(forms.Form):
    """ Форма регистрации нового пользователя """
    name = forms.CharField()
    #type = forms.ChoiceField()

    