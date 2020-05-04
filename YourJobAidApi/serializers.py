from rest_framework import serializers
from django.core.mail import send_mail
from smtplib import SMTPException
import socket
from django.template import loader
from django.contrib.auth.models import Group
from . import models

from rest_framework.serializers import CharField

###############################################################--user-serializers-start--############################################################


class UserSerializer(serializers.ModelSerializer):
    #group = serializers.StringRelatedField(source='group.name')
    group = serializers.SerializerMethodField()
    confirm_password = CharField(max_length=128, write_only=True, style={'input_type': 'password'})

    class Meta:
        model = models.UserProfile
        fields = ['id', 'name', 'email', 'password', 'confirm_password', 'bio', 'group', 'profile_pic']

        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            },
           }

    def get_group(self, obj):
        return str(obj.group)

    def create(self, validated_data):
        """Handle creating user account"""
        password = validated_data.pop('password')
        validated_data.pop('confirm_password')
        user = models.UserProfile(**validated_data)
        user.set_password(password)
        user.save()

        return user

    def update(self, instance, validated_data):
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)

    def validate_confirm_password(self, value):
        data = self.get_initial()
        password = data.get('password')
        confirm_password = value
        if password != confirm_password:
            raise serializers.ValidationError('Password and confirm Password not matched')
        return value



class UpdateUserRoleSerializer(serializers.ModelSerializer):
    group_name = serializers.SerializerMethodField()
    class Meta:
        model = models.UserProfile
        fields = ['id', 'name', 'email','group_name', 'group']

    def get_group_name(self, obj):

        return str(obj.group)



class UserRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'

###############################################################--user-serializers-end--############################################################

###############################################################--Category-serializers-start--######################################################


class CategorySerializers(serializers.ModelSerializer):
    totalposts = serializers.IntegerField(
        source='totalposts.count',
        read_only=True
    )

    class Meta:
        model = models.Category
        fields = ['id', 'title', 'slug', 'totalposts']

    def validate_title(self, value):
        if len(value) < 1:
            raise serializers.ValidationError('Please enter a name of category')
        return value

###############################################################--Category-serializers-end--######################################################

###############################################################--post-serializers-start--########################################################


class PostCreateSerializers(serializers.ModelSerializer):

    class Meta:
        model = models.Post
        fields = ['id', 'title', 'slug', 'category', 'img', 'meta', 'description', 'user', 'get_date']
        read_only_fields = ['user']

    def validate_title(self, value):
        if len(value) < 1:
            raise serializers.ValidationError('Please enter title')
        return value

    def validate_img(self, value):
        if len(value) < 1:
            raise serializers.ValidationError('Please enter an image link')
        return value

    def validate_meta(self, value):
        if len(value) < 1:
            raise serializers.ValidationError('Please enter meta')
        return value

    def validate_description(self, value):
        if len(value) < 1:
            raise serializers.ValidationError('Please enter description')
        return value


class PostListSerializers(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
   # category_slug = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    class Meta:
        model = models.Post
        fields = ['id', 'title', 'slug', 'category', 'img', 'meta', 'description', 'user', 'get_date']
        read_only_fields = ['user']

    def get_user(self, obj):
        return str(obj.user.name)

    def get_category(self, obj):
        res = {'title': obj.category.title, 'slug': obj.category.slug}
        return res


class PostDetailUpdateDeleteSerializers(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    category = CategorySerializers(read_only=True)

    class Meta:
        model = models.Post
        fields = ['id', 'title', 'slug', 'category', 'img', 'meta', 'description', 'user',
                  'get_date']
        read_only_fields = ['user', 'category']

    def get_user(self, obj):
        res = {
            'id': obj.user.id,
            'name': obj.user.name,
            'email': obj.user.email,
            'bio': obj.user.bio,
            'group': obj.user.group.name,
            'profile_pic': obj.user.profile_pic.url
        }

        return res

###############################################################--post-serializers-end--########################################################

###########################################################--comment-serializers-start--######################################################


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = '__all__'


class CommentRepliesSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = models.Comment
        fields = ['text', 'get_time', 'user']

    def get_user(self, obj):
        data = {
            'id': obj.user.id,
            'name': obj.user.name,
            'profile_pic': obj.user.profile_pic.url
        }
        return data


class CommentDetailSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = models.Comment
        fields = ['id', 'text', 'replies', 'get_time', 'user']

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentRepliesSerializer(obj.children(), many=True).data
        return None

    def get_user(self, obj):
        data = {
            'id':obj.user.id,
            'name':obj.user.name,
            'profile_pic': obj.user.profile_pic.url
        }
        return data



###########################################################--comment-serializers-end--########################################################

########################################################--ContactUs-serializers-start--########################################################

class ContactUsSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.ContactUs
        fields = '__all__'
        read_only_fields = ['is_seen', 'email_isSent']

    def validate_name(self, value):
        if len(value) < 1:
            raise serializers.ValidationError('Please enter your name !')
        for char in str(value):
            if char.isdigit():
                raise serializers.ValidationError('Please enter a valid name')

        return value

    def validate_message(self, value):
        if len(value) < 1:
            raise serializers.ValidationError('Please enter your message !')

        return value

    def validate_email(self, value):
        if len(value) < 1:
            raise serializers.ValidationError('Please enter your email !')

        return value

    def create(self, validate_data):
        # instance = super(ContactUsSerializers, self).create(validate_data)
        #instance.pk

        template_name = 'YourJobAidApi/email_template.html'
        subject = "User suggestion from YourJobAid"
        message = 'The following message has been sent ==>'
        context = { 'data': validate_data}
        html_message = loader.render_to_string(template_name, context)
        email_from = 'emailmanager.yourjobaid@gmail.com'
        to = ['devilzhut@gmail.com', 'rayhanbillah@hotmail.com']

        try:
            send_mail(subject, message, email_from, to, fail_silently=False, html_message= html_message)
        except SMTPException:
            validate_data['email_isSent'] = False
        except socket.error:
            validate_data['email_isSent'] = False

        contactus = models.ContactUs.objects.create(**validate_data)

        return contactus


########################################################--ContactUs-serializers-end--########################################################