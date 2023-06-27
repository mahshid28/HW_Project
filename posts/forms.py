from django import forms
from .models import Post, Comment


class PostCreateUpdateForm(forms.ModelForm):
	image = forms.ImageField(required=False)
	class Meta:
		model = Post
		fields = ('content', 'image')
		widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }


class CommentCreateForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('content',)
		widgets = {
			'content': forms.Textarea(attrs={'class':'form-control'})
		}


class CommentReplyForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('content',)


class PostSearchForm(forms.Form):
	search = forms.CharField()