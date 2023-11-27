import cv2
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

# Load mô hình đã huấn luyện
model = tf.keras.models.load_model('improved_handwritten15.model')

def preprocess_image(image):
    # Chuyển ảnh về ảnh xám
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Làm mịn ảnh để làm nổi bật các đặc trưng
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Áp dụng adaptive thresholding để tạo ảnh nhị phân
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 4)

    return thresh

def predict_digit(image):
    processed_image = preprocess_image(image)

    # Tìm contours trong ảnh đã xử lý
    contours, _ = cv2.findContours(processed_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    digits = []

    for contour in contours:
        # Lấy bounding box của contour
        x, y, w, h = cv2.boundingRect(contour)

        # Kiểm tra kích thước của contour và tạo bounding box
        if w > 5 and h > 20:  # Điều kiện kích thước contour
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Trích xuất và chuẩn bị số để dự đoán
            digit_roi = processed_image[y:y + h, x:x + w]
            resized_digit = cv2.resize(digit_roi, (28, 28), interpolation=cv2.INTER_AREA)
            normalized = resized_digit.reshape(-1, 28, 28, 1) / 255.0

            # Dự đoán số
            prediction = model.predict(normalized)
            digit = np.argmax(prediction)
            digits.append(digit)

            # Hiển thị số dự đoán
            cv2.putText(image, str(digit), (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    return image, digits

# Đường dẫn đến ảnh cần nhận dạng
image_path = './data/data1.png'  # Thay đổi đường dẫn này đến ảnh cần dự đoán

# Đọc ảnh và gọi hàm predict_digit
image = cv2.imread(image_path)
output_image, predicted_digits = predict_digit(image)

# Hiển thị ảnh và kết quả dự đoán
plt.imshow(cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB))
plt.title(f"Ket Qua: {predicted_digits}")
plt.axis('off')
plt.show()