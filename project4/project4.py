import tkinter as tk
from random import randint
import numpy as np
from pprint import pprint


class TkApp:

    def __init__(self, root):

        self.root = root
        self.frame1 = tk.Frame(self.root, highlightbackground='blue', highlightthickness=5)
        self.frame1.pack()
        self.frame2 = tk.Frame(self.root)
        self.frame2.pack(fill='x')

        #Label and buttons buttons
        self.score_label = tk.Label(self.frame2)
        self.find_path_btn = tk.Button(self.frame2, text='Show largest sum path', command=self.display_max_path)
        self.refresh_grid_btn = tk.Button(self.frame2, text='Refresh grid', command=self.refresh_grid)

        #Place buttons
        self.score_label.pack()
        self.find_path_btn.pack(fill='x')
        self.refresh_grid_btn.pack(fill='x')

        self.refresh_grid()


    def refresh_grid(self):

        #Reset score label
        self.score_label['text'] = 'Maximum possible score:'

        #Create 5x5 grid
        self.grid = np.zeros((5,5)).tolist()

        #Place number buttons in the grid
        for i in range(5):
            for j in range(5):
                self.grid[i][j] = tk.Button(self.frame1, text=randint(0,9), width=5, height=2, font='Arial 12 bold')
                self.grid[i][j].bind('<Button-1>', lambda event, row=i, col=j: self.color_number_btn(row, col))
                self.grid[i][j].grid(row=i, column=j)
        
        #Get integer values from each button
        self.number_grid = []
        for row in self.grid:
            tmp_list = []
            for btn in row:
                tmp_list.append(btn['text'])
            self.number_grid.append(tmp_list)

        self.number_grid[4][0], self.number_grid[0][4] = 0, 0
 
        #Get largest sum path (but don't show yet)
        self.max_path(self.number_grid)

        self.grid[4][0]['text'], self.grid[0][4]['text'] = 'Start', 'Goal'
        self.grid[4][0].config(foreground='green3')
        self.grid[0][4].config(foreground='purple')


    def max_path(self, grid):

        """Dynamic programming approach to maximum sum path."""

        dp_matrix = np.zeros((5,5), dtype=np.int8).tolist()

        for i in reversed(range(5)):
            for j in range(5):
                if i == 4 and j == 0: continue
                elif i == 4:
                    dp_matrix[i][j] = grid[i][j] + dp_matrix[i][j-1]
                elif j == 0:
                    dp_matrix[i][j] = grid[i][j] + dp_matrix[i+1][j]
                else:
                    dp_matrix[i][j] = grid[i][j] + max(dp_matrix[i+1][j], dp_matrix[i][j-1])

        self.max_sum = dp_matrix[0][4]

        #To get the index values of the largest sum path we traceback from the end in dp_matrix
        i, j = 0, 4
        self.index_values_best_path = []
        while True:
            self.index_values_best_path.append((i, j))
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
        print(self.index_values_best_path)
        print(self.max_sum)


    def display_max_path(self):

        for i, j in self.index_values_best_path:
            self.grid[i][j].configure(bg='green')

        self.score_label['text'] = f'Maximum possible score: {self.max_sum}'


    def color_number_btn(self, row, col):

        i = row
        j = col
        curr_color = self.grid[i][j].cget("background")
        if curr_color != 'SystemButtonFace':
            self.grid[i][j].configure(bg='SystemButtonFace')
        else:
            self.grid[i][j].configure(bg='red')


    def check_user_path_correct(self):

        pass


    def exit_program(self):
        
        pass
        


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Pathfinder")

    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    x = (width / 2) - (200 / 2)
    y = (height / 2) - (420 / 2)
    root.geometry(f'{310}x{343}+{int(x)}+{int(y)}')
    root.resizable(False, False)

    pathfinder = TkApp(root)

    root.mainloop()

        