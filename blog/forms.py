from django import forms
from blog.models import Comment

class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',
                                                         'id': 'didgah-body',
                                                         'placeholder': 'دیدگاه خود را بنویسید'}), label='دیدگاه')
    parent_id = forms.CharField(widget=forms.HiddenInput(attrs={'class': 'form-control',
                                                                'value': 'NONE',
                                                                'id': 'parent_id'
                                                                }))

    class Meta:
        model = Comment
        fields = ('text',)