import requests
import traceback
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions


class MotivationalQuoteView(APIView):
    """
    Searches for a motivational quote from Quotable API
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        quotable_api_url = 'https://api.quotable.io'
        quotable_route = '/quotes/random'
        url = f'{quotable_api_url}{quotable_route}'
        
        try:
            api_response = requests.get(
                url=url,
                timeout=10,
                verify=False) # This line was necessary because the API was not returning a valid SSL certificate at the time of development

            data = api_response.json()[0]

            formatted_response = {
                "quote": data['content'],
                "author": data['author']
            }
            return Response(data=formatted_response, status=status.HTTP_200_OK)
        except Exception as err:
            traceback.print_exc()
            err_msg = {
                "details": f"An error occurred while fetching"
                f"motivational quote: {str(err)}",
                "status": 500
            }
            return Response(
                data=err_msg,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
