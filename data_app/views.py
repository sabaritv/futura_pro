import os

from cryptography.fernet import Fernet
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.
from data_app.forms import LoginRegister, OwnerRegister, ReceiverRegister, UploadForm
from data_app.models import Uploads

@login_required(login_url='login_view')
def index(request):
    return render(request, 'admintemp/adminbase.html')

@login_required(login_url='login_view')
def home(request):
    return render(request, 'home.html')



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('index')
            elif user.is_receiver:
                return redirect('receiver')
            elif user.is_owner:
                return redirect('owner')
            elif user.is_authority:
                return redirect('home')
        # else:
        #     messages.info(request, 'Invalid Credentials')
    return render(request, 'login.html')



def data_owner_register(request):
    login_form = LoginRegister()
    owner_form = OwnerRegister()
    if request.method == 'POST':
        login_form = LoginRegister(request.POST)
        owner_form = OwnerRegister(request.POST)
        if login_form.is_valid() and owner_form.is_valid():
            l = login_form.save(commit=False)
            l.is_owner = True
            l.save()
            owner = owner_form.save(commit=False)
            owner.User = l
            owner.save()
            messages.info(request, 'data owner registered successfully')
            return redirect('login_view')
    return render(request,'ownertemp/owner_reg.html', {'login_form': login_form, 'owner_form': owner_form})


def data_receiver_register(request):
    login_form = LoginRegister()
    receiver_form = ReceiverRegister()
    if request.method == 'POST':
        login_form = LoginRegister(request.POST)
        receiver_form = ReceiverRegister(request.POST)
        if login_form.is_valid() and receiver_form.is_valid():
            User = login_form.save(commit=False)
            User.is_receiver = True
            User.save()
            receiver = receiver_form.save(commit=False)
            receiver.User = User
            receiver.save()
            messages.info(request, 'datareceiver registered successfully')
            return redirect('login_view')
    return render(request, 'receivertmp/receiver_reg.html',{'login_form': login_form, 'receiver_form': receiver_form})

@login_required(login_url='login_view')
def receiver(request):
    return render(request,"receivertmp/receiverbase.html")


@login_required(login_url='login_view')
def owner(request):
    return render(request,"ownertemp/ownerbase.html")


def model_form_upload(request):
    form = UploadForm
    u = request.user
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = u
            obj.save()

            return redirect('owner')
    else:
             form = UploadForm()
    return render(request, 'ownertemp/upload_owner.html', {'form': form})

def doc_views(request):
    uploads = Uploads.objects.all()
    return render(request,'admintemp/admin_data_view.html',{'uploads':uploads})

def logout_view(request):
    logout(request)
    return redirect('login_view')


# def upload_files_owner(request):
#     form = UploadForm()
#     if request.method == 'POST':
#         form = UploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             file = form.save(commit=False)
#             file.User = request.user
#             file.Files = request.FILES['Files']
#             file_type = file.Files.url.split('.')[-1]
#             file_type.lower()
#             directory = os.getcwd()
#             file_name = directory + file.Files.url
#             # for instance in Upload.objects.all():
#             #     if instance.Files:
#             #         directory = os.getcwd()
#             #         file_name = directory+file.Files.url
#             file.save()
#
#             class Encryptor():
#
#                 def create_key(self):
#                     key = Fernet.generate_key()
#                     return key
#
#                 def write_key(self, key, key_name):
#                     with open(key_name, 'wb') as mykey:
#                         mykey.write(key)
#
#                 def load_key(self, key_name):
#                     with open(key_name, 'rb') as mykey:
#                         key = mykey.read()
#                     return key
#
#                 def encrypt_file(self, key, original_file, encrypted_file):
#                     f = Fernet(key)
#
#                     with open(original_file, 'rb') as files:
#                         original = files.read()
#
#                     encrypted = f.encrypt(original)
#
#                     with open(encrypted_file, 'wb') as files:
#                         files.write(encrypted)
#
#                 def decrypt_file(self, key, encrypted_file, decrypted_file):
#                     f = Fernet(key)
#
#                     with open(encrypted_file, 'rb') as files:
#                         encrypted = files.read()
#
#                     decrypted = f.decrypt(encrypted)
#
#                     with open(decrypted_file, 'wb') as files:
#                         files.write(decrypted)
#
#             encryptor = Encryptor()
#
#             mykey = encryptor.create_key()
#
#             encryptor.write_key(mykey, 'key.key')
#
#             loaded_key = encryptor.load_key('key.key')
#
#             encryptor.encrypt_file(loaded_key, file_name, file_name + 'enc_')
#
#             encryptor.decrypt_file(loaded_key, file_name + 'enc_', file_name + 'dec_')
#
#             return render(request, 'owner/confirm_upload.html', {'file': file})
#
#     context = {"form": form, }
#     return render(request, 'owner/upload_owner.html', context)

