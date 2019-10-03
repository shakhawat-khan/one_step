from django.shortcuts import render,redirect,get_object_or_404,HttpResponseRedirect
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import Post,Comment
from .forms import CommentForm
from causes.models import Catagory
# Create your views here.

class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'posts.html'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_context_data(self, **kwargs):          
        context = super().get_context_data(**kwargs)                     
        popular = Post.objects.all().annotate(num_likes=Count('likes')).order_by('-num_likes')
        catagories = Catagory.objects.all()
        context['catagories'] = catagories
        if len(popular)>3:
            context['popular'] = popular[:3]
        else:
            context['popular'] = popular
            
        return context




# class PostDetailView(DetailView):
#     model = Post
#     template_name = 'post_detail.html'

def post_detail(request,pk):
    post = get_object_or_404(Post, id=pk)
    popular = Post.objects.all().exclude(id=post.id).annotate(num_likes=Count('likes')).order_by('-num_likes')
    try:
        next_post = (Post.objects.filter(title__gte=post.title, id__gt=post.id).exclude(id=post.id).order_by('title', 'id').first())
    except Post.DoesNotExist:
        next_post = None

    try:
        previous_post = (Post.objects.filter(title__lte=post.title, id__lt=post.id).exclude(id=post.id).order_by('-title', '-id').first())

    except Post.DoesNotExist:
        previous_post = None

    comments = Comment.objects.filter(post=post).order_by('-id')
    catagories = Catagory.objects.all()
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True 
    
    if request.method=='POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('content')
            comment = Comment.objects.create(post=post, user=request.user, content=content)
            comment.save()
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'is_liked': is_liked,
        'total_likes': post.total_likes(),
        'comments': comments,
        'comment_form': comment_form,
        'next_post': next_post,
        'previous_post': previous_post,
        'catagories': catagories,
        
    }
    if len(popular)>3:
        context['popular'] = popular[:3]
    else:
        context['popular'] = popular
    return render(request, 'post_detail.html', context)


@login_required
def like_post(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user.id)
        post.save()
        is_liked = False 
    else:
        post.likes.add(request.user.id)
        post.save()
        is_liked = True 

    return HttpResponseRedirect(post.get_absolute_url())

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_create.html'
    fields = ['title', 'content', 'catagory', 'thumbnail']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'post_create.html'
    fields = ['title', 'content', 'catagory', 'thumbnail']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        Post = self.get_object()
        if self.request.user == Post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = '/posts'
    def test_func(self):
        Post = self.get_object()
        if self.request.user == Post.author:
            return True
        return False