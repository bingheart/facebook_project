import json

from django.db import models

# Create your models here.
class Users(models.Model):
    id = models.BigIntegerField(primary_key=True, db_index=True, editable=False, verbose_name="ID")
    name = models.CharField(max_length=250, verbose_name="user_name")
    url = models.CharField(max_length=250, verbose_name="user_url")
    item_logging_id = models.CharField(max_length=250, verbose_name="item_logging_id")
    img_url = models.CharField(max_length=500, verbose_name="img_url")
    type = models.CharField(max_length=250, verbose_name="type")
    source_data = models.TextField(verbose_name="source_data")
    def get_map(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            'item_logging_id':self.item_logging_id,
            'img_url':self.img_url,
            'type':self.type,
        }
    class Meta:
        db_table = "users"
        verbose_name = ""
        verbose_name_plural = verbose_name

class Posts(models.Model):
    id = models.AutoField(primary_key=True, db_index=True, editable=False, verbose_name="ID")
    post_id = models.CharField(max_length=250, verbose_name="post_id")
    message = models.TextField(verbose_name="message")
    feedback_id = models.CharField(max_length=250, verbose_name="feedback_id")
    video_list = models.TextField(verbose_name="video_list")
    image_list = models.TextField(verbose_name="image_list")
    posts_url = models.CharField(max_length=250, verbose_name="post_url")
    users = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name="Users")
    source_data = models.TextField(verbose_name="source_data")
    def get_map(self):
        return {
            "id": self.id,
            "post_id": self.post_id,
            "message": self.message,
            "feedback_id": self.feedback_id,
            "video_list": json.loads(self.video_list),
            "image_list": json.loads(self.image_list)
        }
    class Meta:
        db_table = "posts"
        verbose_name = ""
        verbose_name_plural = verbose_name

