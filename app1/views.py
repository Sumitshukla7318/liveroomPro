from django.shortcuts import render
from django.views import View
from django.conf import settings
from twilio.rest import Client
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import random
from app1.models import Profile,Contact
from django.views.decorators.csrf import csrf_exempt
import requests
import os

# Create your views here.

class Login_Phonenumber_view(View):
    def get(self,request):
        return render(request,"login.html")

class Details_view(View):
    def get(self,request):
        #if user doesn't exist render login page 
        if 'pkey' not in request.session:
            return render(request,"login.html")
        
        return render(request,"details.html")
    def post(self,request):
        pass
    
class Index_view(View):
    def get(self,request):
         
        #if user doesn't exist render login page 
        if 'pkey' not in request.session:
            return render(request,"login.html")
        
        pkey = request.session.get('pkey')
        data = Contact.objects.filter(reference = pkey).values()
        data = list(data)
        cnt = Contact.objects.filter(reference=pkey).values('contact')
        people = Profile.objects.all().values('phone')
        phn = [i['phone'] for i in people.values()]
        cnt = [i['contact'] for i in cnt.values()]
        # print(phn)
        # print('l----->',cnt)
        # print(f'c----->{people}')
        list1 = []
        for p in phn:
            if p in cnt:
                list1.append({'id':Contact.objects.get(contact=p).id, 'image': Profile.objects.get(phone=p).image})
            else:
                pass
                # list1.append({'id':Contact.objects.get(contact=p), 'image': ''})            
        print(list1)
        return render(request,"index.html",{'index': "msg",'data': data})
    
    def post(self,request):
        pass

class Status_view(View):
    def get(self,request):

        return render(request,"status.html")
    
class NewGroup_view(View):
    def get(self,request):
        data = {'first': 1,'second': 2,'third': 3,'four': 4,'five': 5}
        return render(request,"newgroup.html",{'contact': data})
    

class CreateGroup_view(View):
    def get(self,request):
        return render(request,"creategroup.html")
    
class Chat_Profile_view(View):
    def get(self,request):
        return render(request, "chat.html")
   
mobile = None

class Request_otp(View):
    def post(self,request):
        self.mobile_number = request.POST.get('mobile_number')
        # print(self.mobile_number)
        # otp = send_otp(mobile_number)
        otp=self.send_otp()
        # Save the OTP in session or database for later verification
        request.session['otp'] = otp
        global mobile
        mobile = self.mobile_number
        # return JsonResponse({'message': 'OTP sent successfully'}, status=200)
        return JsonResponse({'message': 'OTP sent successfully','otp': otp}, status=200)
    def get(self,request):
        return render(request,"login.html",status=200)
    def send_otp(self):
        try:
            # Twilio credentials
            # account_sid = 'your_account_sid'
            # auth_token = 'your_auth_token'
            #account_sid = settings.TWILIO_ACCOUNT_SID
            #auth_token = settings.TWILIO_AUTH_TOKEN
            #twilio_phone_number = settings.TWILIO_PHONE_NUMBER
            # client = Client(account_sid, auth_token)
            otp = random.randint(100000, 999999)
            print(otp)
            # message = f'Your OTP is {otp}'
            # msg = client.messages.create(
            #     body=message,
            #     from_=twilio_phone_number,
            #     to='+91'+self.mobile_number
            # )
            return otp
        except Exception as msg:
            print(msg)
            
class Check_otp(View):
    def post(self,request):
        try:
            otp = request.POST.get('otp')
            # print(otp)
            # print(request.session['otp'])
            if int(otp) == request.session['otp']:
                obj = Profile(phone = mobile)
                obj.save()
                request.session['pkey'] = obj.id
                del request.session['otp']
                print(f'primary key:- {obj.id}')
                return JsonResponse({'success':True},status=200) 
            else:
                return JsonResponse({'success':False},status=200)
        except:
            return JsonResponse({'success':False},status=404)

class Personal_Profile_view(View):
    def get(self,request):
        return render(request,"profile.html")
    
class Contact_list_view(View):
    def get(self,request):
        #if user doesn't exist render login page 
        if 'pkey' not in request.session:
            return render(request,"login.html")
        
        return render(request,"contact_list.html")
    
class Contact_save_view(View):
    def get(self, request, *args, **kwargs):
        #if user doesn't exist render login page 
        if 'pkey' not in request.session:
            return render(request,"login.html")
        pass
    def post(self, request):
        username = request.POST.get('username')
        contact = request.POST.get('contact')
        prevcontact = Contact.objects.all().values('contact')
        print(list(prevcontact))
        for p in prevcontact:
            if p['contact'] == contact:
                return JsonResponse({'msg':"Contact Already Exist..."},status=200)
        print(f'{contact} : {username}')
        # Validate and process the form data

        #checking the number that it is exist or not 
        if not self.isExist(contact):
            return JsonResponse({'msg':"Your provideed Mobie number is Invalid"})


        if username and contact and len(contact) == 10:
            # Save the data or perform some action
            try:
                pkey = request.session.get('pkey')
                obj1 = Profile.objects.get(id = pkey)
                obj2 = Contact(name=username, contact=contact, reference= obj1)
                obj2.save()
                print("contact saved")
                return JsonResponse({'msg': 'Contact saved successfully!'}, status=200)
            except Exception as e:
                print(f"Error: {e}")
                return JsonResponse({'msg': 'Something went wrong'}, status=400)       
        else:
            return JsonResponse({'msg': 'Invalid data provided.'}, status=400)
        
    import requests

    def isExist(self, contact, country_code=None):
        access_key = os.getenv('API_ACCESS_KEY')  # Load API key from environment variable
        api_url = 'http://apilayer.net/api/validate'

        # Prepare the parameters for the API request
        params = {
            'access_key': access_key,
            'number': contact,
            'format': 1  # Request the response in JSON format
        }
    
        # If a country code is provided, use it; otherwise, use the default 'IN'
        if country_code:
            params['country_code'] = country_code
        else:
            params['country_code'] = 'IN'  # Default country code if none is provided

        try:
        # Send GET request to the API
            response = requests.get(api_url, params=params)
    
        # If the API call is successful (status code 200)
            if response.status_code == 200:
                data = response.json()
    
                # Check if the number is valid and its line type is mobile
                if data.get('valid')==True and data.get('line_type') == 'mobile':
                    return True  # The number is valid and mobile
                else:
                    print(f"Error: {contact} is invalid or not a mobile number according to the API.")
                    return False  # The number is invalid or not a mobile number
            else:
                # Handle possible errors with the API request
                print(f"Error: API request failed with status code {response.status_code}")
                return False

        except Exception as e:
        # If there is any issue with making the API request
               print(f"Error occurred while validating phone number: {e}")
               return False
            
    
class Image_submit_view(View):
    def post(self,request):
        try:
            image = request.FILES['input-image']
            # Retrieve the existing object using the primary key from the session
            obj = Profile.objects.get(id=request.session['pkey'])            
            # Update the field(s) you want to modify
            obj.image = image  # Set the new image value
            # Save the changes to the database
            obj.save()
            print("Profile updated successfully!")
            return HttpResponseRedirect('/details/')
        except Profile.DoesNotExist:
            print("Profile with the given ID does not exist.")
            
class Name_submit_view(View):
    def post(self,request):
        try:
            name = request.POST.get('name')
            # Retrieve the existing object using the primary key from the session
            obj = Profile.objects.get(id=request.session['pkey'])
            # Update the field(s) you want to modify
            obj.name = name  # Set the new image value
            # Save the changes to the database
            obj.save()
            print("Profile updated successfully!")
            return JsonResponse({'redirect_url': '/','message': 'Name submitted successfully!'},status=200)
        except Profile.DoesNotExist:
            print("Profile with the given ID does not exist.")
    
class Settings_view(View):
    def get(self,request):
        return render(request,"settings.html")
    
# from .models import Contact 
class Contact_view(View):
    def get(self,request):
        contact = request.GET.get('contact')
        print("Say hii")
        print(contact)
        return JsonResponse({'msg':"Contact no. added successfully..."}, status=200)
    def post(self,request):
        print("POST confirm")
        return HttpResponse("kndkjhdkj")