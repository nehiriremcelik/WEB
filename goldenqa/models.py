from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class Question(models.Model):
    TAG_CHOICES = [
        ('daily_life', 'Daily Life'),
        ('sports', 'Sports'),
        ('hobbies', 'Hobbies'),
        ('technology', 'Technology'),
        ('education_career', 'Education and Career'),
        ('health_fitness', 'Health and Fitness'),
        ('travel', 'Travel'),
        ('entertainment', 'Entertainment'),
        ('food_cooking', 'Food and Cooking'),
        ('music_arts', 'Music and Arts'),
        ('books_literature', 'Books and Literature'),
        ('relationships', 'Relationships'),
        ('gaming', 'Gaming'),
        ('science_nature', 'Science and Nature'),
        ('philosophy', 'Philosophy'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    tag = models.CharField(max_length=30, choices=TAG_CHOICES, default='other')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    def was_published_recently(self):
        return self.created_at >= timezone.now() - datetime.timedelta(days=1)

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer to: {self.question.text[:50]}"

class Upvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='upvotes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'answer')

class Downvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='downvotes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'answer')


