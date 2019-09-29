from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
# 作者表
GENDER = (
    (1,'男'),
    (2,'女')
)
class Author(models.Model):
    name = models.CharField(max_length=32,verbose_name='姓名')
    age = models.IntegerField(verbose_name='年龄')
    gender = models.IntegerField(choices=GENDER,verbose_name='性别')
    email = models.EmailField(verbose_name='邮箱')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'author'


# 文章类型表
class Type(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'type'

# 文章表
class Article(models.Model):
    title = models.CharField(max_length=32)
    data = models.DateField(auto_now=True)
    content = RichTextField()
    description = RichTextField()
    picture = models.ImageField(upload_to='images')
    click = models.IntegerField(verbose_name='点击率',default=0)
    recommend = models.IntegerField(verbose_name='推荐',default=0)
    author = models.ForeignKey(to=Author, on_delete=models.SET_DEFAULT, default=1)
    type = models.ManyToManyField(to=Type)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'article'


class User(models.Model):
    name = models.CharField(max_length=32,verbose_name='用户名')
    password = models.CharField(max_length=32,verbose_name='密码')

    class Meta:
        db_table = 'user'


class LoginUser(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=32)
    username = models.CharField(max_length=32,null=True,blank=True)
    phone_number = models.CharField(max_length=11,null=True,blank=True)
    photo = models.ImageField(upload_to='images',null=True,blank=True)
    age = models.IntegerField(null=True,blank=True)
    gender = models.CharField(null=True,blank=True,max_length=4)
    address = models.TextField(null=True,blank=True)
    class Meta:
        db_table = 'LoginUser'