import os
import dlib
from PIL import Image

def crop_face(input_path, output_path):
    # Sử dụng dlib để nhận diện khuôn mặt
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    for foldername in os.listdir(input_path):
        subfolder_path = os.path.join(input_path, foldername)

        if os.path.isdir(subfolder_path):

            for filename in os.listdir(subfolder_path):
                if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):

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
                        cropped_image = image.crop((left-100, top-100, right+100, bottom+100))

                        # Tạo thư mục đầu ra nếu chưa tồn tại
                        output_folder_path = os.path.join(output_path, foldername)
                        os.makedirs(output_folder_path, exist_ok=True)

                        # Lưu ảnh đã cắt ra thư mục đầu ra
                        output_image_path = os.path.join(output_folder_path, f"cropped_{filename}")
                        cropped_image.save(output_image_path)
                        print(f"Đã cắt ảnh {filename} thành công")
                    else:
                        print(f"Không tìm thấy khuôn mặt trong ảnh {filename}")

# Đường dẫn đầu vào và đầu ra
input_image_path = "../../Input"
output_image_path = "../../Images"

# Gọi hàm để cắt ảnh tập trung vào khuôn mặt
crop_face(input_image_path, output_image_path)
