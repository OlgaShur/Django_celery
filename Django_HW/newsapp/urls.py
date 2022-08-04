from django.urls import path
from .views import *

urlpatterns = [
    path('',PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post'),
    path('search', PostListSearch.as_view(), name='news-search'),
    path('create/', PostCreate.as_view(), name='news-create'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='news-update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='news-delete'),
    path('type/<str:type>', PostListType.as_view(), name='post-type'),
    path('category/<str:category>', CategoryList.as_view(), name='post_category'),
    path('type/<str:category>/subscribe', category_subscribe, name='post_category_subscribe'),

]
