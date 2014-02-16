from kay.utils import forms
import models


class TweetForm(forms.Form):
    code = forms.TextField(required=True, widget=forms.Textarea)
    message = forms.TextField(max_length=100)

