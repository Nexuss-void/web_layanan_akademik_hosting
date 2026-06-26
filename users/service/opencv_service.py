import cv2
import numpy as np
import uuid
from django.core.files.base import ContentFile

def detect_face(image_bytes):
    np_array=np.frombuffer(image_bytes,np.uint8)
    image_decode=cv2.imdecode(np_array,cv2.IMREAD_GRAYSCALE)
    print("Shape:", image_decode.shape)

    face_cascade=cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml' )
    face=face_cascade.detectMultiScale(image_decode, scaleFactor=1.1, minNeighbors=3)
    print("Faces:", len(face))

    if len(face) == 0:
        return 'No face'
    
    if len(face) > 1:
        return 'Multiple faces'
    
    x, y, w, h = face[0]
    face_crop = image_decode[y:y+h,x:x+w]
    face_resize = cv2.resize(face_crop,(228, 228))
    img_for_fer = np.stack([face_resize] * 3,axis=-1)
    _, buffer = cv2.imencode('.png',face_resize)

    processed_image = ContentFile(
        buffer.tobytes(),
        name=f"{uuid.uuid4()}.png"
    )

    print("FER Input Shape:", img_for_fer.shape)
    return {
        'fer_img':img_for_fer,
        'save_img':processed_image
        }
