from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from posts.models import Post, Comment, Like, PostImage, Tag
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from posts.forms import PostCreateUpdateForm, CommentCreateForm, CommentReplyForm, PostSearchForm
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class HomeView(View):
	form_class = PostSearchForm

	def get(self, request):
		posts = Post.objects.all()
		if request.GET.get('search'):
			posts = posts.filter(content__contains=request.GET['search'])
		return render(request, 'home/index.html', {'posts':posts, 'form':self.form_class})


class PostDetailView(View):
	form_class = CommentCreateForm
	form_class_reply = CommentReplyForm

	def setup(self, request, *args, **kwargs):
		self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'], slug=kwargs['post_slug'])
		return super().setup(request, *args, **kwargs)

	def get(self, request, *args, **kwargs):
		comments = self.post_instance.pcomments.filter(is_reply=False)
		can_like = False
		if request.user.is_authenticated and self.post_instance.user_can_like(request.user):
			can_like = True
		post_images = self.post_instance.postimage_set.all()
		return render(request, 'home/detail.html', {'post':self.post_instance, 'comments':comments, 'form':self.form_class, 'reply_form':self.form_class_reply, 'can_like':can_like})

	@method_decorator(login_required)
	def post(self, request, *args, **kwargs):
		form = CommentCreateForm(request.POST)
		if form.is_valid():
			new_comment = form.save(user=request.user, post=self.post_instance)
			messages.success(request, 'your comment submitted successfully', 'success')
			return redirect('home:post_detail', self.post_instance.id, self.post_instance.slug)


class PostDeleteView(LoginRequiredMixin, View):
	def get(self, request, post_id):
		post = get_object_or_404(Post, pk=post_id)
		if post.user.id == request.user.id:
			post.delete()
			messages.success(request, 'post deleted successfully', 'success')
		else:
			messages.error(request, 'you cant delete this post', 'danger')
		return redirect('home:home')


class PostUpdateView(LoginRequiredMixin, View):
	form_class = PostCreateUpdateForm

	def setup(self, request, *args, **kwargs):
		self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'])
		return super().setup(request, *args, **kwargs)

	def dispatch(self, request, *args, **kwargs):
		post = self.post_instance
		if not post.user.id == request.user.id:
			messages.error(request, 'you cant update this post', 'danger')
			return redirect('home:home')
		return super().dispatch(request, *args, **kwargs)

	def get(self, request, *args, **kwargs):
		post = self.post_instance
		form = self.form_class(instance=post)
		return render(request, 'home/update.html', {'form':form})

	def post(self, request, *args, **kwargs):
		post = self.post_instance
		form = self.form_class(request.POST, request.FILES, instance=post)
		if form.is_valid():
			new_post = form.save(commit=False)
			new_post.slug = slugify(form.cleaned_data['content'][:30])
			new_post.save()
			if form.cleaned_data.get('image'):
				for image in request.FILES.getlist('image'):
					PostImage.objects.create(post=new_post, image=image)
			messages.success(request, 'you updated this post', 'success')
			return redirect('home:post_detail', post.id, post.slug)
		else:
			return render(request, 'home/update.html', {'form': form})

class PostCreateView(LoginRequiredMixin, View):
	form_class = PostCreateUpdateForm

	def get(self, request, *args, **kwargs):
		form = self.form_class
		return render(request, 'home/create.html', {'form':form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST, request.FILES)
		if form.is_valid():
			new_post = form.save(commit=False)
			new_post.slug = slugify(form.cleaned_data['content'][:30])
			new_post.user = request.user
			new_post.save()
			if form.cleaned_data.get('image'):
				for image in request.FILES.getlist('image'):
					PostImage.objects.create(related_post=new_post, image=image)
			messages.success(request, 'you created a new post', 'success')
			return redirect('home:post_detail', new_post.id, new_post.slug)
		return render(request, 'home/create.html', {'form':form})

class PostAddReplyView(LoginRequiredMixin, View):
	form_class = CommentReplyForm

	def post(self, request, post_id, comment_id):
		post = get_object_or_404(Post, id=post_id)
		comment = get_object_or_404(Comment, id=comment_id)
		form = self.form_class(request.POST)
		if form.is_valid():
			reply = form.save(commit=False)
			reply.user = request.user
			reply.post = post
			reply.reply = comment
			reply.is_reply = True
			reply.save()
			messages.success(request, 'your reply submitted successfully', 'success')
		return redirect('home:post_detail', post.id, post.slug)

@login_required
def edit_comment(request, comment_id):
	comment = Comment.objects.get(id=comment_id)

	if request.method == 'POST':
		new_content = request.POST.get('content')
		try:
			comment.edit_comment(request.user, new_content)
			messages.success(request, 'Comment edited successfully.')
		except (PermissionError, ValueError) as e:
			messages.error(request, str(e))
		return redirect('post-detail', post_id=comment.post.id)

	context = {
		'comment': comment
	}
	return render(request, 'edit_comment.html', context)


class PostLikeView(LoginRequiredMixin, View):
	def get(self, request, post_id):
		post = get_object_or_404(Post, id=post_id)
		like = Like.objects.filter(related_post=post, user=request.user)
		if like.exists():
			messages.error(request, 'you have already liked this post', 'danger')
		else:
			Like.objects.create(related_post=post, user=request.user)
			messages.success(request, 'you liked this post', 'success')
		return redirect('home:post_detail', post.id, post.slug)