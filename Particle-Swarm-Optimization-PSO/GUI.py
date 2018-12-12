import tkinter as tk
from tkinter import filedialog
import math
import RBFN
import Car


class GUI:
    """Graphical User Interface of Car"""

    def open_data(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("text", "*.txt"), ("all files", "*.*")))
        if filename:
            self.data = self.load_data(filename)
            self.run_button['state'] = 'normal'

    def load_data(self, filename):
        data = []
        with open(filename, 'r') as file:
            for row_data in file:
                data.append([float(x) for x in row_data.rstrip('\n').split(" ")])
                #data.append(np.fromstring(row_data.rstrip('\n'), dtype=float, sep=' '))
        return data

    def draw_arrived_track(self, car_degree_list, car_loaction_list):
        size = len(car_loaction_list) - 1
        for i in range(len(car_loaction_list) - 1):
            x1 = self.origin_point_x + float(car_loaction_list[i][0]) * self.scale
            y1 = self.origin_point_y - float(car_loaction_list[i][1]) * self.scale
            x2 = self.origin_point_x + float(car_loaction_list[i+1][0]) * self.scale
            y2 = self.origin_point_y - float(car_loaction_list[i+1][1]) * self.scale
            self.car_track_canvas.create_line(x1, y1, x2, y2, fill='green', width=3)

        car_center_x = self.origin_point_x + float(car_loaction_list[size][0]) * self.scale
        car_center_y = self.origin_point_y - float(car_loaction_list[size][1]) * self.scale
        x1 = car_center_x - self.car_size * self.scale
        y1 = car_center_y - self.car_size * self.scale
        x2 = car_center_x + self.car_size * self.scale
        y2 = car_center_y + self.car_size * self.scale
        self.car_track_canvas.create_oval(x1, y1, x2, y2, outline='green', width='3')

        # Draw car direction
        direction_x = round(car_center_x + self.car_size * 2 * math.cos(math.radians(car_degree_list[size])) * self.scale, 3)
        direction_y = round(car_center_y - self.car_size * 2 * math.sin(math.radians(car_degree_list[size])) * self.scale, 3)
        self.car_track_canvas.create_line(car_center_x, car_center_y, direction_x, direction_y, fill='green', width=3)
        self.car_track_canvas.update_idletasks()

    def run(self):
        #filename = "C:/Users/pen/Desktop/OAQ.txt"
        #self.data=self.load_data(filename)
        rbfn_parameter = [self.iteration_entry.get(), self.numberOfGroup_entry.get(), self.selfWeight_entry.get(), self.socialWeight_entry.get(), self.numberOfHiddenLayerNeurons_entry.get()]
        self.rbfn = RBFN.RBFN(rbfn_parameter, self.data)
        optimal_vector = self.rbfn.train()

        self.car = Car.Car(self.car_info, self.car_size, self.rbfn, optimal_vector)
        is_arrived, wheel_degree_list, car_degree_list, car_loaction_list, distant_array = self.car.run()

        if is_arrived:
            self.draw_arrived_track(car_degree_list, car_loaction_list)
            print("error times:", self.count_error)
            print("global_min_e:", self.rbfn.pso.global_min_e)
            print("global min vector:", self.rbfn.pso.global_min_vector)
            for i in range(len(wheel_degree_list)):
                print("wheel_degree_list[" + str(i) + "]:" + str(wheel_degree_list[i]) +
                      ", car_degree_list[" + str(i) + "]:" + str(car_degree_list[i]) +
                      ", self.car_x:" + str(car_loaction_list[i][0]) +
                      " self.car_y:" + str(car_loaction_list[i][1]) +
                      ", front_distant:" + str(distant_array[i][0]) +
                      " right_distant:" + str(distant_array[i][1]) +
                      " left_distant:" + str(distant_array[i][2]))
            print('\n\n')
            self.count_error = 0
        else:
            print(self.count_error)
            self.count_error += 1
            self.run()

    def init_label(self):
        self.iteration_label = tk.Label(self.master, text='迭代次數:')
        self.number_of_group_label = tk.Label(self.master, text='族群大小:')
        self.self_weight_label = tk.Label(self.master, text='自身經驗權重:')
        self.social_weight_label = tk.Label(self.master, text='群體經驗權重:')
        self.number_of_hidden_layer_neurons_label = tk.Label(self.master, text='隱藏層神經元個數:')

    def init_entry(self):
        var_iteration = tk.StringVar()
        var_numberOfGroup = tk.StringVar()
        var_selfWeight = tk.StringVar()
        var_socialWeight = tk.StringVar()
        var_numberOfHiddenLayerNeurons = tk.StringVar()

        var_iteration.set('3')
        var_numberOfGroup.set('5')
        var_selfWeight.set('0.6')
        var_socialWeight.set('0.4')
        var_numberOfHiddenLayerNeurons.set('8')

        self.iteration_entry = tk.Entry(self.master, textvariable=var_iteration)
        self.numberOfGroup_entry = tk.Entry(self.master, textvariable=var_numberOfGroup)
        self.selfWeight_entry = tk.Entry(self.master, textvariable=var_selfWeight)
        self.socialWeight_entry = tk.Entry(self.master, textvariable=var_socialWeight)
        self.numberOfHiddenLayerNeurons_entry = tk.Entry(self.master, textvariable=var_numberOfHiddenLayerNeurons)

    def init_button(self):
        self.open_file_buttion = tk.Button(self.master, text='開啟檔案', command=self.open_data, width=10)
        self.run_button = tk.Button(self.master, text='Run', command=self.run, width=10, state='disabled')

    def place_component(self):
        # layout 12*2(row*column)
        spacing = 30
        first_row = 20
        first_column = 20
        second_column = 520
        third_column = 650

        # first row
        self.car_track_canvas.place(x=first_column, y=first_row)
        self.iteration_label.place(x=second_column, y=first_row)
        self.iteration_entry.place(x=third_column, y=first_row)
        # second row
        self.number_of_group_label.place(x=second_column, y=first_row + spacing)
        self.numberOfGroup_entry.place(x=third_column, y=first_row + spacing)
        # third row
        self.self_weight_label.place(x=second_column, y=first_row + spacing * 2)
        self.selfWeight_entry.place(x=third_column, y=first_row + spacing * 2)
        # 4th row
        self.social_weight_label.place(x=second_column, y=first_row + spacing * 3)
        self.socialWeight_entry.place(x=third_column, y=first_row + spacing * 3)
        # 5th row
        self.number_of_hidden_layer_neurons_label.place(x=second_column, y=first_row + spacing * 4)
        self.numberOfHiddenLayerNeurons_entry.place(x=third_column, y=first_row + spacing * 4)
        # 6th row
        self.open_file_buttion.place(x=second_column, y=first_row + spacing * 5)
        self.run_button.place(x=third_column + spacing * 2, y=first_row + spacing * 5)

    def draw_car_track(self):
        car_x = 0
        car_y = 0
        degree = 90
        left_top = [18, 40]
        right_down = [30, 37]
        lan_border = [[-6, -3], [-6, 22], [18, 22], [18, 50], [30, 50], [30, 10], [6, 10], [6, -6], [-6, -3]]

        self.car_info =[[0, 0, 90]]
        self.car_info.append(left_top)
        self.car_info.append(right_down)
        for item in lan_border:
            self.car_info.append(item)
        #print(self.car_info)

        # Draw X-axis and Y-axis
        axis_width = 1
        self.origin_point_y = self.canvas_height / 2
        self.car_track_canvas.create_line(0, self.origin_point_y, self.canvas_width, self.origin_point_y, width=axis_width)
        self.origin_point_x = self.canvas_width / 2
        self.car_track_canvas.create_line(self.origin_point_x, 0, self.origin_point_x, self.canvas_height, width=axis_width)

        # Draw lan
        for i in range(0, len(lan_border)-1):
            x1 = self.origin_point_x + lan_border[i][0] * self.scale
            y1 = self.origin_point_y - lan_border[i][1] * self.scale
            x2 = self.origin_point_x + lan_border[i+1][0] * self.scale
            y2 = self.origin_point_y - lan_border[i+1][1] * self.scale
            self.car_track_canvas.create_line(x1, y1, x2, y2, fill='blue', width=3)

        # Draw end area
        left_top_x = self.origin_point_x + left_top[0] * self.scale
        left_top_y = self.origin_point_y - left_top[1] * self.scale
        right_down_x = self.origin_point_x + right_down[0] * self.scale
        right_down_y = self.origin_point_y - right_down[1] * self.scale
        self.car_track_canvas.create_rectangle(left_top_x, left_top_y, right_down_x, right_down_y, outline='red', fill='red')

        # Draw car
        car_center_x = self.origin_point_x + car_x * self.scale
        car_center_y = self.origin_point_y - car_y * self.scale
        x1 = car_center_x - self.car_size * self.scale
        y1 = car_center_y - self.car_size * self.scale
        x2 = car_center_x + self.car_size * self.scale
        y2 = car_center_y + self.car_size * self.scale
        self.car_track_canvas.create_oval(x1, y1, x2, y2, outline='green', width='3')

        # Draw car direction
        direction_x = round(car_center_x + self.car_size * 2 * math.cos(math.radians(degree)) * self.scale, 3)
        direction_y = round(car_center_y - self.car_size * 2 * math.sin(math.radians(degree)) * self.scale, 3)
        self.car_track_canvas.create_line(car_center_x, car_center_y, direction_x, direction_y, fill='green', width=3)

    def __init__(self, master):
        self.master = master
        master.title('Car Application')
        master.geometry('1366x768')

        # Initial layout component
        self.canvas_height = 640
        self.canvas_width = 480
        self.car_track_canvas = tk.Canvas(master, height=self.canvas_height, width=self.canvas_width, bd=2, relief='solid')

        self.init_label()
        self.init_entry()
        self.init_button()
        self.place_component()

        # Initial car feature in the beginning
        self.scale = 6
        self.car_size = 3

        self.draw_car_track()

        self.count_error = 0
