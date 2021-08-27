
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

from user_api.views import TeacherSearchView
from .views import PostViewSet, CourseViewSet, PostCommentsViewSet, PostSearchView, CourseSearchView

posts_router = routers.SimpleRouter()
posts_router.register(r'posts', PostViewSet, basename='post')

comments_router = routers.NestedSimpleRouter(posts_router, r'posts', lookup='post')
comments_router.register(r'comments', PostCommentsViewSet, basename='post-comments')

courses_router = SimpleRouter()
courses_router.register(r'courses', CourseViewSet, basename='course')

search_router = routers.DefaultRouter()
search_router.register("posts/search", PostSearchView, basename="post-search")
search_router.register("courses/search", CourseSearchView, basename="course-search")
search_router.register("teachers/search", TeacherSearchView, basename="teacher-search")
