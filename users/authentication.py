from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.six import text_type
from rest_framework import HTTP_HEADER_ENCODING
class MyJWTAuthentication(JWTAuthentication):
  

    def get_header(self, request):
        """
        Extracts the header containing the JSON web token from the given
        request.
        """
        header = request.META.get('HTTP_X_ACCESS_TOKEN')
        if isinstance(header, text_type):
            # Work around django test client oddness
            header = header.encode(HTTP_HEADER_ENCODING)

        return header

    def get_raw_token(self, header):
        return header