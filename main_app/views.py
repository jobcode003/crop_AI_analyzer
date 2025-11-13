from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
from django.views.decorators.csrf import csrf_exempt
import json
import ollama

model=load_model('/home/job/Desktop/agri_agent_AI/AgriProject/main_app/mobilenet_finetuned2.keras')
class_names=['corn_Blight', 'corn_Gray Leaf Spot', 'corn_Healthy',
             'corn_Northern_Leaf_Blight', 'corn_common_Rust', 'potato_Early Blight',
             'potato_Healthy', 'potato_Late Blight']

def page(request):
    return render(request,"index.html")

def process(request):
    prediction = None
    confidence = None

    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_file = request.FILES['image']

        # Save uploaded image temporarily
        temp_path = os.path.join('media/uploads', uploaded_file.name)
        os.makedirs(os.path.dirname(temp_path), exist_ok=True)

        with open(temp_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        # Preprocess the image
        img = image.load_img(temp_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = img_array / 255.0  # Normalize
        img_array = np.expand_dims(img_array, axis=0)

        # Predict
        predictions = model.predict(img_array)
        predicted_class_index = np.argmax(predictions[0])
        prediction = class_names[predicted_class_index]
        confidence = round(100 * np.max(predictions[0]), 2)

        # Delete temporary file
        os.remove(temp_path)

    # Render back to the same page with results
    return render(request, 'index.html', {
        'prediction': prediction,
        'confidence': confidence
    })

@csrf_exempt
def chatbot(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "")

        # Build context (you can expand this with FAISS later)
        context = """
        You are an agricultural expert chatbot.
        You answer questions about maize and potato diseases,
        including causes, prevention, and remedies.
        """

        prompt = f"{context}\nFarmer: {user_message}\nAssistant:"

        # Call Ollama
        response = ollama.chat(model="llama3.2:1b", messages=[
            {"role": "user", "content": prompt}
        ])

        answer = response["message"]["content"]
        return JsonResponse({"reply": answer})