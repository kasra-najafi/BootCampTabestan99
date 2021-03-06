from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.authentication import BaseAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from cinema.models import Movie, Cinema, Salon
from .serializers import MovieSerializer, SalonSerializer, CinemaSerializer, TempSalonSerializer, CommentSerializer, ArticleSerializer, AuthorSerializer
from blog.models import Comment, Author, Article
from .permissions import IsOwnerOrReadOnly


class MovieView(APIView):

    def get(self, request, format=None):
        print(request.content_type)
        movies = Movie.objects.all()
        movie_serialized = MovieSerializer(movies, many=True)
        return Response(movie_serialized.data)


# class SalonView(viewsets.ModelViewSet):
#     queryset = Salon.objects.all()
#     serializer_class = SalonSerializer


# class CinemaView(viewsets.ModelViewSet):
#     queryset = Cinema.objects.all().order_by('name')
#     serializer_class = CinemaSerializer


class SalonList(APIView):
    def get(self, request):
        salons = Salon.objects.all()
        salon_serialized = TempSalonSerializer(salons, many=True)
        # salon_serialized = SalonSerializer(salons, many=True)
        return Response(salon_serialized.data)


class SalonDetail(APIView):
    def get(self, request, pk):
        try:
            salon = Salon.objects.get(pk=pk)
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serialized_salon = SalonSerializer(salon)
        return Response(serialized_salon.data)

    # def put(self, request, pk):
    #     try:
    #         salon = Salon.objects.get(pk=pk)
    #     except Exception as e:
    #         return Response(status=status.HTTP_404_NOT_FOUND)

    #     salon.name = request.data['name']
    #     salon.capacity = request.data['capacity']

    #     salon.save()

    def put(self, request, pk):
        try:
            salon = Salon.objects.get(pk=pk)
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serialized_salon = SalonSerializer(salon, data=request.data)
        if serialized_salon.is_valid():
            serialized_salon.save()
            return Response(serialized_salon.data)
        return Response(serialized_salon.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class ArticleList(generics.ListCreateAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


@api_view(['GET', 'POST'])
def hello(request):
    print(request)
    return HttpResponse('Hello')
