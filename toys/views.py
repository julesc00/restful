from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.db import connection

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
def toy_sql_view(request):
    if request.method == "GET":
        toys = Toy.objects.raw("""SELECT * FROM toys_toy""")
        toys_serializer = ToySerializer(toys, many=True)
        return JSONResponse(toys_serializer.data)


def toy_aggregate_view(request):
    try:
        with connection.cursor() as cursor:
            toys_count = cursor.execute("""SELECT COUNT(*) FROM toys_toy""")
            return JSONResponse(toys_count)
    except ConnectionError:
        return JSONResponse({"message": "Something's wrong"})


@csrf_exempt
def toy_raw_sql_view(request):
    """
    The response appears as a list of lists.

    [
    [
        2,
        "Barbie perrea",
        "Barbie shaking that skinny ass.",
        "Hot girl figures",
        "2022-02-16T11:37:39.654136",
        true,
        "2022-02-16T11:37:39.654207"
    ],
    [
        3,
        "Woody the Astronaut",
        "Woody as a galactic astronaut.",
        "Super Heroes",
        "2022-02-16T16:05:08.383561",
        false,
        "2022-02-16T16:05:08.383625"
    ]
]
    """
    if request.method == "GET":
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM toys_toy")
                toy_rows = cursor.fetchall()
                # toys_serializer = ToySerializer(toy_rows, many=True)
                return JSONResponse(toy_rows)
        except ConnectionError:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


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
