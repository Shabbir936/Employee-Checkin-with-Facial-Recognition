import face_recognition as fr 
import numpy as np
import cv2
from io import BytesIO
from PIL import Image
from anti_spoofing.test import test

def compare_photos(known_image_path, unknown_image):
    known_image = fr.load_image_file(known_image_path)

    # Get the face encodings
    try:
        known_encoding = fr.face_encodings(known_image)[0]
        unknown_encoding = fr.face_encodings(unknown_image)[0]
    except IndexError:
        # Handle the case where no faces are found in the photos
        print('Images Not Found')
        return False

    # Compare the faces
    results = fr.compare_faces([known_encoding], unknown_encoding)
    is_same_person = results[0]
    return is_same_person

def is_live_photo_and_matches(image_path, unknown_image):
    file_content = unknown_image.read()
    image_arr = np.frombuffer(file_content, np.uint8)
    cv2_image = cv2.imdecode(image_arr, cv2.IMREAD_COLOR)
    image_stream = BytesIO(file_content)
    image_stream.seek(0)
    pil_image = Image.open(image_stream)
    pil_image = pil_image.convert('RGB')
    fr_image = np.array(pil_image)
    real_image = test(image=cv2_image, device_id=0)
    if real_image == 1:
        if compare_photos(image_path,fr_image):
            return "Matching"
        return "Different"
    return "Spoof"
        