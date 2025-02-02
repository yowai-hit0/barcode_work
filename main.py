# ------------------------------------------generating barcode--------------------------------------
# import barcode
# from barcode.writer import ImageWriter
# # pip install python-barcode and pip install barcode
# # Define the data for the barcode
# data = "https://benax.rw"
#
# # Specify the barcode type (e.g., 'ean13', 'code128', 'upc', etc.)
# barcode_type = "code128"
#
# # Generate the barcode with an image writer
# barcode_class = barcode.get_barcode_class(barcode_type)
# barcode_instance = barcode_class(data, writer=ImageWriter())
#
# # Save the barcode as an image
# output_filename = "barcode"
# barcode_instance.save(output_filename)
#
# print(f"Barcode saved as {output_filename}.png")

# ---------------------------------------decoding barcode ---------------------------------------------

# from pyzbar.pyzbar import decode
# import cv2
# import numpy as np
#
# # Read the image

# image = cv2.imread("barcode.png")
#
# # Decode the barcode
# barcodes = decode(image)
# for barcode in barcodes:
#     data = barcode.data.decode("utf-8")
#     print(f"Barcode Data: {data}")
#     # Draw a rectangle around the barcode
#     points = barcode.polygon
#     points = [(point.x, point.y) for point in points]
#     cv2.polylines(image, [np.array(points, dtype=np.int32)], True, (0, 255, 0), 2)
#
#     # Annotate the decoded data beside the bounding box
#     x, y = points[0]  # Take the first point of the bounding box
#     cv2.putText(image, data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)  # Green text
#
# # Display the image with the barcode highlighted and annotated
# cv2.imshow("Barcode with Annotation", image)
#
# # Wait for a key press
# key = cv2.waitKey(0)
#
# # Save the annotated image when a key is pressed
# output_file = "decoded_barcode.png"
# cv2.imwrite(output_file, image)
# print(f"Annotated image saved as {output_file}")
#
# cv2.destroyAllWindows()


# -----------------------------------------------generate qrcode--------------------------------------------

# # Data to encode in the QR code
# import qrcode
# data = "https://benax.rw"
#
# # Create a QR code object
# qr = qrcode.QRCode(
#     version=1,  # Controls the size of the QR Code (1 is 21x21, up to 40)
#     error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level
#     box_size=10,  # Size of each box in the QR Code grid
#     border=4,  # Thickness of the border (minimum is 4)
# )
#
# # Add data to the QR code
# qr.add_data(data)
# qr.make(fit=True)
#
# # Create an image of the QR code
# qr_image = qr.make_image(fill_color="black", back_color="white")
#
# # Save the QR code image
# qr_image.save("qrcode.png")
# print("QR code saved as 'qrcode.png'")

# ------------------------------------- decode qrcode---------------------------------------------

# import cv2
#
# # Initialize QR code detector
# detector = cv2.QRCodeDetector()
#
# # Read the image
# image = cv2.imread("qrcode.png")
#
# # Detect and decode the QR code
# data, points, _ = detector.detectAndDecode(image)
#
# if data:
#     print(f"QR Code Data: {data}")
#     cv2.polylines(image, [points.astype(int)], True, (0, 255, 0), 2)
# else:
#     print("No QR code detected.")
#
# cv2.imshow("QR Code", image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# ------------------------------------------------ generating pdf417 -----------------------------------------

# import pdf417gen as pdf417
#
# # Data to encode
# data = "This is a PDF417 barcode example. It supports encoding large amounts of data."
#
# # Generate the PDF417 code
# codes = pdf417.encode(data, columns=5)
#
# # Render the codes to an image
# pdf417_image = pdf417.render_image(codes, scale=3)
#
# # Save the image
# pdf417_image.save("pdf417_code.png")
# print("PDF417 code saved as pdf417_code.png")
#
# # Optional: Display the image
# pdf417_image.show()

# ---------------------------------------------- decode pdf417 --------------------------------------------------

import cv2
import numpy as np
import subprocess
import os

# Paths to required files
javase_jar = "javase-3.5.0.jar"
core_jar = "core-3.5.0.jar"
jcommander_jar = "jcommander-1.82.jar"

# barcode_image = "./real-world-codes/IMG_1903.jpg"
barcode_image = "./real-world-codes/IMG_1903.jpg"
# Validate required files
for file in [javase_jar, core_jar, jcommander_jar, barcode_image]:
    if not os.path.exists(file):
        print(f"Error: {file} not found!")
        exit(1)

# Docker command to detect the barcode and get its position
docker_command = [
    "docker", "run", "--rm",
    "-v", f"{os.getcwd()}:/app",
    "openjdk:17",
    "java", "-cp",
    f"/app/{javase_jar}:/app/{core_jar}:/app/{jcommander_jar}",
    "com.google.zxing.client.j2se.CommandLineRunner",
    f"/app/{barcode_image}"
]

try:
    # Run the Docker command to get the decoding and position
    result = subprocess.run(docker_command, capture_output=True, text=True, check=True)
    output = result.stdout.strip()
    print("Decoded Output:")
    print(output)
except subprocess.CalledProcessError as e:
    print("Error during decoding:")
    print(e.stderr)
    exit(1)

# Parse the ZXing output for barcode position
points = []
for line in output.splitlines():
    if line.startswith("  Point"):
        parts = line.split(":")[1].strip().replace("(", "").replace(")", "").split(",")
        points.append((int(float(parts[0])), int(float(parts[1]))))

# If points are found, draw a bounding polygon
if len(points) >= 4:
    # Load the image with OpenCV
    image = cv2.imread(barcode_image)
    if image is None:
        print("Error: Unable to read the image!")
        exit(1)

    # Draw a polygon connecting the points
    points_array = np.array(points, dtype=np.int32).reshape((-1, 1, 2))
    print(f"Drawing polygon with points: {points}")

    cv2.polylines(image, [points_array], isClosed=True, color=(0, 255, 0), thickness=2)

    # Save and display the annotated image
    annotated_image_path = "annotated_barcode.png"
    cv2.imwrite(annotated_image_path, image)
    print(f"Annotated image saved as {annotated_image_path}")

    # Display the image
    cv2.imshow("Detected Barcode", image)
    print("Press any key to close the window.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No bounding box points detected.")