from django import forms


class CommentForm(forms.Form):
    author = forms.CharField(max_length=60, label="Author", widget=forms.TextInput(attrs={'placeholder': 'Author'}))
    body = forms.CharField(label="Comment", widget=forms.TextInput(attrs={'placeholder': 'Type a comment...'}))