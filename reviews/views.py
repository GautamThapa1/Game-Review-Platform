from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    DeleteView,
    UpdateView,
    CreateView,
)
from .models import Game, Review, Tag
from django.urls import reverse_lazy
from .forms import Game


# Create your views here.
class GameList(ListView):
    model = Game
    template_name = "game_list.html"


class GameDetail(DetailView):
    model = Game
    template_name = "game_detail.html"


class EditReview(UpdateView):
    model = Review
    fields = ["rating", "comment"]
    template_name = "review_edit.html"


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
