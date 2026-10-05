from django.db import models
from django.utils.timezone import now
# from pymongo.read_preferences import Primary


#
# # Create your models here.
class BlogPost(models.Model):
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=500,default="")
    author = models.CharField(max_length=100,default="")

    head0 = models.CharField(max_length=500,blank=True)
    cont0 = models.TextField(blank=True)

    head1 = models.CharField(max_length=500,blank=True)
    cont1 = models.TextField(blank=True)

    head2 = models.CharField(max_length=500,blank=True)
    cont2 = models.TextField(blank=True)

    time = models.DateTimeField(default=now)
    img = models.ImageField(upload_to="blog/images")

    def __str__(self):
        return self.title

