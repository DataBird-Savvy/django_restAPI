from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import People
from .serializer import PeopleSerializer,RegisterSerializer,LoginSerializer
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet,ModelViewSet
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator

class CustomPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

class RegisterAPI(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.save()
            return Response(user_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginAPI(APIView):
    permission_classes=[]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            token,_ = Token.objects.get_or_create(user=user)
            if user is not None:
                return Response({'message': 'Login successful','token':token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
     
class PeopleAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    
    
    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [AllowAny()]  
    #     return [IsAuthenticated()] 
    def get(self, request):
        people = People.objects.all()
        page=self.request.GET.get('page',1)
        page_size=5
        paginator=Paginator(people,page_size)
        serializer=PeopleSerializer(paginator.page(page), many=True)
        # serializer = PeopleSerializer(people, many=True)
        if serializer.data:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors)
    
    def post(self, request):
        serializer = PeopleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request):
        try:
            person = People.objects.get(id=request.data.get('id'))
        except People.DoesNotExist:
            return Response({'error': 'Person not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PeopleSerializer(person, data=request.data,partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    
    def patch(self, request):
        try:
            person = People.objects.get(id=request.data.get('id'))
        except People.DoesNotExist:
            return Response({'error': 'Person not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PeopleSerializer(person, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
    
 
    
    





@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def people_api(request):
    
    # ---------------- GET ----------------
    if request.method == 'GET':
        people = People.objects.filter(team__isnull=False)
        serializer = PeopleSerializer(people, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # ---------------- POST ----------------
    elif request.method == 'POST':
        serializer = PeopleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ---------------- PUT ----------------
    elif request.method == 'PUT':
        try:
            person = People.objects.get(id=request.data.get('id'))
        except People.DoesNotExist:
            return Response({'error': 'Person not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PeopleSerializer(person, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ---------------- PATCH ----------------
    elif request.method == 'PATCH':
        try:
            person = People.objects.get(id=request.data.get('id'))
        except People.DoesNotExist:
            return Response({'error': 'Person not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PeopleSerializer(person, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ---------------- DELETE ----------------
    elif request.method == 'DELETE':
        try:
            person = People.objects.get(id=request.data.get('id'))
        except People.DoesNotExist:
            return Response({'error': 'Person not found'}, status=status.HTTP_404_NOT_FOUND)
        
        person.delete()
        return Response({'message': 'Person deleted successfully'}, status=status.HTTP_200_OK)

class PersonViewSet(ModelViewSet):
    queryset = People.objects.all()
    serializer_class = PeopleSerializer
    pagination_class = CustomPagination
    
    # def get_permissions(self):
    #     if self.action == 'list' or self.action == 'retrieve':  
    #         return [AllowAny()]
    #     return [IsAuthenticated()] 
    
    def list(self,request):
        search=request.GET.get('search',None)
        if search:
   
            queryset=self.queryset.filter(name__istartswith=search)
        else:
            queryset=self.queryset.all()
        pagenated_queryset=self.paginate_queryset(queryset)
        if pagenated_queryset is not None:
            serializer=self.serializer_class(pagenated_queryset,many=True)
            return self.get_paginated_response(serializer.data)
        serializer=self.serializer_class(queryset,many=True)
        return self.get_paginated_response({'status' :200,'data': serializer.data})
    