from tkinter import image_names
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from studentpred.models import Ocr
from studentpred.form import *
import pytesseract
from PIL import Image
import numpy as np
import cv2


Marks={}
subjects=["ENGLISH","HINDI","URDU","HISTORY","GEOGRAPHY","POLITICAL" , "SCIENCE","SOCIOLOGY"]


def image_procesing(img_path):
    from PIL import Image, ImageEnhance
    
    print("processing......")
    img = cv2.imread(img_path)
    img = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
    # Apply blur to smooth out the edges
    #img = cv2.GaussianBlur(img, (5, 5), 0)
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    
    return img
    
pytesseract.pytesseract.tesseract_cmd ='C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
# Create your views here.
def home(request):
	form=StudentForm()
	return render(request, 'signin.html',{'form':form})
def signup(request):
	if request.method=="POST":
		form = StudentForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				username=form.cleaned_data['email']
				passw=form.cleaned_data['passw']
			
				print(Ocr.objects.filter(email=username))
				if Ocr.objects.filter(email=username).exists():
					
					message="Allready Exist Email"
					
				else:
					form.save()
					image = request.FILES['image']
					image = image.name
					path = settings.MEDIA_ROOT
					# image=Ocr.objects.all().last()
					# imagename=(image.image)
					# print(imagename)
					img_obj = form.instance
				
					imgchk=str(img_obj.image.url)
					
					imgname=imgchk.replace("/media","")
					
					pathz =str(path+imgname).replace("/","\\")
					
					
					
					# img = cv2.resize(img, (600, 360))
					cleanImage=image_procesing(pathz)
					
					# Adding custom options
					custom_config =r'--oem 3 --psm 6'
					# text = pytesseract.image_to_string((img), lang='eng',config=custom_config)
					data = pytesseract.image_to_string(cleanImage, lang='eng', config=custom_config)
					ocr=(data.split("\n"))
					for line in ocr:
						_list=line.split(" ")
						new_line=list(map(str.upper,_list))
						
						for words in new_line:
							if words in subjects:
								if new_line[-4]=="" or new_line[-4]==" "or new_line[-4]=="-" or new_line[-4]=="_"or new_line[-4]==",":
									Marks[words]=int(str(new_line[-3][1:]))
								else:
									Marks[words]=int(str(new_line[-4][1:]))
								
							
					x = sorted(Marks.items(),key=(lambda i: i[1]))
					second=(x[-2][0])
					first=(x[-1][0])
					print("highest scoring marks are ",first," : ",Marks[first]," AND ",second ," : ",Marks[second])
				
				return render(request, 'signin.html',{'form':form,'message':message})
			except Exception as e:
				print(e.message)
		else:
			print(form.errors)
	else:
		form=StudentForm()
	return render(request, 'signup.html',{'form':form})
	
def signin(request):
	if request.method=="POST":
		form = StudentForm(request.POST, request.FILES)
		try:
			username=request.POST['email']
			passw=request.POST['passw']
			print(username,passw)
				
			if Ocr.objects.filter(email=username,passw=passw).exists():
					
				print("sucess")
				return render(request, 'interest.html',{'form':form,"message_success":"success"})
			else:
				return render(request, 'signin.html',{'form':form,"message":"Credentials are Incorrect"})


		except Exception as e:
			print(e.message)
	else:
		form=StudentForm()
	return render(request, 'signin.html',{'form':form})