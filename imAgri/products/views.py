from django.shortcuts import render
import hashlib
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Organization, Products
import json
import jwt
from datetime import datetime, timedelta
from functools import wraps

def validate_access_token(view_func):
    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        # Get the access token from the request headers
        authorization_header = request.META.get('HTTP_AUTHORIZATION')
        if authorization_header is None:
            return JsonResponse({'error': 'Authorization header is missing'}, status=401)

        try:
            token = authorization_header.split(' ')[1]

            # Decode the access token
            payload = jwt.decode(token, 'your_secret_key', algorithms=['HS256'])
            expiry = datetime.strptime(payload['expiry'], '%Y-%m-%d %H:%M:%S')
            user_id = payload.get('user_id')
            # Check if the token has expired
            if expiry < datetime.now():
                return JsonResponse({'error': 'Token has expired'}, status=401)

            # Call the actual view function
            return view_func(self, request, *args, **kwargs, user_id=user_id)
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Token has expired'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Invalid token'}, status=401)

    return wrapper
    
@method_decorator(csrf_exempt, name='dispatch')
class registerOrganization(View):
    def get(self,request): 
        return render(request, 'register.html') 
    
    def post(self, request):
        data = json.loads(request.body)

            # Extract data fields
        name = data.get('name')
        address = data.get('address')
        email = data.get('email')
        phone_number = data.get('phone_number')
        website = data.get('website')
        location = data.get('location')
        password = data.get('password')
        print(data)

        # Hash the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        try:
            # Create and save organization
            organization = Organization.objects.create(
                name=name,
                address=address,
                email=email,
                phone_number=phone_number,
                website=website,
                location=location,
                password=hashed_password
            )
            return JsonResponse({'message': 'Organization registered successfully'}, status=201)
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')      
class LoginOrganization(View):
    def get(self,request): 
        return render(request, 'login.html') 
    
    def post(self, request):
        try:
            # Parse JSON data from request body
            print("hereerererer")
            data = json.loads(request.body)
            print(data)

            # Extract email and password from JSON data
            email = data.get('email')
            password = data.get('password')

            # Get organization with the provided email
            organization = Organization.objects.get(email=email)
            print(organization)

            # Hash the provided password
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            # Check if the hashed password matches the stored password
            if organization.password == hashed_password:
                access_token = generate_access_token(organization.id, organization.name)

                return JsonResponse({'message': 'Login successful', 'token': access_token, 'user': organization.id}, status=200)
            else:
                return JsonResponse({'error': 'Invalid email or password'}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Organization.DoesNotExist:
            return JsonResponse({'error': 'Organization with this email does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
@method_decorator(csrf_exempt, name='dispatch') 
class addProducts(View):
    # @validate_access_token
    def get(self,request): 
        diseases = ['Gray Leaf Spot on Corn',
        'Common rust Corn',
        'Northern Corn Leaf Blight',
        'Tomato Bacterial Spot',
        'Early Blight',
        'Late Blight']
        return render(request, 'add-product.html', {'diseases': diseases}) 
    
    @validate_access_token
    def post(self, request, user_id):
        try:
            # Parse JSON data from request body
            data = json.loads(request.body)
            print(data)

            # Extract email and password from JSON data
            disease_name = data.get('disease')
            name = data.get('name')
            product_link = data.get('link')

            # Get organization with the provided email
            product = Products.objects.create(
                product=name,
                disease_name=disease_name,
                product_link=product_link,
                org_id=user_id
            )

            
            return JsonResponse({'message': 'Product added successfully' }, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)
        



def generate_access_token(user_id, username):
    # Set expiry to 7 days
    expiry = datetime.now() + timedelta(days=7)

    # Payload for JWT token
    payload = {
        'user_id': user_id,
        'username': username,
        'expiry': expiry.strftime('%Y-%m-%d %H:%M:%S')
    }

    # Generate JWT token
    token = jwt.encode(payload, 'your_secret_key', algorithm='HS256')
    return token

