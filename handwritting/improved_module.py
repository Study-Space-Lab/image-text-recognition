import tensorflow as tf
from tensorflow.keras import layers ##Cung cấp các lớp cơ bản để xây dựng mô hình neural network
from tensorflow.keras.datasets import mnist ## Bộ dữ liệu MNIST chứa các hình ảnh chữ số viết tay.
from tensorflow.keras.models import Sequential ## Mô hình neural network tuần tự.
from tensorflow.keras.optimizers import Adam ## Thuật toán tối ưu hóa.
from tensorflow.keras.callbacks import LearningRateScheduler ## Callback cho việc điều chỉnh tốc độ học.
from tensorflow.keras import regularizers

# Load và chuẩn bị dữ liệu
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = x_train.reshape(-1, 28, 28, 1) / 255.0
x_test = x_test.reshape(-1, 28, 28, 1) / 255.0
## Dữ liệu MNIST được tải và chuẩn bị để sử dụng trong mô hình. Hình ảnh được chia tỷ lệ giữa 0 và 1 bằng cách chia cho 255.

# Xây dựng mô hình CNN
model = Sequential([
    layers.Conv2D(32, 3, activation='relu', input_shape=(28, 28, 1)),
    layers.MaxPooling2D(2),
    layers.Conv2D(64, 3, activation='relu'),
    layers.MaxPooling2D(2),
    layers.Conv2D(128, 3, activation='relu'),
    layers.Flatten(),
    layers.Dropout(0.2),
    layers.Dense(10, activation='softmax', kernel_regularizer=regularizers.l2(0.001))
])
## Mô hình bao gồm các lớp Convolutional, MaxPooling, Flatten, Dropout và Dense. Mục tiêu là phân loại chữ số từ 0 đến 9.

# Biên dịch mô hình
model.compile(loss='sparse_categorical_crossentropy', optimizer=Adam(learning_rate=0.001), metrics=['accuracy'])
## Hàm này được sử dụng để giảm tốc độ học sau 10 epochs.

# Định nghĩa hàm điều chỉnh tốc độ học
def lr_scheduler(epoch, lr):
    if epoch < 10:
        return lr
    else:
        return lr * 0.9

# Huấn luyện mô hình và sử dụng LearningRateScheduler
datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    rotation_range=10,
    width_shift_range=0.1,
    height_shift_range=0.1,
    zoom_range=0.1
)
## Dữ liệu được tăng cường (Data Augmentation) bằng cách xoay, dịch và zoom hình ảnh. Mô hình được huấn luyện qua 20 epochs.

# Huấn luyện mô hình
model.fit(
    datagen.flow(x_train, y_train, batch_size=32),
    epochs=20,
    validation_data=(x_test, y_test),
    callbacks=[LearningRateScheduler(lr_scheduler)]
)

# Lưu mô hình
model.save("improved_handwritten15.model")
## Mô hình được lưu xuống tệp "improved_handwritten15.model" để sử dụng sau này.