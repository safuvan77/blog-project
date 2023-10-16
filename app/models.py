from django.db import models
from django.contrib.auth.models import User


'''

Blog

id      title           content         
4       test title      test content -> <Blog object(4)> 

blog = <Blog object(4)>

Comment

id      text    ref_blog
1       wow     <Blog object(4)>=<Blog object(4)> _/
1       wow     <Blog object(2)>=<Blog object(4)> x
1       wow     <Blog object(4)>=<Blog object(4)> _/

Model Relationships

One To One 
Many To One
Many To Many


Student

id      Name            Place       Class       batch

'''


class Blog(models.Model):
    categorise=(
        ('edu','education'),
        ('scifi',"SCIFI"),
        ('pol','politics'),
        ('others','others')
    )

    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category=models.CharField(max_length=100,choices=categorise)


class Comment(models.Model):
    text = models.CharField(max_length=300)
    ref_blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

