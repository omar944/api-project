from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsAuthorized
from user_api.models import UserRating
from user_api.serializers import UserRatingSerializer


# noinspection PyMethodMayBeStatic
class UserRatingView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorized]
    serializer_class = UserRatingSerializer

    def get(self, request, pk):
        rate = UserRating.objects.filter(rated_user=pk)
        serializer = UserRatingSerializer(rate, many=True)
        av = rate.aggregate(Avg('rate'))
        return Response({"rates": serializer.data, "avg": av['rate__avg']}, status=status.HTTP_200_OK)

    def post(self, request, pk):
        data = request.data
        data['author'] = request.user.id
        data['rated_user'] = pk

        try:
            rate = UserRating.objects.get(rated_user=pk, author=request.user.id)
            return Response({"detail": "already rated by this user"}, status=status.HTTP_403_FORBIDDEN)
        except UserRating.DoesNotExist:
            pass

        serializer = UserRatingSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request, pk):
        data = get_object_or_404(UserRating, rated_user=pk, author=request.user.id)
        serializer = UserRatingSerializer(data, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        data = get_object_or_404(UserRating, rated_user=pk, author=request.user.id)
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyRatingView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserRatingSerializer

    # noinspection PyMethodMayBeStatic
    def get(self, request, pk):
        try:
            rate = UserRating.objects.get(rated_user=pk, author=request.user.id)
            return Response({'rate': rate.rate}, status=status.HTTP_200_OK)
        except UserRating.DoesNotExist:
            return Response({'rate': None}, status=status.HTTP_404_NOT_FOUND)
