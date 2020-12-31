# Generated by Django 3.1.4 on 2021-01-07 00:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('board', '0001_initial'),
        ('order', '0001_initial'),
        ('user', '0001_initial'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewhostcomment',
            name='host',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.host'),
        ),
        migrations.AddField(
            model_name='reviewhostcomment',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='board.review'),
        ),
        migrations.AddField(
            model_name='reviewhelpcount',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='board.review'),
        ),
        migrations.AddField(
            model_name='reviewhelpcount',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.user'),
        ),
        migrations.AddField(
            model_name='review',
            name='feed_like_count',
            field=models.ManyToManyField(related_name='feed_like_counts_set', through='board.FeedLikeCount', to='user.User'),
        ),
        migrations.AddField(
            model_name='review',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='order.order'),
        ),
        migrations.AddField(
            model_name='review',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product'),
        ),
        migrations.AddField(
            model_name='review',
            name='review_help_count',
            field=models.ManyToManyField(related_name='review_help_counts_set', through='board.ReviewHelpCount', to='user.User'),
        ),
        migrations.AddField(
            model_name='review',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.user'),
        ),
        migrations.AddField(
            model_name='questioncomment',
            name='host',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.host'),
        ),
        migrations.AddField(
            model_name='questioncomment',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='board.question'),
        ),
        migrations.AddField(
            model_name='question',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.user'),
        ),
        migrations.AddField(
            model_name='question',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product'),
        ),
        migrations.AddField(
            model_name='feedlikecount',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='board.review'),
        ),
        migrations.AddField(
            model_name='feedlikecount',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.user'),
        ),
        migrations.AddField(
            model_name='feedcomment',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.user'),
        ),
        migrations.AddField(
            model_name='feedcomment',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='board.review'),
        ),
    ]
