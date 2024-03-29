from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Image
from .forms import UploadImageForm, ImageUpload 
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import cv2
import tensorflow as tf

ANSWER = -1
FORM = None
CATEGORIES = ["Fire", "No_Fire"]


def prepare(filepath):
    IMG_SIZE = 70  # 50 in txt-based
    img_array = cv2.imread(filepath)
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 3)

# Create your views here.
def index(request):
	global ANSWER
	ANSWER = -1
	path = './media/images/'
	for file in os.listdir(path):
		os.remove(path + file)
	qset = ImageUpload.objects.all()
	if len(qset) > 0:
		for obj in qset:
			obj.delete()
	return render(request, 'main.html', {'answer': ANSWER})

def handle_uploaded_file(f):
	# process ML model and receive output
	global ANSWER
	model = tf.keras.models.load_model("./main/CNN.model")

	img = './media/images/' + str(f)

	f = open("output.txt", "w")
	f.write("The file \"" + str(f) + "\" outputs:\n")

	prediction = model.predict([prepare(img)])
	print(prediction)  # will be a list in a list.
	if(CATEGORIES[int(prediction[0][0])] == 'Fire'):
		f.write("This is a fire. RUN!")
		ANSWER = 1
	else:
		f.write("No fire, ya good!")
		ANSWER = 0
	f.close()


# ALL IMAGES HAVE BEEN LOADED DO NOT UNCOMMENT
#=======================================================================
# def populate():
# 	print(os.getcwd())
# 	train_fire = os.listdir('./static/data/train/fire')
# 	train_not_fire = os.listdir('./static/data/train/not_fire')
# 	valid_fire = os.listdir('./static/data/validation/fire')
# 	valid_not_fire = os.listdir('./static/data/validation/not_fire')

# 	for image in train_fire:
# 		img = Image(url = image, is_fire = 1, is_training = 1)
# 		img.save()
# 	for image in train_not_fire:		
# 		img = Image(url = image, is_fire = 0, is_training = 1)
# 		img.save()
# 	for image in valid_fire:
# 		img = Image(url = image, is_fire = 1, is_training = 0)
# 		img.save()
# 	for image in valid_not_fire:		
# 		img = Image(url = image, is_fire = 0, is_training = 0)
# 		img.save()
#========================================================================


# class call_model(APIView):
# 	def get(self,request):
# 	    if request.method == 'GET':
	        
# 	        # sentence is the query we want to get the prediction for
# 	        params =  request.GET.get('sentence')
	        
# 	        # predict method used to get the prediction
# 	        response = WebappConfig.predictor.predict(sentence)
	        
# 	        # returning JSON response
# 	        return JsonResponse(response)

def upload(request):
	global ANSWER
	if request.method == 'POST':
		form = UploadImageForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			handle_uploaded_file(request.FILES['img'])
			return render(request, 'main.html', {'answer': ANSWER, 'image': ImageUpload.objects.all()[0] })
	else:
		form = UploadImageForm()
		ANSWER = -1
	return render(request, 'main.html', {'answer': ANSWER, 'form': form })
