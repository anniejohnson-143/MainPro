from django.shortcuts import render
from tensorflow.keras.models import load_model
import numpy as np
import tensorflow as tf
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.http import JsonResponse
from PIL import Image
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import cv2

model = load_model("C:/Users/fathi/Downloads/GAN for Anomaly detection/GAN for Anomaly detection/Git/model.h5")
class_dict = {0: "glioma_tumor", 1: "meningioma_tumor", 2: "no_tumor", 3: "pituitary_tumor"}
@login_required
def index(request):
    return render(request, 'main/index.html')
@login_required
def about(request):
    return render(request, 'main/about.html')
@login_required
def treatment(request):
    return render(request, 'main/treatment.html')

# def doctor(request):
#     return render(request, 'main/doctor.html')


def login_view(request):  # Renamed function
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(f"Received Username: {username}, Password: {password}")  # Debugging

        user = authenticate(username=username, password=password)
        print(f"Authenticated User: {user}")  # Debugging

        if user is not None and user.is_active:
            login(request, user)
            messages.success(request, '✅ Successfully Logged In')
            print("✅ Redirecting to home...")  # Debugging
            return redirect('index')  # ✅ Ensure 'home' exists in your URLs

        else:
            print('❌ Invalid credentials!')
            messages.error(request, "❌ Wrong credentials!")  # ✅ Proper messaging

    return render(request, 'main/login.html')  # ✅ Updated template reference

@login_required
def tumor_analysis(request):
    if request.method == "POST" and request.FILES.get("img"):
        image = request.FILES["img"]

        # Save the uploaded image
        fs = FileSystemStorage(location="media/uploads/")  # Store in 'media/uploads/'
        filename = fs.save(image.name, image)
        file_path = fs.path(filename)
        file_url = fs.url(f"uploads/{filename}")  # URL for accessing the image
        print(f'-------------------------------------{file_path}')
        # Process image

        test_img1 = cv2.imread(file_path)
        print("Done-------------------------------------------------------------------------------------------------------------------")
        test_img1 = np.expand_dims(test_img1, axis=0)
        pred = model.predict(test_img1)
        pred = np.argmax(pred)
        pred_class = class_dict[pred]


        # img = Image.open(image).convert("RGB")  # Convert to RGB
        # img = img.resize((224, 224))  # Resize to match model input
        # img = np.array(img) / 255.0  # Normalize pixel values
        # img = np.expand_dims(img, axis=0)  # Add batch dimension

        # # Make prediction
        # pred = model.predict(img)
        # predicted_class = np.argmax(pred)
        # predicted_label = class_dict.get(predicted_class, "Unknown")

        return render(request, 'main/result.html', {'img': file_url, 'pred' : pred_class, 'img' : file_url})

    return render(request, 'main/tumor_analysis.html')

@login_required
def result(request):
    return render(request, 'main/result.html')

def user_logout(request):
    logout(request)  # Logs out the user
    return redirect('login_view')
