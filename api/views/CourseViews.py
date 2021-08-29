from drf_haystack.viewsets import HaystackViewSet
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from api.models.course import Course, ViewedCourses
from api.permissions import IsAuthorized
from api.serializers.CourseSerializers import CourseSerializer, CourseSearchSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsAuthorized]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # noinspection PyMethodMayBeStatic
    def jaccard_similarity(self, s1, s2):
        intersection = len(list(s1.intersection(s2)))
        union = (len(list(s1)) + len(list(s2)) - intersection)
        if int(union) == 0:
            return 0
        return float(intersection) / union

    def list(self, *args, **kwargs):
        user = self.request.user
        viewed = ViewedCourses.objects.filter(author=user)
        if len(viewed) == 0:
            return super().list(*args, **kwargs)
        user_tags = set()
        viewed_ids = set()
        for i in viewed:
            viewed_ids.add(i.id)
            for tag in i.course.tags.all():
                user_tags.add(tag.name)

        data = Course.objects.all()
        courses_scores = dict()
        for i in data:
            current_tags = set()
            for tag in i.tags.all():
                current_tags.add(tag.name)
            idx = self.jaccard_similarity(user_tags, current_tags)
            courses_scores[i.id] = idx
            if i.id in viewed_ids:
                courses_scores[i.id] = max(courses_scores[i.id] - 0.40, 0.15)

        serializer = self.get_serializer(data, many=True)
        result = list()
        for d in serializer.data:
            result.append(dict(d))

        result = sorted(result, key=lambda k: courses_scores[k['id']])
        result.reverse()
        return Response(result)


class CourseSearchView(HaystackViewSet):
    index_models = [Course]

    serializer_class = CourseSearchSerializer


class ViewedCourse(APIView):
    permission_classes = [IsAuthenticated]

    # noinspection PyMethodMayBeStatic
    def post(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response({'no such course'}, status=status.HTTP_403_FORBIDDEN)
        ViewedCourses.objects.get_or_create(author=request.user, course=course)
        return Response(status=status.HTTP_200_OK)
