from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import tensorflow as tf
import numpy as np
import io
import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from django.utils.decorators import method_decorator

from django.views.decorators.csrf import csrf_exempt
from products.models import Organization, Products

# Create your views here.
class getPrediction(View):
    def get(self,request): 
        diseases = ['Gray Leaf Spot on Corn',
        'Common rust Corn',
        'Northern Corn Leaf Blight',
        'Tomato Bacterial Spot',
        'Early Blight',
        'Late Blight']
        return render(request, 'index.html', {'diseases': diseases}) 
    
@method_decorator(csrf_exempt, name='dispatch')
class makePrediction(View):
    def post(self, request):
        data = {
            'key1': 'value1',
            'key2': 'value2',
            # Add more key-value pairs as needed
        }

        class_names = ['Gray Leaf Spot on Corn',
        'Common rust Corn',
        'Northern Corn Leaf Blight',
        'Corn_(maize)___healthy',
        'Tomato Bacterial Spot',
        'Early Blight',
        'Late Blight',
        'Tomato___healthy']
        image_file = request.FILES.get('image')
        print(image_file)
        print("TensorFlow version:", tf.__version__)

        
            # Read the content of the uploaded file into memory as bytes
        if not image_file or not image_file.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            return JsonResponse({'error': 'Invalid image file'}, status=400)

        # # Load the image using Keras's load_img function
        image_data = io.BytesIO(image_file.read())
        img = image.load_img(image_data, target_size=(128, 128))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0

        model_path = "predictions\\final_model.h5"
        res = os.path.isfile(model_path)
        print(res)
        try:
            model = load_model(model_path)
            print("here")
        except Exception as e:
            error_message = str(e)  # Get the error message as a string
            print("Error loading model:", error_message)
            return JsonResponse({'error': 'Error loading model: ' + error_message}, status=500)



        prediction = model.predict(img_array)

# Get the predicted class
        predicted_class = np.argmax(prediction)
        confidence = prediction[0][predicted_class]

        print("Predicted class:", predicted_class)
        print("Confidence:", confidence)
        predicted_class_name = class_names[predicted_class]
        print("predicted class name: ", predicted_class_name)

        if(predicted_class_name == "Corn_(maize)___healthy" or predicted_class_name == "Tomato___healthy"):
            return JsonResponse({
            'preventive_measures': [],
            'treatment_options': [],
            'links': [],
            'prediction': predicted_class_name,
            'confidence': round(float(confidence) * 100, 2) ,
            'products': []
            })
        with open('predictions\\disease_info_2.json', 'r') as file:
            disease_info = json.load(file)

        def get_disease_information(disease_name):
            # Check if the disease name exists in the loaded JSON data
            if disease_name in disease_info:
                return disease_info[disease_name]
            else:
                 return JsonResponse({
            'preventive_measures': [],
            'treatment_options': [],
            'links': [],
            'prediction': predicted_class_name,
            'confidence': round(float(confidence) * 100, 2) ,
            'products': []
            })

        result = get_disease_information(predicted_class_name)
        print(result)

        if isinstance(result, dict):
            preventive_measures = result.get("Preventive Measures", [])
            treatment_options = result.get("Treatment Options", [])
            urls = result.get("Url", [])
        

            print("Preventive Measures:")
            for measure in preventive_measures:
                print(f"- {measure}")

            print("\nTreatment Options:")
            for option in treatment_options:
                print(f"- {option}")
                
            print("\nLinks:")
            for option in urls:
                print(f"- {option}")
        else:
            print(result)

        print(preventive_measures)
        print(treatment_options)
        print(urls)
        print(predicted_class_name)
        products = Products.objects.filter(disease_name=predicted_class_name).select_related('org').values(        'id',
        'disease_name',
        'product',
        'product_link',
        'org__name',
        'org__address',
        'org__email',
        'org__phone_number',
        'org__website',
        'org__location',)
        
        product_list = list(products)
        print(product_list)

        return JsonResponse({
            'preventive_measures': preventive_measures,
            'treatment_options': treatment_options,
            'links': urls,
            'prediction': predicted_class_name,
            'confidence': round(float(confidence) * 100, 2) ,
            'products': product_list
            })
    

    
