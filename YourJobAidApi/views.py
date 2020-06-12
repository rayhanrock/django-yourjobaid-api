from rest_framework import viewsets, filters, views, generics
from rest_framework.response import Response
from django.contrib.auth.models import Group
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from . import permissions, models, serializers
from .pagination import PostPageNumberPagination, PaginationFuctionForApiView

#################################################################--user-views-start--##############################################################

class UserViewSets(viewsets.ModelViewSet):
    queryset = models.UserProfile.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.UpdateOwnProfile,)
    authentication_classes = (TokenAuthentication,)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    ordering_fields = ('id',)
    search_fields = ('name', 'email',)


class UserLoginApiView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserRoleViewSets(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = serializers.UserRoleSerializer
    permission_classes = (IsAdminUser, )
    authentication_classes = (TokenAuthentication, )


class UpdateUserRoleViewSets(generics.RetrieveUpdateAPIView):
    queryset = models.UserProfile.objects.all()
    serializer_class = serializers.UpdateUserRoleSerializer
    pagination_class = PostPageNumberPagination
    permission_classes = (IsAdminUser, )
    authentication_classes = (TokenAuthentication, )

#################################################################--user-views-end--##############################################################

###############################################################--post-views-start--##############################################################


class PostCreateView(generics.CreateAPIView):
    serializer_class = serializers.PostCreateSerializers
    permission_classes = (permissions.IsAdmin_IsAuthor, )
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostListView(generics.ListAPIView):
    lookup_field = 'slug'
    queryset = models.Post.objects.all().order_by('-created_at')
    serializer_class = serializers.PostListSerializers
    pagination_class = PostPageNumberPagination
    permission_classes = (AllowAny, )
    authentication_classes = (TokenAuthentication,)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    ordering_fields = ('id',)
    search_fields = ('category__title', 'title', 'description', 'meta')


class PostDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'
    queryset = models.Post.objects.all().order_by('-created_at')
    serializer_class = serializers.PostDetailUpdateDeleteSerializers
    permission_classes = (permissions.IsAdminOrUpdateOwnPost, )
    authentication_classes = (TokenAuthentication,)


class CategoryViewSets(viewsets.ModelViewSet):
    lookup_field = 'slug'
    permission_classes = (permissions.IsAdminUserOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializers


class PostListCategoryWise(PaginationFuctionForApiView,views.APIView):
    authentication_classes = (TokenAuthentication,)
    pagination_class = PostPageNumberPagination
    serializer_class = serializers.PostListSerializers

    def get(self, request, category_slug, format=None):
        queryset = models.Post.objects.filter(category__slug__exact=category_slug).order_by('-created_at')
        # if queryset.count() == 0:
        #     raise Http404
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


#################################################################--post-views-end--########################################################

########################################################-comment-views-start--#########################################################

class CommentsOfPost(PaginationFuctionForApiView, views.APIView):
    permission_classes = (AllowAny, )
    serializer_class = serializers.CommentDetailSerializer
    pagination_class = PostPageNumberPagination

    def get(self, request, post_pk, format=None):
        queryset = models.Comment.objects.filter(post=post_pk, parent=None).order_by('-created_at')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class CommentCreateAPIView(generics.CreateAPIView):
    # queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentCreateSerializer
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


########################################################--Comment-views-end--#########################################################

########################################################--contact-us-views-start--#########################################################

class ContactUsList(generics.ListAPIView):
    queryset = models.ContactUs.objects.all()
    serializer_class = serializers.ContactUsSerializers
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)
    pagination_class = PostPageNumberPagination


class ContactUsCreate(generics.CreateAPIView):
    queryset = models.ContactUs.objects.all()
    serializer_class = serializers.ContactUsSerializers
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    pagination_class = PostPageNumberPagination

#########################################################--contact-us-views-end--##############################################################