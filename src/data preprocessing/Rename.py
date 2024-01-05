import os

# Đọc nội dung từ file ex.txt
with open('train_ai.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Lặp qua từng dòng trong file và thực hiện đổi tên thư mục và file
for line in lines:
    # Tách thông tin từ mỗi dòng
    parts = line.strip().split(' ')
    student_id, student_name = parts[0], parts[1:]

    # Tạo đường dẫn mới cho thư mục hình ảnh
    old_path = os.path.join('../../Images', ' '.join(student_name))
    new_path = os.path.join('../../Images', student_id)

    # Đổi tên thư mục
    if not os.path.exists(new_path):
        os.rename(old_path, new_path)

        # Lặp qua các file trong thư mục mới và đổi tên
        for i, filename in enumerate(os.listdir(new_path)):
            old_file_path = os.path.join(new_path, filename)
            new_file_name = f"{student_id}_{i+1}.png"
            new_file_path = os.path.join(new_path, new_file_name)

            # Đổi tên file
            os.rename(old_file_path, new_file_path)

# Hiển thị thông báo khi hoàn thành
print("Đổi tên thư mục và file thành công.")
