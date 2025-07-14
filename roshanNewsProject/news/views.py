from django.core.serializers import serialize
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import NewsSerializer
from rest_framework import status
from .models import News, Tag
from django.db.models import Q

# Create your views here.
@api_view(["POST"])
def insert_news(request):
    serializer = NewsSerializer(data=request.data)
    print(request.data)
    tags = request.data['tags']
    for tag in tags:
        if not Tag.objects.filter(name=tag):
            new_tag = Tag.objects.create(name=tag)
            new_tag.save()
    if News.objects.filter(title=request.data['title']):
        return Response({"error": "خبر تکراری است!"}, status=status.HTTP_400_BAD_REQUEST)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def all_news(request):
    news = News.objects.all()
    tags = request.query_params.getlist('tags')
    print(tags)
    if tags:
        news = news.filter(tags__name__in=tags).distinct()
    keyword = request.query_params.get('keyword')
    if keyword:
        news = news.filter(Q(title__icontains=keyword) | Q(content_news__icontains=keyword)).distinct()
    exclude_keyword = request.query_params.get('exclude_keyword')
    if exclude_keyword:
        news = news.exclude(content_news__icontains=exclude_keyword).distinct()

    serializer = NewsSerializer(news, many=True)
    return Response(serializer.data)

@api_view(["DELETE"])
def delete_news(request):
    try:
        news = News.objects.all()
        for n in news:
            n.delete()
        tags = Tag.objects.all()
        for t in tags:
            t.delete()
        return Response({"message": "خبر با موفقیت حذف شد."}, status=status.HTTP_204_NO_CONTENT)
    except News.DoesNotExist:
        return Response({"error": "خبر پیدا نشد!"}, status=status.HTTP_404_NOT_FOUND)