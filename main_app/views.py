from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
from django.views.decorators.csrf import csrf_exempt
import json
import requests
import ollama


model=load_model('main_app/mobilenet_finetuned2.keras')
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
        temp_path = os.path.join('media/uploads', uploaded_file.name)
        os.makedirs(os.path.dirname(temp_path), exist_ok=True)

        with open(temp_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        #code to preproces the image
        img = image.load_img(temp_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = img_array / 255.0  
        img_array = np.expand_dims(img_array, axis=0)

        # making  Predictions
        predictions = model.predict(img_array)
        predicted_class_index = np.argmax(predictions[0])
        prediction = class_names[predicted_class_index]
        confidence = round(100 * np.max(predictions[0]), 2)

        
        os.remove(temp_path)

    # Render back to the same page with results
    return render(request, 'index.html', {
        'prediction': prediction,
        'confidence': confidence
    })


@csrf_exempt
def chat(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')
        prompt = f"""
            You are AgriBot, an agricultural assistant for small farmers.
            RULES:
            - Respond in plain text, no markdown or asterisks.
            - Output in short, clear points, each point on a new line.
            - Include Causes, Symptoms, Remedies.
            - No greetings or introductions.
            - Each point should be a complete sentence.
            Question: {user_message}"""

        url = "https://api.groq.com/openai/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 300
        }

        response = requests.post(url, headers=headers, json=payload)
        print("STATUS:", response.status_code)
        print("RAW RESPONSE TEXT:", response.text)


        try:
            result = response.json()
        except Exception as e:
            print("JSON PARSE ERROR:", e)
            print("UNPARSED RESPONSE:", response.text)
            return JsonResponse({"response": "Groq returned invalid JSON."})

        print("PARSED RESULT:", result)

                                                         
        if "error" in result:
            return JsonResponse({"response": f"Groq Error: {result['error']['message']}"})

        try:
            reply = result["choices"][0]["message"]["content"]
        except Exception as e:
            print("CHOICES ERROR:", e)
            print("RESULT STRUCTURE:", result)
            return JsonResponse({"response": "Groq did not return a valid AI message."})

        return JsonResponse({"response": reply})

    return JsonResponse({"error": "Invalid request"}, status=400)
