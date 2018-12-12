import random
import sys


class GA:

    def crossover_swap(self, a, b):
        temp = a
        a = b
        b = temp

    def update_vector(self, e, individual_vector):
        #print("e:", e)

        sorted_e_indices = sorted(range(self.groupNumber), key=lambda k: e[k])  # the indices of sorted vector e
        # print("sorted_e_indices:", sorted_e_indices)

        # update global optimal
        if e[sorted_e_indices[0]] < self.global_min_e:
            self.global_min_e = e[sorted_e_indices[0]]
            self.global_min_vector = individual_vector[sorted_e_indices[0]]
        #print("global_min_vector:", self.global_min_vector)

        # reproduction (Roulette)
        sum_e = 0
        for i in range(self.groupNumber):
            sum_e += 1 / e[i]  # total of e vector
        sum_e = 1 / sum_e
        #print("sum_e:", sum_e)
        for i in range(self.groupNumber):
            self.reproduction_rate[i] = round(1 / e[i] * sum_e, 2)
        #print("reproduction_rate:", self.reproduction_rate)
        start_index = 0
        sum_number_reproduction = 0
        for index in sorted_e_indices:
            sum_number_reproduction += int(round(self.reproduction_rate[index] * self.groupNumber, 0))
            #print("sum_number_reproduction:", sum_number_reproduction)
            if sum_number_reproduction == start_index:
                sum_number_reproduction += 1
            if sum_number_reproduction > self.groupNumber:
                sum_number_reproduction = self.groupNumber
            for j in range(start_index, sum_number_reproduction):
                self.mating_pool[j] = individual_vector[index]
            if sum_number_reproduction == self.groupNumber:
                break
            start_index = sum_number_reproduction
            #print("start_index:", start_index)
        #for i in range(self.groupNumber):
            #print("mating_pool[", i, "]:", self.mating_pool[i])

        # crossover
        number_crossover = int(self.groupNumber * self.matingProbability)
        start_range = random.randint(0, self.vectorDimension - 1)
        end_range = random.randint(0, self.vectorDimension - 1)
        for i in range(number_crossover):
            male_index = random.randint(0, self.groupNumber - 1)
            female_index = random.randint(0, self.groupNumber - 1)
            if start_range > end_range:
                for j in range(start_range, self.vectorDimension):
                    self.crossover_swap(self.mating_pool[male_index][j], self.mating_pool[female_index][j])
                for j in range(0, end_range):
                    self.crossover_swap(self.mating_pool[male_index][j], self.mating_pool[female_index][j])
            else:
                for j in range(start_range, end_range):
                    self.crossover_swap(individual_vector[male_index][j], individual_vector[female_index][j])

        # mutation
        number_mutation = int(self.groupNumber * self.mutationProbability)
        if number_mutation <= 0:
            number_mutation = 1
        for i in range(number_mutation):
            mutation_index = random.randint(0, self.groupNumber - 1)
            self.mating_pool[mutation_index][1] = random.uniform(-1, 1)
            self.mating_pool[mutation_index][self.vectorDimension-1] = random.random()
            while self.mating_pool[mutation_index][self.vectorDimension - 1] == 0:
                self.mating_pool[mutation_index][self.vectorDimension - 1] = random.random()
            if self.mating_pool[mutation_index][self.vectorDimension - 1] < 0:
                self.mating_pool[mutation_index][self.vectorDimension - 1] *= -1

        # update individual vector
        for i in range(self.groupNumber):
            individual_vector[i] = self.mating_pool[i]
            #print("individual_vector[", i, "]:", individual_vector[i])

        #os.system("pause")
        return individual_vector

    def __init__(self, groupNumber, matingProbability, mutationProbability, hiddenNeurons, inputDimension, vectorDimension):
        # set parameters
        self.groupNumber = groupNumber
        self.matingProbability = matingProbability
        self.mutationProbability = mutationProbability
        self.hiddenNeurons = hiddenNeurons
        self.inputDimension = inputDimension
        self.vectorDimension = vectorDimension

        # initial ga global optimal, mating_pool 初始化族群最佳、交配池
        self.global_min_e = sys.maxsize  # global optimal 族群中最佳適應值(E最小)
        self.global_min_vector = [0.] * self.vectorDimension  # 族群最佳向量(最佳鍵結值向量)
        self.reproduction_rate = [0.] * self.groupNumber  # 複製機率
        self.mating_pool = [[0.] * self.vectorDimension] * self.groupNumber  # 交配池

