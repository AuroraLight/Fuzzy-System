import random
import sys


class PSO:

    def update_individual_vector(self, individual_vector):
        for i in range(self.groupNumber):
            for j in range(self.vectorDimension):
                self.individual_velocity[i][j] += \
                    self.selfWeight * (self.individual_min_vector[i][j] - individual_vector[i][j]) + \
                    self.socialWeight * (self.global_min_vector[j] - individual_vector[i][j])

                individual_vector[i][j] += self.individual_velocity[i][j]

    def update_min_vector(self, e, individual_vector):
        for i in range(self.groupNumber):
            if e[i] < self.individual_min_e[i]:  # update individual optimal
                self.individual_min_e[i] = e[i]
                self.individual_min_vector[i] = individual_vector[i]
            if e[i] < self.global_min_e:  # update global optimal
                self.global_min_e = e[i]
                self.global_min_vector = individual_vector[i]

    def __init__(self, groupNumber, selfWeight, socialWeight, hiddenNeurons, inputDimension, vectorDimension):
        # set parameters
        self.groupNumber = groupNumber
        self.selfWeight = selfWeight
        self.socialWeight = socialWeight
        self.hiddenNeurons = hiddenNeurons
        self.inputDimension = inputDimension
        self.vectorDimension = vectorDimension

        # initial pso v, global optimal, individual optimal 初始化族群最佳、個體最佳、速度
        self.global_min_e = sys.maxsize  # global optimal 族群中最佳適應值(E最小)
        self.global_min_vector = [0.] * self.vectorDimension  # 族群最佳向量(最佳鍵結值向量)
        self.individual_min_e = [100.0] * self.groupNumber  # individual optimal 個體最佳E
        self.individual_min_vector = [[0.] * self.vectorDimension] * self.groupNumber  # 個體最佳向量
        # 個體速度
        self.individual_velocity = \
            [[random.uniform(-1, 1) for col in range(self.vectorDimension)] for row in range(self.groupNumber)]
        # 個體速度向量中的sigma為正
        for i in range(self.groupNumber):
            for j in range(self.vectorDimension - self.hiddenNeurons, self.vectorDimension):
                while self.individual_velocity[i][j] == 0.0:
                    self.individual_velocity[i][j] = random.random()
                if self.individual_velocity[i][j] < 0.:
                    self.individual_velocity[i][j] *= -1
