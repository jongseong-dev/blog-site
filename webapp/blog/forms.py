from django import forms

from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("name", "email", "body")


SEARCH_TYPE_CHOICES = (
    ("nr", "기본 검색 - 키워드 검색"),
    ("tr", "유사성 검색 - 단어의 유사성을 통한 검색"),
)


class SearchForm(forms.Form):
    query = forms.CharField()
    type = forms.ChoiceField(
        choices=SEARCH_TYPE_CHOICES, widget=forms.RadioSelect
    )
