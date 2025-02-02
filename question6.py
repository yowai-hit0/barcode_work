import os
from pyzxing import BarCodeReader

def decode_maxicode(image_path):
    # Ensure the file exists
    if not os.path.exists(image_path):
        return f"Error: File '{image_path}' not found."

    # Initialize the barcode reader
    reader = BarCodeReader()

    try:
        # Decode the MaxiCode from the image file
        result = reader.decode(image_path)

        # Check if the decoding was successful
        if result:
            # Return the decoded data (MaxiCode content)
            return result[0]['parsed']
        else:
            return "Error: No MaxiCode detected in the image."

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    # Path to the MaxiCode image file
    image_path = "./real-world-codes/maxicode-example.png"  # Replace with your MaxiCode image path

    # Decode the MaxiCode
    decoded_output = decode_maxicode(image_path)

    # Print the result
    print(decoded_output)
