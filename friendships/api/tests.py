from django_hbase.models import EmptyColumnError, BadRowKeyError
from friendships.hbase_models import HBaseFollowing, HBaseFollower
from friendships.models import Friendship
from friendships.services import FriendshipService
from testing.testcases import TestCase
import time


class FriendshipServiceTests(TestCase):

    def setUp(self):
        super(FriendshipServiceTests, self).setUp()
        self.linghu = self.create_user('linghu')
        self.dongxie = self.create_user('dongxie')

    def test_get_followings(self):
        user1 = self.create_user('user1')
        user2 = self.create_user('user2')
        for to_user in [user1, user2, self.dongxie]:
            self.create_friendship(from_user=self.linghu, to_user=to_user)

        user_id_set = FriendshipService.get_following_user_id_set(self.linghu.id)
        self.assertSetEqual(user_id_set, {user1.id, user2.id, self.dongxie.id})

        FriendshipService.unfollow(self.linghu.id, self.dongxie.id)
        user_id_set = FriendshipService.get_following_user_id_set(self.linghu.id)
        self.assertSetEqual(user_id_set, {user1.id, user2.id})


class HBaseTests(TestCase):
    @property
    def ts_now(self):
        return int(time.time() * 1000000)

    def test_save_and_get(self):
        timestamp = self.ts_now
        following = HBaseFollowing(from_user_id=123, to_user_id=34, created_at=timestamp)
        following.save()
        instance = HBaseFollowing.get(from_user_id=123, created_at=timestamp)
        self.assertEqual(instance.from_user_id, 123)
        self.assertEqual(instance.to_user_id, 34)
        self.assertEqual(instance.created_at, timestamp)
        following.to_user_id = 456
        following.save()
