# Django imports
# REST Framework imports
from drf_haystack.viewsets import HaystackViewSet
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, extend_schema_view
from rest_framework import viewsets, status, views
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

# App imports
from api.models import Post, Comment
from api.models.post import Like
from api.permissions import IsAuthorized
from api.serializers.PostSerializers import PostReadSerializer, PostWriteSerializer, CommentSerializer, LikeSerializer, \
    PostSearchSerializer
from api.views.views import DynamicSearchFilter


# noinspection PyMethodMayBeStatic
class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorized]
    filter_backends = (DynamicSearchFilter,)
    queryset = Post.objects.none()

    def get_queryset(self):
        return Post.objects.all()
        # if self.action in ["create", "update", "partial_update", "destroy"]:
        #     return Post.objects.all()
        # return Post.post_comments_likes.all()

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return PostWriteSerializer
        return PostReadSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# noinspection PyMethodMayBeStatic
@extend_schema_view(
    list=extend_schema(parameters=[OpenApiParameter("post_pk", OpenApiTypes.UUID, OpenApiParameter.PATH)]),
    retrieve=extend_schema(parameters=[OpenApiParameter("post_pk", OpenApiTypes.UUID, OpenApiParameter.PATH)]),
    create=extend_schema(parameters=[OpenApiParameter("post_pk", OpenApiTypes.UUID, OpenApiParameter.PATH)]),
    update=extend_schema(parameters=[OpenApiParameter("post_pk", OpenApiTypes.UUID, OpenApiParameter.PATH)]),
    partial_update=extend_schema(parameters=[OpenApiParameter("post_pk", OpenApiTypes.UUID, OpenApiParameter.PATH)]),
    destroy=extend_schema(parameters=[OpenApiParameter("post_pk", OpenApiTypes.UUID, OpenApiParameter.PATH)]),
)
class PostCommentsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorized]
    serializer_class = CommentSerializer
    queryset = Comment.objects.none()

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_pk'])

    def create(self, request, *args, **kwargs):
        request.data['post_id'] = kwargs.get('post_pk')
        request.data['author'] = request.user.id
        return super().create(request, *args, **kwargs)


# noinspection PyMethodMayBeStatic
class LikePost(views.APIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorized]

    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        serializer = LikeSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        try:
            like = Like.objects.get(author=request.user.id, post_id=pk)
            return Response(status=status.HTTP_403_FORBIDDEN)
        except Like.DoesNotExist:
            pass
        opj = Like.objects.create(post_id=Post.objects.get(pk=pk), author=request.user)
        opj.save()
        # check
        return Response({"likes": Like.objects.filter(post_id=pk).count()}, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        user = request.user.id
        try:
            like = Like.objects.get(author=user, post_id=pk)
            like.delete()
            return Response({"likes": Like.objects.filter(post_id=pk).count()}, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN)


class PostSearchView(HaystackViewSet):
    index_models = [Post]
    serializer_class = PostSearchSerializer





