from django import forms

from .models import MovieComment


class MovieCommentForm(forms.ModelForm):

    class Meta:
        model = MovieComment
        fields = ['comment_text']

    def clean(self):
        data = super().clean()
        if "hasan" in data['comment_text']:
            raise forms.ValidationError("No hasan allowed!!")


class MovieRateForm(forms.Form):
    rate = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)], widget=forms.RadioSelect)