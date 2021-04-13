import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from random import randint
import numpy as np
from pprint import pprint


class TkApp:

    def __init__(self, root):

        self.root = root
        self.frame1 = tk.Frame(self.root, highlightbackground='#1f2b38', highlightthickness=12)
        self.frame1.pack()
        self.frame2 = tk.Frame(self.root)
        self.frame2.pack(fill='x')
        self.frame3 = tk.Frame(self.root)
        self.frame3.pack(fill='x')

        #Canvas, label and buttons
        self.canvas = tk.Canvas(self.frame1, width=440, height=360)
        self.score_label = ttk.Label(self.frame2)
        self.find_path_btn = ttk.Button(self.frame3, width=37, text='Show largest sum path', command=self.display_max_path)
        self.refresh_grid_btn = ttk.Button(self.frame3, width=37, text='Refresh grid', command=self.refresh_grid)

        #Place canvas/widgets
        self.canvas.pack()
        self.score_label.pack()
        self.find_path_btn.grid(row=0, column=0)
        self.refresh_grid_btn.grid(row=0, column=1)

        self.refresh_grid()


    def refresh_grid(self):

        #Destroy and remake canvas to preserve item IDs in canvas
        self.canvas.destroy()
        self.canvas = tk.Canvas(self.frame1, width=440, height=360)
        self.canvas.bind("<ButtonPress-1>", self.color_rectangle_on_click)
        self.canvas.pack()

        #Reset score label
        self.score_label['text'] = 'Maximum possible score:'

        #Create 5x5 grid
        self.grid = np.random.randint(10, size=(5,5)).tolist()
        self.grid[4][0], self.grid[0][4] = 'Start', 'Goal'

        #Create rectangle grid with numbers in canvas
        for i in range(0, 440, 88):
            for j in range(0, 360, 72):
                self.canvas.create_rectangle(i, j, i+90, j+74, outline='black', fill='white')

        for j in range(5):
            for i in range(5):
                self.canvas.create_text(j*88+44, i*72+36, text=self.grid[i][j], font='Arial 14 bold')
       
        self.canvas.itemconfig(30, fill='green3')
        self.canvas.itemconfig(46, fill='red1')
 
        #Get largest sum path (but don't show yet)
        self.max_path()


    def max_path(self):

        """Dynamic programming approach to maximum sum path."""

        self.grid[4][0], self.grid[0][4] = 0, 0

        dp_matrix = np.zeros((5,5), dtype=np.int8).tolist()

        for i in reversed(range(5)):
            for j in range(5):
                if i == 4 and j == 0: continue
                elif i == 4:
                    dp_matrix[i][j] = self.grid[i][j] + dp_matrix[i][j-1]
                elif j == 0:
                    dp_matrix[i][j] = self.grid[i][j] + dp_matrix[i+1][j]
                else:
                    dp_matrix[i][j] = self.grid[i][j] + max(dp_matrix[i+1][j], dp_matrix[i][j-1])

        self.max_sum = dp_matrix[0][4]

        #To get the index values of the largest sum path, in dp_matrix we traceback from the end to start
        i, j = 0, 4
        self.largest_path = []
        while True:
            self.largest_path.append(j*5 + (i+1))
            if i == 4 and j == 0: break
            if i == 4: j -= 1
            elif j == 0: i += 1
            else:
                value_left = dp_matrix[i][j-1]
                value_down = dp_matrix[i+1][j]
                if value_left > value_down:
                    j -= 1 
                else:
                    i += 1
        

        pprint(dp_matrix)
        print(self.largest_path)
        print(self.max_sum)


    def display_max_path(self):

        for i in self.largest_path:
            self.canvas.itemconfig(i, fill='yellow')
            self.canvas.itemconfig(i + 25, fill='blue')

        self.score_label['text'] = f'Maximum possible score: {self.max_sum}'


    def color_rectangle_on_click(self, event):

        rect_id = self.canvas.find_closest(event.x, event.y)[0]
        color = self.canvas.itemcget(rect_id, "fill")
        unclicked_colors = ['white', 'black', 'green3', 'red1']
        if color in unclicked_colors:
            if rect_id > 25:
                self.canvas.itemconfig(rect_id - 25, fill='#FF717E')
                self.canvas.itemconfig(rect_id, fill='blue')
            else:
                self.canvas.itemconfig(rect_id, fill='#FF717E')
                self.canvas.itemconfig(rect_id + 25, fill='blue') 
        else:
            if rect_id > 25:
                self.canvas.itemconfig(rect_id - 25, fill='white')
                self.canvas.itemconfig(rect_id, fill='black')
            else:
                self.canvas.itemconfig(rect_id, fill='white')
                self.canvas.itemconfig(rect_id + 25, fill='black') 



if __name__ == '__main__':
    root = ThemedTk(theme='vista')
    root.title("Pathfinder")

    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    x = (width / 2) - (463 / 2)
    y = (height / 2) - (433 / 2)
    root.geometry(f'{464}x{433}+{int(x)}+{int(y)}')
    root.resizable(False, False)

    pathfinder = TkApp(root)
    root.mainloop()
