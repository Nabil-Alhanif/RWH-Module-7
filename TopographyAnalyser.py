import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

def proper_round(num, dec=0):
    num = str(num)[:str(num).index('.')+dec+2]
    if num[-1]>='5':
        return float(num[:-2-(not dec)]+str(int(num[-2-(not dec)])+1))
    return float(num[:-1])

class ImageDistanceCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Distance Calculator")

        self.canvas = tk.Canvas(self.root)
        self.canvas.pack()

        self.img = Image
        self.photo_img = None
        self.image_path = ""

        self.point1 = None
        self.point2 = []

        self.canvas.bind("<Button-1>", self.select_point)

        select_button = tk.Button(self.root, text = "Select Image", command = self.open_image)
        select_button.pack()

        calculate_button = tk.Button(self.root, text = "Calculate Distance", command = self.calculate_distance)
        calculate_button.pack()

        delete_button = tk.Button(self.root, text = "Clear Dots", command = self.clear)
        delete_button.pack()

    def open_image(self):
        self.image_path = filedialog.askopenfilename()
        if self.image_path:
            self.img = Image.open(self.image_path)
            self.photo_img = ImageTk.PhotoImage(self.img)
            self.canvas.config(width = self.img.width, height = self.img.height)
            self.canvas.create_image(0, 0, anchor = tk.NW, image = self.photo_img)

    def select_point(self, event):
        if self.img:
            if not self.point1:
                current_point = self.canvas.create_oval(event.x-5, event.y-5, event.x+5, event.y+5, fill="red")
                self.point1 = (current_point, event.x, event.y)
            else:
                current_point = self.canvas.create_oval(event.x-5, event.y-5, event.x+5, event.y+5, fill="blue")
                self.point2.append((current_point, event.x, event.y))

    def calculate_distance(self):
        if self.point1 and self.point2:
            arr = []
            for p2 in self.point2:
                act_x = p2[1] - self.point1[1]
                x_dist = abs(self.point1[1] - p2[1]) * 120 / self.img.width
                x_dist = round(x_dist)
                if (act_x < 0):
                    x_dist *= -1

                act_y = p2[2] - self.point1[2]
                y_dist = abs(self.point1[2] - p2[2]) * 120 / self.img.height
                y_dist = round(y_dist)
                if (act_y > 0):
                    y_dist *= -1

                #print(x_dist, y_dist);
                distance = (x_dist ** 2 + y_dist ** 2) ** 0.5
                #print("Distance between selected points:", distance)
                arr.append((distance, x_dist, y_dist))
            arr.sort()
            for i in arr:
                print("Distance: ", i[0], "X_dist: ", i[1], "Y_dist: ", i[2])
            print("DONE")
        else:
            print("Please select two points on the image.")

    def clear(self):
        if self.point1:
            self.canvas.delete(self.point1[0])
            self.point1 = None
        for p in self.point2:
            self.canvas.delete(p[0])
        self.point2.clear()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageDistanceCalculator(root)
    root.mainloop()

