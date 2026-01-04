import requests
import base64
import os

# The URL of your running Flask API
API_URL = "http://127.0.0.1:5000/segment"

# The path to the image you want to process
IMAGE_TO_TEST = "test_images/4.jpg" # <--- IMPORTANT: Change this!

# The folder to save the results in
OUTPUT_FOLDER = "api_results"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

try:
    # Open the image file in binary mode and send it
    with open(IMAGE_TO_TEST, 'rb') as f:
        files = {'file': (os.path.basename(IMAGE_TO_TEST), f, 'image/jpeg')}
        print(f"Sending {IMAGE_TO_TEST} to the API...")
        response = requests.post(API_URL, files=files)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'success':
            documents = data.get('documents', [])
            print(f"API returned {len(documents)} documents.")
            
            # Decode and save each document
            for doc in documents:
                filename = doc['filename']
                image_data = base64.b64decode(doc['data'])
                
                output_path = os.path.join(OUTPUT_FOLDER, filename)
                with open(output_path, 'wb') as out_f:
                    out_f.write(image_data)
                print(f"  - Saved {filename} to {output_path}")

        else:
            print(f"API returned an error: {data.get('message')}")
    else:
        print(f"Failed to call API. Status code: {response.status_code}")
        print("Response:", response.text)

except requests.exceptions.ConnectionError as e:
    print(f"Connection Error: Could not connect to the API at {API_URL}.")
    print("Please make sure the Flask server (app.py) is running.")