import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import filedialog
from PIL import Image, ImageTk
import pytesseract
import tkinter.messagebox

# Đặt đường dẫn của tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Phap\\Downloads\\DOW_PHAN_MEM_HOC\Newpython\Newpython\tesseract.exe'
class OCRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OCR App")

        # Tạo các biến
        self.image_path = None
        self.result_text = tk.StringVar()
        self.photo = None
        self.photo_label = tk.Label(self.root)  # Khởi tạo label một lần

        # Tạo các thành phần GUI
        self.create_widgets()

    def create_widgets(self):
        # Frame chứa các thành phần
        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.pack(expand=True, fill="both")

        # Thêm các widget vào frame
        # Kéo và thả ảnh
        label_drag_drop = tk.Label(frame, text="Kéo và thả ảnh vào đây:")
        label_drag_drop.grid(row=0, column=0, pady=10)

        frame_drag_drop = tk.Frame(frame, bg="lightgray", width=500, height=400)
        frame_drag_drop.grid(row=1, column=0, pady=10)
        frame_drag_drop.drop_target_register(DND_FILES)
        frame_drag_drop.dnd_bind('<<Drop>>', self.on_drop)

        # Kết quả OCR
        label_result = tk.Label(frame, text="Kết quả OCR:")
        label_result.grid(row=0, column=1, pady=10)

        self.text_result = tk.Text(frame, wrap="word", width=80, height=30)
        self.text_result.grid(row=1, column=1, padx=(0, 10), sticky="w")
        self.text_result.insert("1.0", "Kết quả sẽ xuất hiện ở đây.")
        # Kết nối StringVar với Text widget
        self.result_text = tk.StringVar()

        # Nút Copy
        button_copy = tk.Button(frame, text="Copy", command=self.copy_result)
        button_copy.grid(row=2, column=1, pady=(10, 0), sticky="w")

        # Nút Mở Thư mục
        button_open_folder = tk.Button(frame, text="Mở Thư mục", command=self.open_folder)
        button_open_folder.grid(row=3, column=0, pady=(10, 0), sticky="w")

    def on_drop(self, event):
        # Xử lý sự kiện khi thả ảnh vào frame
        file_path = event.data
        self.image_path = file_path
        self.process_image()

    def process_image(self):
        # Xử lý hình ảnh và hiển thị kết quả
        if self.image_path:
            try:
                # # Mở hình ảnh
                image = Image.open(self.image_path)
                # image.thumbnail((400, 200))

                # # Hiển thị hình ảnh trên label
                # self.photo = ImageTk.PhotoImage(image)
                # self.photo_label.config(image=self.photo)  # Cập nhật hình ảnh
                # self.photo_label.grid(row=1, column=0, padx=(0, 10), sticky="w")

                # Nhận diện văn bản từ hình ảnh
                text = pytesseract.image_to_string(image)
                print(text)

                # Hiển thị kết quả trong Text widget
                self.result_text.set(text)
                self.text_result.delete("1.0", tk.END)
                self.text_result.insert(tk.END, text)

            except Exception as e:
                tkinter.messagebox.showerror("Lỗi", f"Lỗi: {str(e)}")

    def copy_result(self):
        # Sao chép kết quả vào clipboard
        result_text = self.result_text.get()
        self.root.clipboard_clear()
        self.root.clipboard_append(result_text)
        self.root.update()

    def open_folder(self):
        # Mở thư mục và chọn file ảnh
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
        if file_path:
            self.image_path = file_path
            self.process_image()

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = OCRApp(root)
    root.mainloop()