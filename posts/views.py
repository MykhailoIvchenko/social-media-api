from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from posts.models import Post
from posts.permissions import IsOwnerOrReadOnly
from posts.serializers import (
    PostSerializer,
    PostDetailsSerializer,
    PostImageSerializer
)


class PostViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = PostDetailsSerializer
    permission_classes = [IsOwnerOrReadOnly]

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        """Retrieve the posts with filters"""
        user = self.request.user
        queryset = Post.objects.filter(user=user)

        is_following = self.request.query_params.get(
            "is_following", "false").lower() == "true"
        hashtags = self.request.query_params.get("hashtags")

        if is_following:
            queryset = Post.objects.filter(user__in=user.following.all())

        if hashtags:
            hashtags_list = hashtags.split(",")
            queryset = queryset.filter(hashtags__name__in=hashtags_list)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return PostSerializer

        if self.action == "retrieve":
            return PostDetailsSerializer

        if self.action == "upload_image":
            return PostImageSerializer

        return PostDetailsSerializer

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
        permission_classes=[IsOwnerOrReadOnly],
    )
    def upload_image(self, request, pk=None):
        """Endpoint for uploading image to specific movie"""
        movie = self.get_object()
        serializer = self.get_serializer(movie, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "is_following",
                type={"type": "list", "items": {"type": "boolean"}},
                description="Retrieve posts of followed users",
            ),
            OpenApiParameter(
                "hashtags",
                type={"type": "list", "items": {"type": "str"}},
                description="Filter by hashtags",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
