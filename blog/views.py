from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin # To ensure I'm logged inn to create a post
from django.contrib.auth.mixins import UserPassesTestMixin # The one updating a post s the one who created it.
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# Create your views here.


def home(request):
	return render(request, 'blog/home.html', {'posts': Post.objects.all()})


class PostListView(ListView):
	model = Post
	template_name = 'blog/home.html'
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 5

class UserPostListView(ListView):
	model = Post
	template_name = 'blog/user_posts.html'
	context_object_name = 'posts'
	paginate_by = 5

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
	model = Post
	

class PostCreateView(LoginRequiredMixin, CreateView):	# To ensure I'm logged inn to create a post
	model = Post
	fields = ['title', 'content']

	def form_valid(self,form):
		form.instance.author = self.request.user
		return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):	# To ensure I'm logged inn to create a post
	model = Post
	fields = ['title', 'content']

	def form_valid(self,form):
		form.instance.author = self.request.user
		return super().form_valid(form)


	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False


class PostDeleteView(DeleteView, LoginRequiredMixin, UserPassesTestMixin):
	model = Post
	success_url = '/'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False


def about(request):
	return render(request, 'blog/about.html', {'title': 'About'})


