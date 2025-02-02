import cv2
import pyzxing

def process_and_decode(image_path):

    # Read the image using OpenCV
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use ZXing (pyzxing) to decode the barcode
    zx = pyzxing.BarCodeReader()
    decoded = zx.decode(image_path)

    if decoded:
        # Return the decoded data (ZXing returns it as a dictionary)
        return decoded[0]['parsed']
    else:
        return "No barcode found"

if __name__ == "__main__":
    # Define the image path
    image_path = "./real-world-codes/aztec-example.jpg"

    try:
        result = process_and_decode(image_path)
        print("Decoded Data:", result)
    except Exception as e:
        print("Decoding failed:", e)
