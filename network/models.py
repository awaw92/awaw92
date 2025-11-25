from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    # Obserwowanie innych użytkowników (relacja M2M)
    following = models.ManyToManyField("self", related_name="followed_by", symmetrical=False)

    def __str__(self):
        return self.username


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    # Dodajemy pole do przechowywania liczby polubień
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:30]}"

    def total_likes(self):
        """Metoda do liczenia liczby polubień danego posta"""
        return self.likes.count()


class Follow(models.Model):
    """Model do przechowywania relacji follow/unfollow"""
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following_users")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers_users")

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"
