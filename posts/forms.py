from django import forms
from .models import Post, Comment


class PostCreateUpdateForm(forms.ModelForm):
	image = forms.ImageField()
	class Meta:
		model = Post
		fields = ('content', 'image')
		widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }


class CommentCreateForm(forms.ModelForm):
    comment_id = forms.IntegerField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'class':'form-control'})
        }

    def save(self, user, post):
        comment = Comment(related_post=post, user=user, content=self.cleaned_data['content'])
        comment.save()
        return comment

class CommentReplyForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('content',)


class PostSearchForm(forms.Form):
	search = forms.CharField()