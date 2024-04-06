import face_recognition

# Load the images
image1 = face_recognition.load_image_file("image1.jpg")
image2 = face_recognition.load_image_file("image2.jpg")

# Find face locations in each image
face_locations1 = face_recognition.face_locations(image1)
face_locations2 = face_recognition.face_locations(image2)

# If there are no faces in either image, they can't be compared
if len(face_locations1) == 0 or len(face_locations2) == 0:
    print("No faces found in one or both images.")
else:
    # Encode the faces in each image
    face_encodings1 = face_recognition.face_encodings(image1, face_locations1)
    face_encodings2 = face_recognition.face_encodings(image2, face_locations2)

    # Compare the first face found in each image
    match = face_recognition.compare_faces([face_encodings1[0]], face_encodings2[0])

    if match[0]:
        print("They are the same person")
    else:
        print("Different people are present in the images.")
