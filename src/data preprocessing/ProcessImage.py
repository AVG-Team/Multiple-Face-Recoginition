import cv2
import os
import dlib
from PIL import Image


def crop_face(input_path, output_path):
    # Use dlib to detect model hog face
    detector = dlib.get_frontal_face_detector()
    data_not_found = []
    for foldername in os.listdir(input_path):
        subfolder_path = os.path.join(input_path, foldername)

        if os.path.isdir(subfolder_path):

            for filename in os.listdir(subfolder_path):
                # only processes image files jpg jpeg png
                if filename.endswith(('.jpg', '.jpeg', '.png')):

                    image_path = os.path.join(subfolder_path, filename)
                    image = Image.open(image_path)

                    img_array = dlib.load_rgb_image(image_path)
                    dets = detector(img_array, 1)

                    if len(dets) > 0:
                        # Only take the first recognized face
                        face = dets[0]

                        # Get the coordinates of the face
                        left, top, right, bottom = face.left(), face.top(), face.right(), face.bottom()

                        # Crop photo according to face
                        cropped_image = image.crop((left - 100, top - 100, right + 100, bottom + 100))

                        # Create an output directory if it doesn't exist yet
                        output_folder_path = os.path.join(output_path, foldername)
                        os.makedirs(output_folder_path, exist_ok=True)

                        # Save the cropped image to the output folder
                        if os.path.splitext(filename)[1].lower() == ".jpg" or os.path.splitext(filename)[
                            1].lower() == '.jpeg':
                            output_image_path_tmp = os.path.join(output_folder_path,
                                                                 f"{os.path.splitext(filename)[0]}.png")
                        else:
                            output_image_path_tmp = os.path.join(output_folder_path, f"{filename}")

                        # enhance image data
                        flipped_horizontal = cropped_image.transpose(Image.FLIP_LEFT_RIGHT)
                        flipped_vertical = cropped_image.transpose(Image.FLIP_TOP_BOTTOM)
                        flipped_left = cv2.flip(Image, 1)
                        flipped_right = cv2.flip(Image, 0)
                        imgGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                        # Save file
                        flipped_horizontal.save(
                            os.path.join(output_folder_path, f"{os.path.splitext(filename)[0]}_1.png"))
                        flipped_vertical.save(
                            os.path.join(output_folder_path, f"{os.path.splitext(filename)[0]}_2.png"))
                        flipped_left.save(
                            os.path.join(output_folder_path, f"{os.path.splitext(filename)[0]}_3.png"))
                        flipped_right.save(
                            os.path.join(output_folder_path, f"{os.path.splitext(filename)[0]}_4.png"))
                        imgGray.save(
                            os.path.join(output_folder_path, f"{os.path.splitext(filename)[0]}_5.png"))
                        cropped_image.save(output_image_path_tmp)

                        print(f"Image {filename} has been cropped successfully")
                    else:
                        print(f"No face found in the photo {filename}")

                        data_not_found.append(filename)
    data_not_found_name_file = "data_not_found.txt"
    if not os.path.exists(data_not_found_name_file):
        # If it doesn't exist, create a new file
        with open(data_not_found_name_file, 'w') as file:
            for item in data_not_found:
                file.write(str(item) + '\n')
        print(f"The file {data_not_found_name_file} has been created and data has been written to.")
    else:
        with open(data_not_found_name_file, 'w') as file:
            for item in data_not_found:
                file.write(str(item) + '\n')
        print(f"The file {data_not_found_name_file} has been created and data has been written to.")


# Input and output paths
input_image_path = "../../Images/not_process"
output_image_path = "../../Images/processed"

# Call the function to crop the image focusing on the face
crop_face(input_image_path, output_image_path)
