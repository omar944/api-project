from django.http import HttpResponse
from django.http import HttpResponse
from drf_haystack.viewsets import HaystackViewSet
from rest_framework import generics
from rest_framework.decorators import api_view

from .models import User
from .serializers import UserDetailsSerializer, TeacherSearchSerializer


class GetUserView(generics.RetrieveAPIView):
    serializer_class = UserDetailsSerializer
    queryset = User.objects.all()


class TeacherSearchView(HaystackViewSet):
    # `index_models` is an optional list of which models you would like to include
    # in the search result. You might have several models indexed, and this provides
    # a way to filter out those of no interest for this particular view.
    # (Translates to `SearchQuerySet().models(*index_models)` behind the scenes.
    index_models = [User]

    serializer_class = TeacherSearchSerializer


def email_verified(request):
    html = "<html><body> <h1>email verified</h1></body></html>"
    return HttpResponse(html)