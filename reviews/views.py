from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    DeleteView,
    UpdateView,
    CreateView,
)
from .models import Game, Review, Tag
from django.urls import reverse_lazy, reverse
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect


# Create your views here.
class GameList(ListView):
    model = Game
    template_name = "game_list.html"

    def get_queryset(self):
        query = self.request.GET.get("searched")
        if query:
            return Game.objects.filter(title__icontains=query)
        return Game.objects.all()


class GameDetail(DetailView):
    model = Game
    template_name = "game_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["review_form"] = ReviewForm()  # Name given for understanding
        context["reviews"] = self.object.review_set.all()
        return context


@login_required
def add_review(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    # Check if user already reviewed this game
    existing_review = game.review_set.filter(user=request.user).first()
    if existing_review:
        # Option 1: Redirect back with a message, or
        # Option 2: Update the existing review instead of creating a new one
        # For now, let's just redirect to game detail without saving duplicate
        return redirect("game_detail", pk=game.id)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.game = game
            review.save()
    return redirect("game_detail", pk=game.id)


class EditReview(UpdateView):
    model = Review
    fields = ["rating", "comment"]
    template_name = "review_edit.html"

    def get_success_url(self):
        # Redirect to the related game's detail page after saving the review
        return reverse("game_detail", kwargs={"pk": self.object.game.id})


class GameDelete(DeleteView):
    model = Game
    template_name = "game_delete.html"
    success_url = reverse_lazy("game_list")  # it doesn't require pk cuz it's list view


class GameUpdate(UpdateView):
    model = Game
    template_name = "game_edit.html"
    fields = "__all__"


class DeleteReview(DeleteView):
    model = Review
    template_name = "review_delete.html"

    def get_success_url(self):
        return reverse_lazy("game_detail", kwargs={"pk": self.object.game.id})

    # it requires pk cuz it's in detail view and which game to load


class GameAdd(CreateView):
    model = Game
    template_name = "game_add.html"
    fields = "__all__"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all()
        return context


class ReviewAdd(CreateView):
    model = Review
    template_name = "review_add.html"
    fields = ["rating", "comment"]


class TagAdd(CreateView):
    model = Tag
    template_name = "tag_add.html"
    fields = "__all__"

    def get_success_url(self):
        return reverse_lazy("game_add")


class TagDelete(DeleteView):
    model = Tag
    template_name = "tag_delete.html"
    success_url = reverse_lazy("game_add")
