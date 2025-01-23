from rest_framework import serializers
from .models import User, BaiDang, BinhLuan, Reaction

class UserSerializer(serializers.ModelSerializer):
    tuongTac = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all()
    )

    class Meta:
        model = User
        fields = ['id', 'password', 'email', 'username', 'first_name', 'last_name', 'SDT', 'image', 'vaiTro', 'tuongTac']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        tuong_tac_data = validated_data.pop('tuongTac', None)
        password = validated_data.pop('password', None)

        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()

        if tuong_tac_data:
            user.tuongTac.set(tuong_tac_data)

        return user


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'SDT']


class BaiDangSerializer(serializers.ModelSerializer):
    nguoiDangBai = UserDetailSerializer(read_only=True)

    class Meta:
        model = BaiDang
        fields = ['id', 'tieuDe', 'thongTin', 'nguoiDangBai', 'created_date', 'updated_date', 'khoa_binh_luan']


class BinhLuanSerializer(serializers.ModelSerializer):
    nguoiBinhLuan = UserDetailSerializer(read_only=True)

    class Meta:
        model = BinhLuan
        fields = ['id', 'baiDang', 'nguoiBinhLuan', 'noiDung', 'created_date']


class ReactionSerializer(serializers.ModelSerializer):
    nguoiThucHien = UserDetailSerializer(read_only=True)

    class Meta:
        model = Reaction
        fields = ['id', 'baiDang', 'nguoiThucHien', 'loai']
