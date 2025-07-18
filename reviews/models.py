from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Game(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True)
    image = models.ImageField(upload_to="game_images/", blank=True)

    def __str__(self):
        return self.title

    def average_rating(self):
        reviews = self.review_set.all()
        if not reviews:
            return 0  # There are no reviews

        total = sum(
            review.rating for review in reviews
        )  # sum(x.rating for x in reviews)
        avg = total / reviews.count()
        return round(avg, 2)

    def get_absolute_url(self):
        return reverse("game_detail", kwargs={"pk": self.pk})


class Review(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (
            "game",
            "user",
        )  # only at database level, would not duplicate the reviews

    def __str__(self):
        return f"{self.user.username} - {self.game.title}"

    def get_absolute_url(self):
        return reverse("game_detail", kwargs={"pk": self.pk})
