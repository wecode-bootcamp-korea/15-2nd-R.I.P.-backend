import boto3
import uuid
import json

from django.views import View
from django.http  import JsonResponse
from django.db    import transaction

from .models      import Review, ReviewImage, ReviewHostComment, ReviewHelpCount, FeedComment, FeedLikeCount
from user.models  import User, Host
from user.utils   import login_required
from my_settings  import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

class ReviewView(View):
    
    s3_client = boto3.client(
        's3',
        aws_access_key_id     = AWS_ACCESS_KEY_ID,
        aws_secret_access_key = AWS_SECRET_ACCESS_KEY
    )
    @transaction.atomic
    @login_required
    def post(self, request, product_id):

        try:
            content     = request.POST['content']
            star_rating = request.POST['star_rating']

            user = request.user

            if request.FILES.get('file'):
                file = request.FILES['file']
                filename = str(uuid.uuid1()).replace('-', '')
                self.s3_client.upload_fileobj(
                    file,
                    "rip-dev-bucket",  
                    f'review_images/{filename}',        
                    ExtraArgs={
                        "ContentType": file.content_type
                    }
                )
                file_url = f"https://s3.ap-northeast-2.amazonaws.com/rip-dev-bucket/review_images/{filename}"

            else:
                file_url = None

            review = Review.objects.create(
                user        = user,
                product_id  = product_id,
                contents    = content,
                star_rating = star_rating,
            )
            review_image = ReviewImage.objects.create(
                review = review,
                url    = file_url,
            )
            data = {
                'id'            : review.id,
                'review_imgage' : review_image.url,
                'user_imgage'   : user.profile_image if user.profile_image else "https://i.pinimg.com/474x/85/e8/bc/85e8bc20c22d9e3817a7182413af5c5d.jpg",
                'user_name'     : user.nickname,
                'price'         : review.product.price,
                'content'       : content,
            }
            return JsonResponse({'MESSAGE': 'SUCCESS', 'REVIEW': data}, status=200)

        except KeyError as e:
            return JsonResponse({'MESSAGE': 'KEY_ERROR => ' + e.args[0]}, status=400)


    @login_required
    def patch (self, request, review_id):
        data = json.loads(request.body)
        
        try:
            review = Review.objects.get(id=review_id)

            if data.get('star_rating'):
                review.star_rating = data.get('star_rating')
            if data.get('contents'):
                review.contents = data.get('contents')
            if data.get('review_image'):
                review.review_image = data.get('review_image')
            if data.get('review_help_count') == "True":
                review.review_help_count += 1
            review.save()

            return JsonResponse({"MESSAGE":"SUCCESS"}, status=200)

        except KeyError as e:
            return JsonResponse({"MESSAGE": "KEY_ERROR => " + e.args[0]}, status=400)

        except Review.DoesNotExist:
            return JsonResponse({"MESSAGE": "REVIEW_NOT_EXIST"}, status=400)


    @login_required
    def delete(self, request, review_id):

        try:
            review = Review.objects.get(id=review_id)
            review.delete()

            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=204)

        except Review.DoesNotExist:
            return JsonResponse({"MESSAGE": "REVIEW_NOT_EXIST"}, status=400)


class ReviewSummaryView(View):

    def get(self, request, product_id):
        
        try:
            reviews = Review.objects.select_related('order','product').prefetch_related('reviewimage_set').order_by('review_help_count').filter(product=product_id)

            review_overview = [{
                'id'                : review.id,
                'nickname'          : review.order.user.nickname,
                'profile_image'     : review.order.user.profile_image,
                'contents'          : review.contents,
                'product_id'        : review.product.id,
                'review_help_count' : review.review_help_count.count(), 
                'review_image'      : review.reviewimage_set.filter(review_id=review.id)[0].url if review.reviewimage_set.filter(review_id=review.id) else none,
            } for review in reviews]

            return JsonResponse({"MESSAGE": "SUCCESS", "review_overview": review_overview}, status=201)

        except Review.DoesNotExist as e:
           return JsonResponse({"MESSAGE": "KEY_ERROR => " + e.args[0]}, status=400)


class ReviewListView(View):

    def get(self, request, product_id):

        offset = int(request.GET.get('offset', 0))
        limit  = int(request.GET.get('limit', 10))
        limit += offset
        
        try:
            reviews = Review.objects.select_related('order','product').prefetch_related('reviewimage_set', 'reviewhostcomment_set').order_by('star_rating').filter(product=product_id)

            review_list = [{
                'id'                 : review.id,
                'nickname'           : review.order.user.nickname,
                'profile_image'      : review.order.user.profile_image,
                'star_rating'        : review.star_rating,
                'created_at'         : review.created_at,
                'contents'           : review.contents,
                'product_id'         : review.product.id,
                'review_help_count'  : review.review_help_count.count(), 
                'review_image'       : [{
                    'id'  : reviewimage.id,
                    'url' : reviewimage.url
                    } for reviewimage in review.reviewimage_set.all()],
                'review_comment_list': [{ 
                    'id'        : review_comment.id,
                    'review_id' : review_comment.review.id,
                    'host'      : review_comment.host.name,
                    'contents'  : review_comment.contents
                    } for review_comment in review.reviewhostcomment_set.all()]
                } for review in reviews[offset:limit]]

            return JsonResponse({"MESSAGE":"SUCCESS", "review_list": review_list}, status=201)

        except Review.DoesNotExist as e:
           return JsonResponse({"MESSAGE":"KEY_ERROR => " + e.args[0]}, status=400)


class ReviewHostCommentView(View):

    def post(self, request, review_id):
        data = json.loads(request.body)

        try:
            contents     = Review.contents,
            review_id    = data['review_id']
            check_review = Review.objects.get(id=review_id)

            if not check_review:
                return JsonResponse({"MESSAGE":"REVIEW_NOT_EXIST"}, status=400)

            review_comment = ReviewHostComment(
                host_id    = data['host_id'], 
                review_id  = data['review_id'],
                contents   = data['contents'],
                )
            review_comment.save()

            return JsonResponse({"MESSAGE":"SUCCESS"}, status=201)

        except KeyError as e:
            return JsonResponse({"MESSAGE":"KEY_ERROR =>" + e.args[0]}, status=400)


    @login_required
    def patch (self, request, review_comment_id):
        data = json.loads(request.body)
        
        try:
            review_comment = ReviewHostComment.objects.filter(id=review_comment_id)

            if data.get('contents'):
                review_comment.contents = data.get('contents')
            review_comment.save()

            return JsonResponse({"MESSAGE":"SUCCESS"}, status=200)

        except KeyError as e:
            return JsonResponse({"MESSAGE":"KEY_ERROR => " + e.args[0]}, status=400)

        except ReviewHostComment.DoesNotExist:
            return JsonResponse({"MESSAGE":"REVIEW_COMMENT_NOT_EXIST"}, status=400)


    @login_required
    def delete(self, request, review_comment_id):

        try:
            review_comment = ReviewHostComment.objects.get(id=review_comment_id)
            review_comment.delete()

            return JsonResponse({"MESSAGE":"SUCCESS"}, status=204)

        except ReviewHostComment.DoesNotExist:
            return JsonResponse({"MESSAGE":"REVIEW_COMMENT_NOT_EXIST"}, status=400)


class FeedListView(View):

    def get(self, request):
        
        offset = int(request.GET.get('offset',0))
        limit = int(request.GET.get('limit',10))
        limit += offset
        
        try:
            feeds = Review.objects.prefetch_related('feedcomment_set').order_by('-created_at').all()

            feed_list = [{
                'id'                : feed.id,      
                'nickname'          : feed.order.user.nickname, 
                'profile_image'     : feed.order.user.profile_image, 
                'created_at'        : feed.created_at,  
                'contents'          : feed.contents, 
                'product_id'        : feed.product.id,
                'product_name'      : feed.product.name,
                'feed_like_count'   : feed.feed_like_count.count(), 
                'feed_image'        : [{        
                    'id'  : reviewimage.id,     
                    'url' : reviewimage.url     
                    } for reviewimage in feed.reviewimage_set.all()] if feed.reviewimage_set.filter(review_id=feed.id) else None,
                'feed_comment_list' : [{
                    'feedcomment_id' : feed_comment.id,
                    'product_id'     : feed_comment.review.product.id,
                    'feed_id'        : feed_comment.review.id,
                    'author'         : feed_comment.author.nickname, 
                    'contents'       : feed_comment.contents,
                    'created_at'     : feed_comment.created_at
                    } for feed_comment in feed.feedcomment_set.all()]
                } for feed in feeds[offset:limit]]

            return JsonResponse({"MESSAGE":"SUCCESS", "feed_list": feed_list}, status=201)

        except Review.DoesNotExist as e:
           return JsonResponse({"MESSAGE":"KEY_ERROR => " + e.args[0]}, status=400)


    @login_required
    def patch (self, request, review_id):  
        data = json.loads(request.body)
        
        try:
            feed = Review.objects.get(id=review_id)

            if data.get('contents'):
                feed.contents = data.get('contents')
            feed.save()

            return JsonResponse({"MESSAGE":"SUCCESS"}, status=200)

        except KeyError as e:
            return JsonResponse({"MESSAGE":"KEY_ERROR => " + e.args[0]}, status=400)


    @login_required
    def delete(self, request, review_id):
        try:
            feed = Review.objects.get(id=review_id)
            feed.delete()

            return JsonResponse({"MESSAGE":"SUCCESS"}, status=204)

        except Review.DoesNotExist:
            return JsonResponse({"MESSAGE":"FEED_NOT_EXIST"}, status=400)

        
class FeedCommentView(View):

    @login_required
    def post(self, request, review_id):
        data = json.loads(request.body)

        try:
            feed_comment = FeedComment(
                author     = request.user, 
                review_id  = data['review_id'],
                contents   = data['contents'],
                )
            feed_comment.save()

            return JsonResponse({"MESSAGE":"SUCCESS"}, status=201)

        except User.DoesNotExist:  
            return JsonResponse({"MESSAGE":"INVALID_USER"}, status=400)

        except KeyError as e:
            return JsonResponse({"MESSAGE":"KEY_ERROR =>" + e.args[0]}, status=400)


    @login_required
    def get(self, request, review_id):

        try:
            feed_comments = FeedComment.objects.select_related('author').order_by('created_at').filter(review=review_id)

            feed_comment_list = [{
                'id'        : feed_comment.id,
                'product_id': feed_comment.review.product.id,
                'feed_id'   : feed_comment.review.id,
                'author'    : feed_comment.author.nickname,
                'contents'  : feed_comment.contents,
                'created_at': feed_comment.created_at
                } for feed_comment in feed_comments.all()]

            return JsonResponse({"MESSAGE":"SUCCESS", "FEED_COMMENT_LIST": feed_comment_list}, status=200)

        except Review.DoesNotExist:  
            return JsonResponse({"MESSAGE":"FEED_NOT_EXIST"}, status=400)

        except KeyError as e:
            return JsonResponse({"MESSAGE":"KEY_ERROR =>" + e.args[0]}, status=400)


    @login_required
    def delete(self, request, feed_comment_id):
        try:
            feed_comment = FeedComment.objects.get(id=feed_comment_id)
            feed_comment.delete()

            return JsonResponse({"MESSAGE":"SUCCESS"}, status=204)

        except FeedComment.DoesNotExist:
            return JsonResponse({"MESSAGE":"FEED_COMMENT_NOT_EXIST"}, status=400)

