import random
import math
import GA
import time


class RBFN:

    def normalize_data(self, data):
        start_index = 0
        if self.inputDimension == 5:
            start_index = 2
        for i in range(start_index, self.inputDimension):
            if data[i] < 40:
                data[i] = data[i] / 40 - 1
            else:
                data[i] = data[i] / 40
        return data

    def normalize_input_data(self, input_data):
        for i in range(len(input_data)):
            input_data[i] = self.normalize_data(input_data[i])
            input_data[i][self.inputDimension] /= 40
        return input_data

    def anti_normalization_f(self, f):
        degree = f * 40
        if degree > 40:
            degree = 40.0
        if degree < -40:
            degree = -40.0
        return degree

    def calcu_F(self, vector, input_x):
        #print("vector:", vector)
        #print("input_x:", input_x)
        #print("type(vector):", type(vector))
        #print("type(input_x):", type(input_x))

        sum_f = 0.0
        for i in range(self.hiddenNeurons):
            neuron_ith_m_start_index = 1 + self.hiddenNeurons + i * self.inputDimension
            m = vector[neuron_ith_m_start_index: neuron_ith_m_start_index + self.inputDimension]
            sigma = vector[self.vectorDimension - self.hiddenNeurons + i]
            #print("m:", m)
            #print("sigma:", sigma)

            '''
            print("m[0]:", m[0])
            print("type(m[0]:", type(m[0]))
            print("type(m):", type(m))
            print("type(sigma):", type(sigma))
            print("input_x[0]:", input_x[0])
            print("type(input_x[0]):", type(input_x[0]))
            '''

            # gaussian
            sum = 0.0
            for j in range(self.inputDimension):
                sum += (input_x[j] - m[j]) * (input_x[j] - m[j])
            sum = sum * -1
            self.phi[i + 1] = math.exp(float(sum) / float(2 * sigma * sigma))

            # accumulator
            sum_f += vector[i] * self.phi[i]

        sum_f += vector[self.hiddenNeurons] * self.phi[self.hiddenNeurons]
        return sum_f

    def calcu_fitness(self, y, f):
        sum = 0
        for i in range(self.input_length):
            sum += (y[i] - f[i]) * (y[i] - f[i])
        sum /= 2
        return sum
        #return (np.power(y - f, 2)).sum() / 2

    def train(self):
        start_time = time.clock()
        for i in range(self.iteration):  # 執行設定的迭代次數，期望得到的E越好越好
            #iteration_start_time = time.clock()
            for j in range(self.groupNumber):
                #one_input_start_time = time.clock()
                for l in range(self.input_length):
                    #calcu_F_start_time = time.clock()
                    self.F[l] = self.calcu_F(self.individual_vector[j], self.input_x[l])
                    #calcu_F_end_time = time.clock()
                    #print("calcu_F execution time:", calcu_F_end_time - calcu_F_start_time)

                #fitness_start_time = time.clock()
                self.E[j] = self.calcu_fitness(self.input_y, self.F)
                #fitness_end_time = time.clock()
                #print("e execution time:", fitness_end_time - fitness_start_time)

                #one_input_end_time = time.clock()
                #print("one input execution time:", one_input_end_time - one_input_start_time)

            '''
            print("e:", e)
            print("individual_vector:", self.individual_vector)
            print("pso.global_min_e:", self.pso.global_min_e)
            print("pso.global_min_vector:", self.pso.global_min_vector)
            print("pso.individual_min_e:", self.pso.individual_min_e)
            print("pso.individual_min_vector:", self.pso.individual_min_vector)
            '''

            #ga_update_start_time = time.clock()
            # print("individual_vector:", self.individual_vector)
            self.individual_vector = self.ga.update_vector(self.E, self.individual_vector)
            #print("update individual_vector:", self.individual_vector)
            #ga_update_end_time = time.clock()
            #print("ga_update execution time:", ga_update_end_time - ga_update_start_time)

            #iteration_end_time = time.clock()
            #print("once iteration execution time:", iteration_end_time - iteration_start_time)

        end_time = time.clock()
        print("train execution time:", end_time - start_time)
        #print("ga.global_min_vector:", self.ga.global_min_vector)
        return self.ga.global_min_vector

    def test(self, car_data, optimal_vector):
        #print("car_data:", car_data)
        normalized_car_data = self.normalize_data(car_data)
        #print("After normalized car_data:", normalized_car_data)

        #print("optimal_vector:", optimal_vector)

        #os.system("pause")
        f = self.calcu_F(optimal_vector, normalized_car_data)
        #print("f:", f)
        steering_wheel_degree = self.anti_normalization_f(f)
        #print("steering_wheel_degree:", steering_wheel_degree)
        return steering_wheel_degree

    def __init__(self, rbfn_parameter, data):
        # set parameters
        self.iteration = int(rbfn_parameter[0])
        self.groupNumber = int(rbfn_parameter[1])
        self.matingProbability = float(rbfn_parameter[2])
        self.mutationProbability = float(rbfn_parameter[3])
        self.hiddenNeurons = int(rbfn_parameter[4])

        # process input data
        self.input_length = len(data)
        self.inputDimension = len(data[0]) - 1
        #np.random.shuffle(data)
        #print("data[5]:", data[5])
        self.data = self.normalize_input_data(data)
        #print("normalize data[5]:", self.data[5])
        self.input_x = [[0.] * self.inputDimension] * self.input_length
        self.input_y = []
        for i in range(self.input_length):
            for j in range(self.inputDimension):
                self.input_x[i][j] = self.data[i][j]
            self.input_y.append(self.data[i][self.inputDimension])
        self.vectorDimension = 1 + 2 * self.hiddenNeurons + self.hiddenNeurons * self.inputDimension

        # initial groups
        # 個體向量
        self.individual_vector = \
            [[random.uniform(-1, 1) for col in range(self.vectorDimension)] for row in range(self.groupNumber)]
        # 個體向量中sigma為正
        for i in range(self.groupNumber):
            for j in range(self.vectorDimension - self.hiddenNeurons, self.vectorDimension):
                while self.individual_vector[i][j] == 0.0:
                    self.individual_vector[i][j] = random.random()
                if self.individual_vector[i][j] < 0:
                    self.individual_vector[i][j] *= -1

        # initial F、E
        self.F = [0.] * self.input_length
        self.E = [0.] * self.groupNumber
        self.phi = [1.] * (self.hiddenNeurons + 1)

        # initial pso
        self.ga = GA.GA(self.groupNumber, self.matingProbability, self.mutationProbability,
                        self.hiddenNeurons, self.inputDimension, self.vectorDimension)
