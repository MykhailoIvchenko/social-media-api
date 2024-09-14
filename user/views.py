from rest_framework import viewsets, status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .models import User
from user.permissions import IsOwnerOrReadOnly
from .serializers import UserProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().prefetch_related('following', 'followers')
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = User.objects.all().prefetch_related('following', 'followers')
        email = self.request.query_params.get("email", None)
        if email:
            queryset = queryset.filter(email__icontains=email)
        return queryset


class UserFollowViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def follow(self, request, pk=None):
        user_to_follow = self.get_object(pk)
        if request.user == user_to_follow:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        request.user.following.add(user_to_follow)
        return Response({"detail": "You are now following this user."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def unfollow(self, request, pk=None):
        user_to_unfollow = self.get_object(pk)
        if request.user == user_to_unfollow:
            return Response({"detail": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        if user_to_unfollow not in request.user.following.all():
            return Response({"detail": "You are not following this user."}, status=status.HTTP_400_BAD_REQUEST)
        request.user.following.remove(user_to_unfollow)
        return Response({"detail": "You have unfollowed this user."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def following(self, request):
        users_following = request.user.following.all().prefetch_related('following', 'followers')
        serializer = UserProfileSerializer(users_following, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def followers(self, request):
        followers = request.user.followers.all().prefetch_related('following', 'followers')
        serializer = UserProfileSerializer(followers, many=True)
        return Response(serializer.data)

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserProfileSerializer


@api_view(['POST'])
def logout(request):
    try:
        refresh_token = request.data.get("refresh", None)
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)