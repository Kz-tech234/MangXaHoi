from django.core.exceptions import ValidationError
from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser
from enum import IntEnum
from cloudinary.models import CloudinaryField

class VaiTro(IntEnum):
    QUANTRIVIEN = 1
    GIANGVIEN = 2
    CUUSINHVIEN = 3

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

class User(AbstractUser):
    SDT = models.CharField(max_length=10)
    image = CloudinaryField('avatar', null=True)
    vaiTro = models.IntegerField(choices=VaiTro.choices(), default=VaiTro.QUANTRIVIEN)
    tuongTac = models.ManyToManyField("self", symmetrical=False, related_name="tuong_tac")

    class Meta:
        verbose_name_plural = 'Người dùng'

class BaiDang(models.Model):
    tieuDe = models.CharField(max_length=255)
    thongTin = RichTextField()
    nguoiDangBai = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    khoa_binh_luan = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Bài đăng'

    def __str__(self):
        return self.tieuDe

class BinhLuan(models.Model):
    baiDang = models.ForeignKey(BaiDang, on_delete=models.CASCADE, related_name='binhluans')
    nguoiBinhLuan = models.ForeignKey(User, on_delete=models.CASCADE)
    noiDung = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.baiDang.khoa_binh_luan:
            raise ValidationError("Bình luận không được phép vì bài đăng đã bị khóa bình luận.")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Bình luận'

class ReactionType(IntEnum):
    LIKE = 1
    HAHA = 2
    LOVE = 3

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

class Reaction(models.Model):
    baiDang = models.ForeignKey(BaiDang, on_delete=models.CASCADE, related_name='reactions')
    nguoiThucHien = models.ForeignKey(User, on_delete=models.CASCADE)
    loai = models.IntegerField(choices=ReactionType.choices())

    class Meta:
        verbose_name_plural = 'Cảm xúc'
        unique_together = ('baiDang', 'nguoiThucHien')
