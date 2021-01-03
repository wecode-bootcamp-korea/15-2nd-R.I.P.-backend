from django.db      import models

from rip.core import TimeStampModel


class Review(TimeStampModel):
    order             = models.ForeignKey('order.Order', on_delete = models.PROTECT)
    contents          = models.TextField()
    product           = models.ForeignKey('product.Product', on_delete = models.CASCADE)
    feed_like_count   = models.ManyToManyField('user.User', through = "FeedLikeCount", related_name = "feed_like_counts_set")
    review_help_count = models.ManyToManyField('user.User', through = "ReviewHelpCount", related_name = "review_help_counts_set")
    star_rating       = models.DecimalField(max_digits = 2, decimal_places = 1)

    class Meta:
        db_table = 'reviews'


class ReviewImage(models.Model):
    review = models.ForeignKey(Review, on_delete = models.CASCADE)
    url    = models.URLField(max_length = 2000, null = True)

    class Meta:
        db_table = 'review_images'


class ReviewHostComment(TimeStampModel):
    host       = models.ForeignKey('user.Host', on_delete = models.SET_NULL, null=True)
    review     = models.ForeignKey('Review', on_delete = models.CASCADE)
    contents   = models.TextField()

    class Meta:
        db_table = 'review_host_comments'


class FeedComment(TimeStampModel):
    author     = models.ForeignKey('user.User', on_delete = models.SET_NULL, null=True)
    review     = models.ForeignKey('Review', on_delete = models.CASCADE)
    contents   = models.TextField()

    class Meta:
        db_table = 'feed_comments'


class FeedLikeCount(models.Model):
    user   = models.ForeignKey('user.User', on_delete = models.SET_NULL, null=True)
    review = models.ForeignKey('Review', on_delete = models.CASCADE)

    class Meta:
        db_table ='feed_like_counts'


class ReviewHelpCount(models.Model):
    user   = models.ForeignKey('user.User', on_delete = models.SET_NULL, null=True)
    review = models.ForeignKey('Review', on_delete = models.CASCADE)

    class Meta:
        db_table ='review_help_counts'


class Question(TimeStampModel):
    author     = models.ForeignKey('user.User', on_delete = models.SET_NULL, null = True)
    product    = models.ForeignKey('product.Product', on_delete = models.CASCADE)
    contents   = models.TextField()
    is_private = models.BooleanField(default = False)

    class Meta:
        db_table = 'questions'


class QuestionComment(TimeStampModel):
    host       = models.ForeignKey('user.Host', on_delete = models.SET_NULL, null = True)
    question   = models.ForeignKey('Question', on_delete = models.CASCADE)
    contents   = models.TextField()

    class Meta:
        db_table = 'question_comments'
