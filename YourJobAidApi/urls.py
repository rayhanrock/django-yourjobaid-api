from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'YourJobAidApi'

router = DefaultRouter()
router.register('users', views.UserViewSets)
router.register('category', views.CategoryViewSets)
router.register('user-roles', views.UserRoleViewSets)


urlpatterns = [
    path('', include(router.urls)),

    path('login/', views.UserLoginApiView.as_view(), name='user-login'),
    path('update-user-roles/<int:pk>', views.UpdateUserRoleViewSets.as_view(), name = 'update-user-role'),

    path('<slug:category_slug>/posts/', views.PostListCategoryWise.as_view(), name='category-post-list'),
    path('posts/', views.PostListView.as_view(), name='category-post-list'),
    path('posts/create/', views.PostCreateView.as_view(), name='category-post-list'),
    path('posts/<slug:slug>/', views.PostDetailUpdateDeleteView.as_view(), name='category-post-list'),

    path('posts/comments/create/', views.CommentCreateAPIView.as_view(), name='create-post-comment'),
    path('comments/posts/<int:post_pk>/', views.CommentsOfPost.as_view(), name='post-comment'),


    path('contact-us/', views.ContactUsList.as_view(), name='contact-us'),
    path('contact-us/create/', views.ContactUsCreate.as_view(), name='create-contact-us'),

]
