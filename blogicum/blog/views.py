from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import (get_object_or_404, redirect, render)
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from blog.models import Category, Comment, Post, User
from blogicum.constants import PAGINATOR
from .forms import CommentForm, PostForm, ProfileEditForm


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


def index(request):
    post_list = Post.custom_manager.annotate(
        comment_count=Count('comments')).order_by(
        '-pub_date'
    )
    paginator = Paginator(post_list, PAGINATOR)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'blog/index.html', context)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_object(self, queryset=None):
        post = get_object_or_404(
            self.model, id=self.kwargs[self.pk_url_kwarg]
        )
        if post.author == self.request.user:
            return post
        return get_object_or_404(
            Post.custom_manager, id=self.kwargs[self.pk_url_kwarg]
        )

    def get_context_data(self, **kwargs):
        comment_form = CommentForm()
        comments = self.object.comments.select_related('author')

        return {
            **super().get_context_data(**kwargs),
            'form': comment_form,
            'comments': comments,
        }


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category, slug=category_slug, is_published=True
    )
    posts = Post.custom_manager.filter(
        category=category).order_by(
        '-pub_date'
    )
    paginator = Paginator(posts, PAGINATOR)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'category': category,
        'page_obj': page_obj,
    }

    return render(request, 'blog/category.html', context)


def get_profile(request, username):
    profile = get_object_or_404(User, username=username)
    user_posts = profile.posts.select_related('author').annotate(
        comment_count=Count('comments')).order_by('-pub_date')
    if not request.user.is_authenticated:
        user_posts = profile.posts.select_related('author').filter(
            pub_date__lte=timezone.now(),
            is_published=True).order_by('-pub_date')

    paginator = Paginator(user_posts, PAGINATOR)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'profile': profile,
        'page_obj': page_obj,
    }
    return render(request, 'blog/profile.html', context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        post = form.save(commit=False)
        post.pub_date = timezone.now()
        post.save()
        return super().form_valid(form)

    def get_success_url(self):
        user = self.request.user.username
        return reverse('blog:profile', kwargs={'username': user})


class PostUpdateView(OnlyAuthorMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def handle_no_permission(self):
        return redirect(
            'blog:post_detail',
            post_id=self.kwargs[self.pk_url_kwarg]
        )

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs[self.pk_url_kwarg]}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(instance=self.object)
        return context


class PostDeleteView(OnlyAuthorMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'
    success_url = reverse_lazy('blog:index')


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('blog:post_detail', post_id=post_id)
    else:
        form = CommentForm()

    return render(request, 'blog/detail.html', {'form': form, 'post': post})


class CommentUpdateView(OnlyAuthorMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'
    success_url = reverse_lazy('blog:index')


class CommentDeleteView(OnlyAuthorMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'
    success_url = reverse_lazy('blog:index')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('blog:index')
    else:
        form = ProfileEditForm(instance=request.user)
        return render(request, 'blog/user.html', {'form': form})
