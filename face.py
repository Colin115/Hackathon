from deepface import DeepFace


def compare_faces(image1_path, image2_path):
    # Perform face verification
    result = DeepFace.verify(image1_path, image2_path)
    return result["verified"]


    # Check if images are loaded successfully
    if img1 is None:
        print(f"Error: Unable to load image from '{image1_path}'")
        return None
    elif img2 is None:
        print(f"Error: Unable to load image from '{image2_path}'")
        return None

if __name__ == "__main__":
    # Paths to the images
    image1_path = "IMG_7469.jpg"
    image2_path = "IMG_7471.jpg"

    # Compare faces
    similar_faces = compare_faces(image1_path, image2_path)

    if similar_faces:
        print("The faces are similar.")
    else:
        print("The faces are different.")














