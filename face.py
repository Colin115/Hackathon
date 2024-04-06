from deepface import DeepFace


def compare_faces(f1, f2):
    # Perform face verification
    backends = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe']
    result = DeepFace.verify(img1_path=f1, img2_path=f2, detector_backend=backends[2], enforce_detection=True)
    
    return result["verified"]


if __name__ == "__main__":
    # Paths to the images
    image1_path = "IMG_7468.jpg"
    image2_path = "IMG_7470.jpg"

    # Compare faces
    similar_faces = compare_faces(image1_path, image2_path)

    if similar_faces:
        print("The faces are similar.")
    else:
        print("The faces are different.")














