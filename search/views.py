from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .logic.search_users import *
import time
import csv


@api_view(['GET'])
def user_list(request):
    start = time.time()

    params = {
        "keyword": "",
        "location": "",
        "followers": "",
        "repos": "",
        "language": "",
    }
    for key in params:
        params[key] = request.query_params.get(key)

    query = create_query(params)
    if not query:
        return Response({"Error": "Insufficient parameters"}, status=status.HTTP_400_BAD_REQUEST)

    user_list, user_count = get_user_list(query)

    if user_count == 0:
        return Response({"Result: 0 Users Found"}, status=status.HTTP_200_OK)
    elif user_count == -1:
        return Response({"Error": "github api link broken"}, status=status.HTTP_404_NOT_FOUND)

    user_urls = fill_queue_and_list(user_list)

    user_info = multi_threading(user_urls)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename = "user_info.csv"'

    writer = csv.writer(response, lineterminator='\n')
    writer.writerow([
        "Name", "Github Handle", "Bio", "Location", "Email", "Github Link"])
    writer.writerows(user_info)

    print(f'Time Taken: {time.time() - start} seconds')  
    return response
