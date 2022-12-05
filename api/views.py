from datetime import datetime
import email
from msilib.schema import SelfReg
from multiprocessing import AuthenticationError
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .models import SampleModel
from .models import SessionModel
from .serializers import SampleModelSerializer
from .models import UserModel
from .serializers import UserModelSerializer
from .serializers import SessionModelSerializer
from .models import RatingModel
from .serializers import RatingModelSerializer
import jwt
import datetime
import uuid
from django.conf import settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


# Learn more about django_rest_framework here:
# https://www.django-rest-framework.org/


# Create your views here.

# Sample API
@api_view(['GET'])
def getRoutes(request):

    routes = [
        {
            'Endpoint': '/teknoplat/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of teknoplat'
        },
        {
            'Endpoint': '/teknoplat/id',
            'method': 'GET',
            'body': None,
            'description': 'Returns a single session object'
        },
        {
            'Endpoint': '/teknoplat/create/',
            'method': 'POST',
            'body': {'body': ""},
            'description': 'Creates new session with data sent in post request'
        },
        {
            'Endpoint': '/teknoplat/id/update/',
            'method': 'PUT',
            'body': {'body': ""},
            'description': 'Creates an existing session with data sent in post request'
        },
        {
            'Endpoint': '/teknoplat/id/delete/',
            'method': 'DELETE',
            'body': None,
            'description': 'Deletes and exiting session'
        },
    ]

    return Response(routes)


@api_view(['GET'])
def getSampleModel(request):
    sampleModel = SampleModel.objects.all()
    serializer = SampleModelSerializer(sampleModel, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getUserModel(request):
    userModel = UserModel.objects.all()
    serializer = UserModelSerializer(userModel, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def addUserModel(request):
    serializeUser = UserModelSerializer(data=request.data)
    if serializeUser.is_valid():
        serializeUser.save()
        return Response(200)
    return Response(serializeUser.errors)


@api_view(['POST'])
def authUser(request):
    email = request.data['email']
    password = request.data['password']

    user = UserModel.objects.filter(email=email).first()

    if user is None:
        raise AuthenticationError("User not found")

    #if not user.password:
     #   raise AuthenticationError("Incorrect Password")

    payload = {
        'id': user.userID,
        'email': user.email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'iat': datetime.datetime.utcnow()
    }

    token = jwt.encode(payload, 'secret', algorithm='HS256')

    res = Response()

    res.set_cookie(key='jwt', value=token, httponly=True)

    res.data = {
        'jwt': token
    }

    return res


@api_view(['GET'])
def getAuthUser(request):
    token = request.COOKIES.get('jwt')
    print(token)

    if not token:
        raise AuthenticationError("Unauthenticated")

    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationError("Expired")

    user = UserModel.objects.filter(userID=payload['id']).first()
    serializer = UserModelSerializer(user)
    return Response(serializer.data)


@api_view(['POST'])
def logout(reqest):
    response = Response()
    response.delete_cookie('jwt')
    response.data = {
        'message': 'successfully logged out'
    }
    return response

# SessionModel


@api_view(['GET'])
def getAllSessionModel(request):
    sessionModel = SessionModel.objects.all()
    sessionSerializer = SessionModelSerializer(sessionModel, many=True)
    return Response(sessionSerializer.data)


@api_view(['GET'])
def getSessionModel(request, pk):
    sessionModel = SessionModel.objects.filter(searchID=pk)
    sessionSerializer = SessionModelSerializer(sessionModel, many=True)
    return Response(sessionSerializer.data)


@api_view(['POST'])
def setSessionModel(request):
    serializeUser = SessionModelSerializer(data=request.data)
    if serializeUser.is_valid():
        serializeUser.save()
        return Response()
    return Response(serializeUser.errors)


@api_view(['GET'])
def getRateModel(request):
    userModel = RatingModel.objects.all()
    serializer = RatingModelSerializer(userModel, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def addRateModel(request):
    serializeUser = RatingModelSerializer(data=request.data)
    if serializeUser.is_valid():
        serializeUser.save()
        return Response(200)
    return Response(serializeUser.errors)


@api_view(['GET'])
def get100MsKeys(request):
    keys = {
        'APP_KEY_100MS': settings.APP_KEY_100MS,
        'SECRET_KEY_100MS': settings.SECRET_KEY_100MS,
    }
    return Response(keys)


@api_view(['GET'])
def generateManagementToken(request):
    app_access_key = '6372de82a04fa8bc9163c888'
    app_secret = 'nH6grEk7yAMdjtvp3JEpSHDa0w95Iv_DkiC_ylkAmhM6xmx5TRkaIswO-TN1t-55uoRV5CqFavbvW3jzcM9yr8W81D009tMUYZR0JDVjAYt_BKwX2HDy1FFtuqCsS5dMg5DfmKOo8VrLMiFgmuiibnfHoCKjIXN_BrjXjzSHAto='
    expires = 24 * 3600
    now = datetime.datetime.utcnow()
    exp = now + datetime.timedelta(seconds=expires)

    management_token = jwt.encode(payload={
        'access_key': app_access_key,
        'type': 'management',
        'version': 2,
        'jti': str(uuid.uuid4()),
        'iat': now,
        'exp': exp,
        'nbf': now
    }, key=app_secret)

    return Response(management_token)
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, usermodel):
        token = super().get_token(usermodel)

        # Add custom claims
        token['username'] = usermodel.username
        token['first_name'] = usermodel.first_name
        token['last_name'] = usermodel.last_name
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
