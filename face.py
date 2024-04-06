import cv2

def compare_images(image1_path, image2_path, threshold=1000):
    # Read images
    img1 = cv2.imread(image1_path)
    img2 = cv2.imread(image2_path)
    
    # Convert images to grayscale
    gray_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    
    # Compute Mean Squared Error (MSE)
    mse = ((gray_img1 - gray_img2) ** 2).mean()
    
    return mse < threshold

if __name__ == "__main__":
    # Paths to the images
    image1_path = "image1.jpg"
    image2_path = "image2.jpg"
    
    # Compare images
    similar = compare_images(image1_path, image2_path)
    
    if similar:
        print("The images are similar.")
    else:
        print("The images are different.")

