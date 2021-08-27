from django.db.models import Count, Q
from rest_framework import generics, filters

from user_api.models import User
from user_api.serializers import TeacherSerializer


class GetTeachersView(generics.ListAPIView):
    serializer_class = TeacherSerializer
    queryset = User.objects.annotate(courses_num=Count('courses'), skills_num=Count('skills'))\
        .filter(Q(courses_num__gt=0) | Q(skills_num__gt=0))


# Allows user to select fields to search by...
class DynamicSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        return request.GET.getlist('search_fields', [])

    """
        add ^ to search query to search for matches starting with pattern
        add @ for exact match search
    """
