from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import UpdateView, DeleteView, ListView, DetailView, CreateView
from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import redirect

# Create your views here.

class PostList(ListView):
    model = Post
    ordering = '-post_time_create'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10


class PostListType(PostList):

    def get_queryset(self):
        return self.model.objects.filter(type=self.kwargs.get('type'))


class PostListSearch(ListView):
    model = Post
    ordering = '-post_time_create'
    template_name = 'search.html'
    context_object_name = 'news'
    paginate_by = 5
    filterset_class = PostFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'one_news.html'
    context_object_name = 'post'


class PostCreate(CreateView, PermissionRequiredMixin):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('newsapp.add_post', )


class PostUpdate(UpdateView, PermissionRequiredMixin):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('newsapp.change_post', )


class PostDelete(DeleteView, PermissionRequiredMixin):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
    permission_required = ('newsapp.delete_post', )


class CategoryList(ListView):

    def get_queryset(self):
        category = Category.objects.get(name=self.kwargs.get('category'))
        return self.model.objects.filter(category=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(name=self.kwargs.get('category'))
        subscribers = category.subscribers.all()
        context['is_subscribed'] = self.request.user in subscribers
        return context

@login_required
def category_subscribe(request, category: str):
    category = Category.objects.get(name=category)
    category.subscribers.add(request.user)
    return redirect('/news/')



