from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello this is the Fintrack API site, this page is not use for anything. The API service"
                        "can be accessed through api/v1/")
