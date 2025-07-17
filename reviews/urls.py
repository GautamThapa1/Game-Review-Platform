from django.urls import path
from .views import (
    GameList,
    GameDetail,
    EditReview,
    GameDelete,
    GameUpdate,
    DeleteReview,
    GameAdd,
    TagAdd,
    TagDelete,
)

urlpatterns = [
    path("", GameList.as_view(), name="game_list"),
    path("<int:pk>", GameDetail.as_view(), name="game_detail"),
    path("games/<int:pk>/edit/", GameUpdate.as_view(), name="game_edit"),
    path("games/<int:pk>/delete/", GameDelete.as_view(), name="game_delete"),
    path("reviews/<int:pk>/edit/", EditReview.as_view(), name="review_edit"),
    path("reviews/<int:pk>/delete/", DeleteReview.as_view(), name="review_delete"),
    path("games/add/", GameAdd.as_view(), name="game_add"),
    path("games/add/tagAdd/", TagAdd.as_view(), name="tag_add"),
    path("tags/delete/<int:pk>/", TagDelete.as_view(), name="tag_delete"),
]
