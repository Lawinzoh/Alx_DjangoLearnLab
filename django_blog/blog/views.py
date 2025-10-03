from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import PostForm, ProfileUpdateForm, SignUpForm, UserUpdateForm
from .models import Post, Profile
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            #If profile_picture was uploaded, save it to the profile
            profile_picture = request.FILES.get('profile_picture')
            if profile_picture:
                user.profile.profile_picture = profile_picture
                user.profile.save()
            login(request, user)  # Log the user in after blog
            return redirect('profile')  # Redirect to a profile page
    else:
        form = SignUpForm()
    return render(request, 'blog/register.html', {'form': form})

@login_required # Ensure the user is logged in to view their profile
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'blog/profile.html', {'u_form': u_form, 'p_form': p_form})

def home(request):
    return render(request, 'blog/home.html')

def posts(request):
    return render(request, 'blog/posts.html')


#CRUD views for blog posts

# 1. ListView: List all blog posts (R - Read All)
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']  # Newest posts first

# 2. DetailView: Show details of a single post (R - Read One)
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

# 3. CreateView: Create a new post (only logged-in users) (C - Create)
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user  # set the post author automatically
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('post-list')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Create'
        return context

# 4. UpdateView: Update an existing post (only the author can edit) (U - Update)
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user  # ensure the author remains the same
        return super().form_valid(form)
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author  # only allow the author to edit
    def get_success_url(self):
        return reverse('post-list')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Update'
        return context

# 5. DeleteView: Delete a post (only the author can delete) (D - Delete)
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    # Redirect to the blog list after successful deletion
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author  # only allow the author to delete