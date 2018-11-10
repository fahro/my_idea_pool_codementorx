from rest_framework.views import APIView, Response,status
from rest_framework.response import Response
from .models import Idea
from users.models import User
from .serializers import IdeaSerializerPost,IdeaSerializerGet,IdeaSerializerPut
import jwt
from my_idea_pool.settings import SECRET_KEY

from django.shortcuts import  get_object_or_404
import operator

class IdeaView(APIView):


    def get(self, request, format=None):
        access_token = request.META.get('HTTP_X_ACCESS_TOKEN')
        decoded = jwt.decode(access_token,SECRET_KEY)
        ideas = Idea.objects.filter(user_id=decoded['id'])
        try:
            page = self.request.query_params.get('page')
            if page is None:
                page=0
            elif int(page)<0:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                page=int(page)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        ideas = sorted(ideas,key=operator.attrgetter('average_score'),reverse=True )[(page-1)*10:page*10]
        serilazer = IdeaSerializerGet(ideas,many=True)
        print(serilazer.data)
        return Response(serilazer.data)

    def post(self, request, format=None ): 
        access_token = request.META.get('HTTP_X_ACCESS_TOKEN')
        decoded = jwt.decode(access_token,SECRET_KEY)
        data=request.data.copy()
        data['user_id'] = decoded['id']
        serializer = IdeaSerializerPost(data=data)
        serializer.is_valid(raise_exception=True)
        idea = serializer.save()
        serializer = IdeaSerializerGet(idea)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



    def put(self, request, pk, format=None):
        access_token = request.META.get('HTTP_X_ACCESS_TOKEN')
        decoded = jwt.decode(access_token,SECRET_KEY)
        idea = get_object_or_404(Idea,pk=pk,user_id=decoded['id'])
        serializer = IdeaSerializerPut(idea, data=request.data)
        if serializer.is_valid():
            idea = serializer.save()
            serializer = IdeaSerializerGet(idea)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        access_token = request.META.get('HTTP_X_ACCESS_TOKEN')
        decoded = jwt.decode(access_token,SECRET_KEY)
        idea = get_object_or_404(Idea,pk=pk,user_id=decoded['id'])
        idea.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)