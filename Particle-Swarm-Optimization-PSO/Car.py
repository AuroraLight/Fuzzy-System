import sys
import math


class Car:

    # calculate the constant b of the linear equation
    def calculate_b(self, x, y, m):
        if m == 0:
            b = y
        elif m == 9999:
            b = x
        else:
            b = y - m * x
        return b

    # calculate slope
    def calculate_m(self, x1, y1, x2, y2):
        x_diff = x2 - x1
        y_diff = y2 - y1
        m = 0  # y = ? Horizontal line
        if x_diff != 0:
            m = round(y_diff / x_diff, 3)  # slope
        elif x_diff == 0:
            m = 9999  # x = ? Vertical line
        return m

    def find_intersection(self, m, b):
        cross_index = []
        for i in range(len(self.lan) - 1):
            if m == 9999:
                if (self.lan[i][0] >= b and self.lan[i+1][0] < b)\
                        or (self.lan[i][0] <= b and self.lan[i+1][0] > b):
                    cross_index.append(i)
                    cross_index.append(i+1)
            elif (m * self.lan[i][0] + b >= float(self.lan[i][1]) and m * self.lan[i+1][0] + b <= float(self.lan[i+1][1])) \
                    or (m * self.lan[i][0] + b <= float(self.lan[i][1]) and m * self.lan[i+1][0] + b >= float(self.lan[i+1][1])):
                cross_index.append(i)
                cross_index.append(i+1)
        #print('cross_index: ' + str(cross_index))
        return cross_index

    def calculate_distant(self, cross_index, m, b, direction_x, direction_y):
        distant = sys.maxsize
        temp_x1 = direction_x - self.car_x
        temp_y1 = direction_y - self.car_y
        #print('temp_x1: ' + str(temp_x1))
        #print('temp_y1: ' + str(temp_y1))
        for i in range(0, len(cross_index), 2):
            cross_m = self.calculate_m(self.lan[cross_index[i]][0], self.lan[cross_index[i]][1], self.lan[cross_index[i+1]][0], self.lan[cross_index[i+1]][1])
            cross_b = self.calculate_b(self.lan[cross_index[i]][0], self.lan[cross_index[i]][1], cross_m)
            #print('cross_m: ' + str(cross_m))
            #print('cross_b: ' + str(cross_b))
            if m == 0 and cross_m == 9999:  # Horizontal line and Vertical line
                cross_x = cross_b
                cross_y = b
            elif m == 9999 and cross_m == 0:  # Vertical line and Horizontal line
                cross_x = b
                cross_y = cross_b
            elif m == 0 and cross_m != 9999:  # Horizontal line and normal line
                cross_x = round((b - cross_b) / cross_m, 3)
                cross_y = b
            elif m == 9999 and cross_m != 0:  # Vertical line and normal line
                cross_x = b
                cross_y = cross_m * b + cross_b
            elif cross_m == 0:  # normal line and Horizontal line
                cross_x = round((cross_b - b) / m, 3)
                cross_y = cross_b
            elif cross_m == 9999:  # normal line and Vertical line
                cross_x = cross_b
                cross_y = m * cross_b + b
            else:  # normal line and normal line
                cross_x = round((cross_b - b) / (m - cross_m), 3)
                cross_y = cross_m * cross_x + cross_b
            #print('cross_x: ' + str(cross_x))
            #print('cross_y: ' + str(cross_y))
            temp_x2 = cross_x - self.car_x
            temp_y2 = cross_y - self.car_y
            #print('temp_x2: ' + str(temp_x2))
            #print('temp_y2: ' + str(temp_y2))
            if (temp_x1 >= 0 and temp_y1 >= 0 and temp_x2 >= 0 and temp_y2 >= 0) \
                    or (temp_x1 < 0 and temp_y1 >= 0 and temp_x2 < 0 and temp_y2 >= 0) \
                    or (temp_x1 >= 0 and temp_y1 < 0 and temp_x2 >= 0 and temp_y2 < 0) \
                    or (temp_x1 < 0 and temp_y1 < 0 and temp_x2 < 0 and temp_y2 < 0):
                temp_d = math.sqrt(pow((cross_x - direction_x), 2) + pow((cross_y - direction_y), 2))
                #print('temp_d: ' + str(temp_d))
                if temp_d < distant:
                    distant = temp_d
        return distant

    def get_distant(self, degree):
        sensor_direction_x = round(self.car_x + self.car_size * math.cos(math.radians(degree)), 3)
        sensor_direction_y = round(self.car_y + self.car_size * math.sin(math.radians(degree)), 3)
        #print('sensor_direction_x: ' + str(sensor_direction_x))
        #print('sensor_direction_y: ' + str(sensor_direction_y))

        # car sensor linear equation y = sensor_m * x + sensor_b
        sensor_m = self.calculate_m(self.car_x, self.car_y, sensor_direction_x, sensor_direction_y)
        sensor_b = self.calculate_b(self.car_x, self.car_y, sensor_m)
        #print('sensor_m: ' + str(sensor_m))
        #print('sensor_b: ' + str(sensor_b))

        sensor_cross_index = self.find_intersection(sensor_m, sensor_b)
        #print('sensor_cross_index: ' + str(sensor_cross_index))

        # Get the distant of the sensor
        sensor_distant = self.calculate_distant(sensor_cross_index, sensor_m, sensor_b, sensor_direction_x, sensor_direction_y)
        #print('sensor_distant: ' + str(sensor_distant))
        return sensor_distant

    def get_sensor_data(self):
        #print('self.degree: ' + str(self.degree))
        front_distant = self.get_distant(self.degree)
        right_distant = self.get_distant(self.degree - 45)
        left_distant = self.get_distant(self.degree + 45)
        #print('front_distant: ' + str(front_distant))
        #print('right_distant: ' + str(right_distant))
        #print('left_distnat: ' + str(left_distant))
        return front_distant, right_distant, left_distant

    def judge_arrive(self):
        if self.car_x >= float(self.end_area[0][0]) and self.car_x <= float(self.end_area[1][0]) \
            and self.car_y <= float(self.end_area[0][1]) and self.car_y >= float(self.end_area[1][1]):
            return True
        return False

    def get_next_wheel_degree(self, front_distant, right_distant, left_distant):
        if self.input_dimension == 3:
            car_data = [front_distant, right_distant, left_distant]
        if self.input_dimension == 5:
            car_data = [self.car_x, self.car_y, front_distant, right_distant, left_distant]
        return self.fine_train_rbfn.test(car_data, self.optimal_vector)

    def run(self):
        arrive = False
        distant_array = []
        car_degree_list = []
        car_degree_list.append(self.degree)
        wheel_degree_list = []
        wheel_degree_list.append(0)
        car_location_list = []
        car_location_list.append([self.car_x, self.car_y])
        count = 0
        while not arrive:
            front_distant, right_distant, left_distant = self.get_sensor_data()
            distant_array.append([front_distant, right_distant, left_distant])
            if front_distant == sys.maxsize or right_distant == sys.maxsize or left_distant == sys.maxsize:
                #print('Car drives out of the driveway!!!')
                break
            #if front_distant < 2 or right_distant < 2 or left_distant < 2:
                # print('Car drives out of the driveway!!!')
                #break

            steering_wheel_degree = self.get_next_wheel_degree(front_distant, right_distant, left_distant)
            wheel_degree_list.append(steering_wheel_degree)
            #print('steering_wheel_degree: ' + str(steering_wheel_degree))
            # move
            self.car_x += round(math.cos(math.radians(self.degree + steering_wheel_degree)) +
                math.sin(math.radians(steering_wheel_degree*-1)) * math.sin(math.radians(self.degree)), 8)
            self.car_y += round(math.sin(math.radians(self.degree + steering_wheel_degree)) -
                math.sin(math.radians(steering_wheel_degree*-1)) * math.cos(math.radians(self.degree)), 8)
            #print('self.car_x: ' + str(self.car_x))
            #print('self.car_y: ' + str(self.car_y))

            car_location_list.append([self.car_x, self.car_y])
            self.degree -= math.degrees(math.asin(2*math.sin(math.radians(steering_wheel_degree*-1)) / (self.car_size*2)))
            if self.degree >= 270:
                self.degree -= 360
            if self.degree <= -90:
                self.degree += 360
            car_degree_list.append(self.degree)
            #print('self.degree: ', self.degree)

            arrive = self.judge_arrive()
            if arrive:
                front_distant, right_distant, left_distant = self.get_sensor_data()
                distant_array.append([front_distant, right_distant, left_distant])
            count += 1
            if count > 10000:
                break

            #print('count: ', count, '\n\n')
        return arrive, wheel_degree_list, car_degree_list, car_location_list, distant_array

    def __init__(self, info, car_size, fine_train_rbfn, optimal_vector):
        self.car_x, self.car_y, self.degree = info[0][0], info[0][1], info[0][2]
        self.end_area = info[1:3]
        self.lan = info[3:]
        self.car_size = car_size

        self.fine_train_rbfn = fine_train_rbfn
        self.input_dimension = fine_train_rbfn.inputDimension
        self.optimal_vector = optimal_vector
