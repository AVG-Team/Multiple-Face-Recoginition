import os
import dlib
from PIL import Image


def crop_face(input_path, output_path):
    # Sử dụng dlib để nhận diện khuôn mặt model hog
    detector = dlib.get_frontal_face_detector()
    data_not_found = []
    for foldername in os.listdir(input_path):
        subfolder_path = os.path.join(input_path, foldername)

        if os.path.isdir(subfolder_path):

            for filename in os.listdir(subfolder_path):
                if filename.endswith(('.jpg', '.jpeg', '.png')):

                    image_path = os.path.join(subfolder_path, filename)
                    image = Image.open(image_path)

                    img_array = dlib.load_rgb_image(image_path)
                    dets = detector(img_array, 1)

                    if len(dets) > 0:
                        # Chỉ lấy khuôn mặt đầu tiên được nhận diện
                        face = dets[0]

                        # Lấy tọa độ của khuôn mặt
                        left, top, right, bottom = face.left(), face.top(), face.right(), face.bottom()

                        # Cắt ảnh theo khuôn mặt
                        cropped_image = image.crop((left - 100, top - 100, right + 100, bottom + 100))

                        # Tạo thư mục đầu ra nếu chưa tồn tại
                        output_folder_path = os.path.join(output_path, foldername)
                        os.makedirs(output_folder_path, exist_ok=True)

                        # Lưu ảnh đã cắt ra thư mục đầu ra
                        if os.path.splitext(filename)[1].lower() == ".jpg" or os.path.splitext(filename)[1].lower() == '.jpeg':
                            output_image_path_tmp = os.path.join(output_folder_path, f"{os.path.splitext(filename)[0]}.png")
                        else:
                            output_image_path_tmp = os.path.join(output_folder_path, f"{filename}")

                        flipped_horizontal = cropped_image.transpose(Image.FLIP_LEFT_RIGHT)
                        flipped_vertical = cropped_image.transpose(Image.FLIP_TOP_BOTTOM)

                        flipped_horizontal.save(os.path.join(output_folder_path, f"{os.path.splitext(filename)[0]}_1.png"))
                        flipped_vertical.save(os.path.join(output_folder_path, f"{os.path.splitext(filename)[0]}_2.png"))
                        cropped_image.save(output_image_path_tmp)

                        print(f"Đã cắt ảnh {filename} thành công")
                    else:
                        print(f"Không tìm thấy khuôn mặt trong ảnh {filename}")

                        data_not_found.append(filename)
    data_not_found_name_file = "data_not_found.txt"
    if not os.path.exists(data_not_found_name_file):
        # Nếu không tồn tại, tạo mới tệp
        with open(data_not_found_name_file, 'w') as file:
            for item in data_not_found:
                file.write(str(item) + '\n')
        print(f"Tệp {data_not_found_name_file} đã được tạo và dữ liệu đã được ghi vào.")
    else:
        with open(data_not_found_name_file, 'w') as file:
            for item in data_not_found:
                file.write(str(item) + '\n')
        print(f"Tệp {data_not_found_name_file} đã tồn tại và dữ liệu đã được ghi vào.")


# Đường dẫn đầu vào và đầu ra
input_image_path = "../../Images/not_process"
output_image_path = "../../Images/processed"

# Gọi hàm để cắt ảnh tập trung vào khuôn mặt
crop_face(input_image_path, output_image_path)
