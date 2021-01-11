from django.urls import path
from .views      import ReviewView, ReviewSummaryView, ReviewListView, ReviewHostCommentView, FeedListView, FeedCommentView

urlpatterns = [
    path('/review', ReviewView.as_view()),
    path('/review/<int:review_id>', ReviewView.as_view()),
    path('/review_list/product/<int:product_id>', ReviewSummaryView.as_view()),
    path('/review_detailed_list/product/<int:product_id>', ReviewListView.as_view()),
    path('/review/comment/<int:review_id>', ReviewHostCommentView.as_view()),
    path('/review_comment/<int:review_comment_id>', ReviewHostCommentView.as_view()),
    path('/feed_list', FeedListView.as_view()),
    path('/feed_list/<int:review_id>', FeedListView.as_view()),
    path('/feed/comment/<int:review_id>', FeedCommentView.as_view()),
    path('/feed_comment/<int:feed_comment_id>', FeedCommentView.as_view()),
]
