from django.urls import path, include

from user_api.views import TeacherSearchView
from .routers import posts_router, courses_router, comments_router, search_router
from .views import GetTeachersView, UserRatingView, LikePost, MyRatingView, ViewedCourse

urlpatterns = [
    path('courses/view/<int:pk>', ViewedCourse.as_view()),
    path('', include(search_router.urls)),
    path('', include(courses_router.urls), name='get-delete-create-update-courses'),
    path('', include(posts_router.urls)),
    path('', include(comments_router.urls)),
    path('teachers', GetTeachersView.as_view(), name='get-teachers'),
    path('user/my-rate/<int:pk>', MyRatingView.as_view()),
    path('user/rate/<int:pk>', UserRatingView.as_view()),
    path('posts/<int:pk>/likes', LikePost.as_view()),
    path('search/', include('haystack.urls')),
]
