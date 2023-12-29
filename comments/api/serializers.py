from accounts.api.serializers import UserSerializerForComment
from comments.models import Comment
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from tweets.models import Tweet


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializerForComment()

    class Meta:
        model = Comment
        # use tuple, unchangeable
        fields = (
            'id',
            'tweet_id',
            'user',
            'content',
            'created_at',
            'updated_at',
        )


class CommentSerializerForCreate(serializers.ModelSerializer):
    # 这两项必须手动添加
    # 因为默认 ModelSerializer 里只会自动包含 user 和 tweet 而不是 user_id 和 tweet_id

    # User is the name of a model
    # user is an instance of User
    # users is a list of user or queryset of User
    # user_id is the primary key of User, by default is should be an int
    tweet_id = serializers.IntegerField()
    user_id = serializers.IntegerField()

    class Meta:
        model = Comment
        fields = ('content', 'tweet_id', 'user_id')

    def validate(self, data):
        tweet_id = data['tweet_id']
        if not Tweet.objects.filter(id=tweet_id).exists():
            raise ValidationError({'message': 'tweet does not exist'})
        # 必须 return validated data
        # 也就是验证过之后，进行过处理的（当然也可以不做处理）输入数据
        return data

    def create(self, validated_data):
        return Comment.objects.create(
            user_id=validated_data['user_id'],
            tweet_id=validated_data['tweet_id'],
            content=validated_data['content'],
        )