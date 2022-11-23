from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .logic.search_users import search_users
import csv


@api_view(['GET'])
def user_list(request):
    params = {
        "keyword": "",
        "location": "",
        "followers": "",
        "repos": "",
        "language": "",
    }
    for key in params:
        params[key] = request.query_params.get(key)
    
    data = search_users(params)

    response =  HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename = "user_info.csv"'

    writer = csv.writer(response, lineterminator='\n')
    writer.writerow([
        "Name", "Github Handle", "Bio", "Location", "Email", "Github Link"])
    writer.writerows(data)


    return response

