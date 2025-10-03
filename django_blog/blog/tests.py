from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from blog.models import Post

class PostCRUDTests(TestCase):

    def setUp(self):
        # Create a test user with your registration details
        self.user = User.objects.create_user(
            username="lawinzoh",
            email="lawinzoh@example.com",
            password="supersecret"
        )
        # Create a sample post
        self.post = Post.objects.create(
            title="My First Post",
            content="This is the content of my first post.",
            author=self.user
        )

    # ---------------- CRUD Tests ----------------
    def test_post_list_view(self):
        response = self.client.get(reverse('post-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "My First Post")

    def test_post_detail_view(self):
        response = self.client.get(reverse('post-detail', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This is the content of my first post.")

    def test_create_post_view_authenticated(self):
        self.client.login(username="lawinzoh", password="supersecret")
        response = self.client.post(reverse('post-create'), {
            'title': "New Post",
            'content': "Some fresh content."
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(title="New Post").exists())

    def test_create_post_view_unauthenticated(self):
        response = self.client.post(reverse('post-create'), {
            'title': "Unauthorized Post",
            'content': "Should not be allowed."
        })
        self.assertNotEqual(response.status_code, 200)
        self.assertFalse(Post.objects.filter(title="Unauthorized Post").exists())

    def test_update_post_view_by_author(self):
        self.client.login(username="lawinzoh", password="supersecret")
        response = self.client.post(reverse('post-update', args=[self.post.id]), {
            'title': "Updated Post",
            'content': "This content has been updated."
        })
        self.assertEqual(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "Updated Post")

    def test_delete_post_view_by_author(self):
        self.client.login(username="lawinzoh", password="supersecret")
        response = self.client.post(reverse('post-delete', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())

    def test_update_post_view_by_other_user(self):
        other_user = User.objects.create_user(
            username="notlawinzoh",
            password="otherpassword"
        )
        self.client.login(username="notlawinzoh", password="otherpassword")
        response = self.client.post(reverse('post-update', args=[self.post.id]), {
            'title': "Hack Attempt",
            'content': "Trying to edit someone else's post."
        })
        self.assertEqual(response.status_code, 403)

    def test_delete_post_view_by_other_user(self):
        other_user = User.objects.create_user(
            username="notlawinzoh",
            password="otherpassword"
        )
        self.client.login(username="notlawinzoh", password="otherpassword")
        response = self.client.post(reverse('post-delete', args=[self.post.id]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Post.objects.filter(id=self.post.id).exists())

    # ---------------- Navigation Tests ----------------
    def test_navigation_home_link(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Home")

    def test_navigation_posts_link(self):
        response = self.client.get(reverse('post-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Blog Posts")

    def test_navigation_login_link(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")

    def test_navigation_register_link(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Register")
