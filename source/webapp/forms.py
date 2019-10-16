from django import forms
from django.forms import widgets
from django.forms import ModelForm
from webapp.models import Article


class ArticleForm(ModelForm):
    tags = forms.CharField(max_length=100,required=False,)
    # title = forms.CharField(max_length=200, required=True, label='Title')
    # author = forms.CharField(max_length=40, required=True, label='Author')
    # text = forms.CharField(max_length=3000, required=True, label='Text',
    #                        widget=widgets.Textarea)
    # category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, label='Category',
    #                                   empty_label=None)

    class Meta:
        model = Article
        fields = ['title', 'text', 'author']


class CommentForm(forms.Form):
    article = forms.ModelChoiceField(queryset=Article.objects.all(), required=True, label='Article',
                                     empty_label=None)
    author = forms.CharField(max_length=40, required=False, label='Author', initial='Аноним')
    text = forms.CharField(max_length=400, required=True, label='Text',
                           widget=widgets.Textarea)

