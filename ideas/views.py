from rest_framework.views import APIView, Response,status
from rest_framework.response import Response
from .models import Idea
from users.models import User
from .serializers import IdeaSerializerPost,IdeaSerializerGet,IdeaSerializerPut
import jwt
from my_idea_pool.settings import SECRET_KEY

import operator

class IdeaView(APIView):


    def get(self, request, format=None):
        access_token = request.META.get('HTTP_X_ACCESS_TOKEN')
        decoded = jwt.decode(access_token,SECRET_KEY)
        ideas = Idea.objects.filter(user_id=decoded['id'])
        try:
            page = int(self.request.query_params.get('page'))
            if page is None or page<0:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        ideas = sorted(ideas,key=operator.attrgetter('average_score'),reverse=True )[(page-1)*10:page*10]
        serilazer = IdeaSerializerGet(ideas,many=True)
        return Response(serilazer.data)

    def post(self, request, format=None ): 
      
      
        access_token = request.META.get('HTTP_X_ACCESS_TOKEN')
        decoded = jwt.decode(access_token,SECRET_KEY)
        data=request.data.copy()
        data['user_id'] = decoded['id']
        serializer = IdeaSerializerPost(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def put(self, request, pk, format=None):
        idea = Idea.objects.get(id=pk)
        idea.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    def put(self, request, pk, format=None):
        idea = Idea.objects.get(id=pk)
        serializer = IdeaSerializerPut(idea, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        idea = Idea.objects.get(id=pk)
        idea.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)