from fer import FER

detector = FER(mtcnn=True)
def detect_emotion(face_image):
    print("Received Shape:", face_image.shape)
    results = detector.detect_emotions(face_image)
    if len(results) == 0:
        return 'No face'
    
    emotions = results[0]['emotions']
    dominan_emotion = max(emotions, key=emotions.get)

    return {
        'dominan_emotion': dominan_emotion,
        'emotion_details': emotions
    }