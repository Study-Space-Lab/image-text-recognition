import tkinter as tk
from PIL import ImageGrab, ImageOps, Image
import win32gui
import numpy as np
import tensorflow as tf

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.x = self.y = 0
        # Tải mô hình TensorFlow
        self.model = tf.keras.models.load_model('improved_handwritten15.model')

        # Tạo các thành phần giao diện
        self.canvas = tk.Canvas(self, width=400, height=400, bg="white", cursor="cross")
        self.label = tk.Label(self, text="Kết Quả", font=("Helvetica", 48))
        self.clear_button = tk.Button(self, text="Xóa", command=self.clear_all)
        self.canvas.grid(row=0, column=0, pady=2, sticky=tk.W)
        self.label.grid(row=0, column=1, pady=2, padx=2)
        self.clear_button.grid(row=1, column=0, pady=2)

        # Gắn các sự kiện
        self.canvas.bind("<B1-Motion>", self.draw_lines)  # Gắn sự kiện kéo chuột
        self.canvas.bind("<ButtonRelease-1>", self.classify_handwriting)  # Gắn sự kiện thả chuột

    def clear_all(self):
        # Xóa mọi thứ trên canvas và cập nhật nhãn kết quả
        self.canvas.delete("all")
        self.label.configure(text="Kết Quả")

    def classify_handwriting(self, event):
        # Lấy cửa sổ chứa canvas
        HWND = self.canvas.winfo_id()
        rect = win32gui.GetWindowRect(HWND)
        im = ImageGrab.grab(rect)
        im = ImageOps.grayscale(im)  # Chuyển đổi sang ảnh xám
        im = im.resize((28, 28))
        im = ImageOps.invert(im)  # Đảo ngược ảnh để có chữ số đen trên nền trắng
        im = np.array(im)
        im = im.astype('float32') / 255.0
        im = im.reshape(1, 28, 28, 1)  # Reshape để phù hợp với kích thước đầu vào của mô hình

        # Dự đoán
        prediction = self.model.predict(im)
        digit = np.argmax(prediction)
        acc = np.max(prediction)

        self.label.configure(text=str(digit) + ', ' + str(int(acc * 100)) + '%               ')

    def draw_lines(self, event):
        # Vẽ các đường tròn khi di chuyển chuột
        self.x = event.x
        self.y = event.y
        r = 8
        self.canvas.create_oval(self.x - r, self.y - r, self.x + r, self.y + r, fill='black')


app = App()
app.mainloop()