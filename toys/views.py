from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from toys.models import Toy
from toys.serializers import ToySerializer

"""
Function-based Non-abstract approach
"""


class JSONResponse(HttpResponse):
    def __init__(self, data, *args, **kwargs):
        content = JSONRenderer().render(data)
        kwargs["content_type"] = "application/json"
        super(JSONResponse, self).__init__(content, *args, **kwargs)


@csrf_exempt
def toy_list_view(request):
    if request.method == "GET":
        toys = Toy.objects.all()
        toys_serializer = ToySerializer(toys, many=True)
        print(toys_serializer.data)
        return JSONResponse(toys_serializer.data)


@csrf_exempt
def toy_detail_view(request, pk):
    try:
        toy = Toy.objects.filter(pk=pk).first()
    except Toy.DoesNotExist:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    if request.method == "GET":
        toy_serializer = ToySerializer(toy)
        return JSONResponse(toy_serializer.data)
    elif request.method == "PUT":
        toy_data = JSONParser().parse(request)
        toy_serializer = ToySerializer(toy, data=toy_data)
        if toy_serializer.is_valid():
            toy_serializer.save()
            return JSONResponse(toy_serializer.data)
        return JSONResponse(toy_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        toy.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
