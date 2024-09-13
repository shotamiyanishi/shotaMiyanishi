import numpy as np

from benchmarks import Sphere, Rastrigin, RozenBlock

def evaluate(func, poplation):
    pop_size = len(poplation)
    for i in range(pop_size):
        eval = func(poplation[i].get_x())
        poplation[i].set_eval(eval)
        

class solution:
    def __init__(self, dim):
        self.x = np.zeros(dim)
        self.z = np.zeros(dim)
        self.dim = dim
        self.eval = 0.0
            
    def __str__(self):
        sol = "個体：["
        for i in range(self.dim):
            if not i == self.dim - 1:
                sol += str (self.x[i]) + ", "
            else:
                sol += str (self.x[i]) + " ]\n"
                
        sol += f"評価値：{self.eval}"
        return sol
    
    def __lt__(self, other):
        if self.eval == float("inf") and other.eval == float("inf"):
            return np.linalg.norm(self.get_z()) < np.linalg.norm(other.get_z())
        return self.eval < other.eval
    
    def get_z(self):
        return self.z
    
    def set_z(self, z):
        self.z = z
    
    def get_x(self):
        return self.x

    def set_x(self, x):
        self.x = x
        
    def set_eval(self, eval):
        self.eval = eval
        
    def get_eval(self):
        return self.eval
    
class dxnes:
    def __init__(self, dim, pop_size, m, sigma, seed):
        np.random.seed(seed)
        #集団の保持
        self.population = []
        for _ in range(pop_size):
            sol = solution(dim)
            self.population.append(sol)
        #集団サイズ
        self.pop_size = pop_size
        #次元数
        self.dim = dim
        #平均ベクトル，ステップサイズ，正規化変換行列
        self.m = np.ones(dim) * m
        self.sigma = sigma
        self.B = np.eye(dim)
        
        #重みの初期化
        self.w = np.zeros(self.pop_size)
        
        #rankベースの重みの初期化
        self.w_hat = np.zeros(pop_size)
        self.w_rank = np.zeros(pop_size)
        for i in range(pop_size):
            tmp_value = np.log((float(pop_size) / 2.0) + 1.0) - np.log(i + 1)
            if 0.0 < tmp_value:
                self.w_hat[i] = tmp_value
                
        sum = float (self.w_hat.sum())        
        for i in range(pop_size):
            self.w_rank[i] = (self.w_hat[i] / sum) - (1.0 / float(pop_size))
            
        #distベースの重みの初期化
        self.w_dist = np.zeros(pop_size)
            
        #h^(-1)(n)の計算をニュートン法を用いて行う．
        a = 1.0
        for i in range(1000):
            tmp_1 = (1.0 + float(a ** 2)) * np.exp(float(a ** 2) / 2.0)
            tmp_1 = (tmp_1 / 0.24) - 10.0
            tmp_1 = tmp_1 - float(self.dim)
            tmp_2 = float (a) * float(a ** 2) * np.exp(float(a ** 2) / 2.0)
            tmp_2 = tmp_2 / 0.12
            a = a - float(tmp_1) / float(tmp_2)
        
        self.n_inv = a
        
        #alphaの計算を行う．
        self.alpha = 1.0 * self.n_inv
        if np.sqrt(float(pop_size)/ float(dim)) < 1.0:
            self.alpha = self.n_inv * np.sqrt(float(pop_size)/ float(dim))
            
        #学習率の設定を行う．
        #平均ベクトルの学習率
        self.Eta_m = 1.0
        
        #正規化変換行列の学習率
        self.Eta_B = 0.0
        self.Eta_B_move = (float(pop_size) + 2.0 * float(dim)) / (float(pop_size) + 2.0 * float(dim) * float(dim) + 100.0)
        
        if np.sqrt(float(pop_size)/ float(dim)) < 1.0:
            self.Eta_B_move = self.Eta_B_move * np.sqrt(float(pop_size)/ float(dim)) 
        
        self.Eta_B_stag = (float(pop_size)) / (float(pop_size) + 2.0 * float(dim) * float(dim) + 100.0)
        self.Eta_B_conv = (float(pop_size)) / (float(pop_size) + 2.0 * float(dim) * float(dim) + 100.0)
        
        #ステップサイズの学習率
        self.Eta_sigma = 0.0
        self.Eta_sigma_move = 1.0
        self.Eta_sigma_stag = 0.5 * (1.0 + (float(pop_size) / (float(pop_size) + 2.0 * float(dim))))
        self.Eta_sigma_conv = 2.0 * self.Eta_sigma_stag
        
        #c_sigmaの初期化
        mu_eff = 0.0
        for i in range(pop_size):
            mu_eff += (float(self.w_rank[i]) + (1.0 / float(self.pop_size))) * (float(self.w_rank[i]) + (1.0 / float(self.pop_size)))
        
        self.mu_eff = 1.0 / mu_eff
        
        tmp_1 = 1.0 / (2.0 * np.log(float(dim) + 1.0))
        tmp_2 = (self.mu_eff + 2.0) / (float(dim) + self.mu_eff + 5.0)   
        
        self.c_sigma = tmp_1 * tmp_2
        
        #進化パスの初期化
        self.p_sigma = np.zeros(dim)
        
        #ε(フェーズの判定に用いる閾値)→重み，学習率の決定に用いる
        self.epsilon = np.sqrt(dim) * (1.0 - (1.0 / (4.0 * float(dim))) + (1.0 / (21.0 * float (dim) * float (dim))))
        
        #自然勾配の計算に用いるパラメータ
        self.G_B = np.eye(dim)
        self.G_M = np.eye(dim)
        self.G_delta = np.zeros(dim)
        self.G_sigma = 0.0

        #計算用の行列，ベクトル
        self.vecter = np.zeros(dim)
        self.matrix = np.eye(dim)
        
    #個体のサンプリングを行う．     
    def sampling(self):
        count = int (self.pop_size / 2)
        for i in range(count):
            z = np.random.normal(0.0, 1.0, self.dim)
            self.population[2 * i].z = z
            self.population[2 * i].x = self.sigma *  np.real(np.dot(self.B, z)) + self.m
            
            z = -1.0 * z
            self.population[2 * i + 1].z = z
            self.population[2 * i + 1].x = self.sigma *  np.dot(self.B, z) + self.m
            #print(self.population[2 * i + 1].x)
            
    #集団内の個体をソートする
    def sort(self): 
        self.population.sort()
            
    #進化パスの計算を行う．
    def calc_evolution_path(self):
        tmp_value = 0.0
        for i in range(self.pop_size):
            tmp_value += self.w_rank[i] * self.population[i].get_z()
        tmp_value *= np.sqrt(self.c_sigma * (2.0 - self.c_sigma) * self.mu_eff)
        tmp_value += (1.0 - self.c_sigma) * self.p_sigma
        self.p_sigma = tmp_value
        
    #distベースの重みw_distの計算
    def calc_dist_weight(self):
        tmp_value = 0.0
        for i in range(self.pop_size):
            tmp_value += self.w_hat[i] * np.exp(self.alpha * np.linalg.norm(self.population[i].get_z()))
        
        for i in range(self.pop_size):
            self.w_dist[i] = (((self.w_hat[i]) * np.exp(self.alpha * np.linalg.norm(self.population[i].get_z()))) / (tmp_value)) - (1.0 / float(self.pop_size))
        
        self.w = self.w_dist                                     
        
        
    #進化パスのノルムに応じた重みの設定を行う．
    def deside_weight(self):
        norm = np.linalg.norm(self.p_sigma)
        if norm >= self.epsilon:
            self.calc_dist_weight()
        else:
            self.w = self.w_rank
            
    #ステップサイズ，正規化変換行列の学習率を決める
    def decide_learning_rate(self):
        norm = np.linalg.norm(self.p_sigma)
        #move, #stag, #convの学習率の設定
        if norm >= self.epsilon:
            self.Eta_sigma = self.Eta_sigma_move
            self.Eta_B = self.Eta_B_move
        elif norm >= 0.1 * self.epsilon:
            self.Eta_sigma = self.Eta_sigma_stag
            self.Eta_B = self.Eta_B_stag
        else:
            self.Eta_sigma = self.Eta_sigma_conv
            self.Eta_B = self.Eta_B_conv
            
    #自然勾配の計算を行う．
    def calc_Natural_Gradient(self):
        #G_delta, G_Mの計算
        pop_size = len(self.population)
        eye_matrix = np.eye(self.dim)
        self.G_delta = np.zeros(self.dim)
        self.G_M = np.eye(self.dim) * 0.0
        for i in range(pop_size):
            self.G_delta += self.w[i] * self.population[i].get_z()
            self.G_M += self.w[i] * (np.dot(self.population[i].get_z().reshape(self.dim, 1), self.population[i].get_z().reshape(1, self.dim)) - eye_matrix)
        #G_sigma, G_Bの計算を行う．
        self.G_sigma = float(np.trace(self.G_M)) / float(self.dim)
        self.G_B = self.G_M - self.G_sigma * eye_matrix
        
    def update_parameters(self):
        #平均ベクトルmの更新
        self.vecter =  self.Eta_m * self.sigma * np.dot(self.B, self.G_delta)
        self.m = self.m + self.vecter
        
        #ステップサイズσの更新
        self.sigma = self.sigma * np.exp(self.Eta_sigma * self.G_sigma / 2.0)
        
        #正規化変換行列Bの更新
        self.matrix = self.Eta_B * self.G_B / 2.0
        eig, P = np.linalg.eig(self.matrix)
        self.matrix = np.linalg.inv(P) @ self.matrix @ P
        
        for i in range(self.dim):
            self.matrix[i][i] = np.exp(self.matrix[i][i])
        
        self.matrix = np.linalg.inv(P) @ self.matrix @ P
        
        self.B = np.dot(self.B, self.matrix)
        
    def do_one_generation(self):
        self.sort()
        self.calc_evolution_path()
        self.deside_weight()
        self.decide_learning_rate()
        self.calc_Natural_Gradient()
        self.update_parameters()
        
    def get_population(self):
        return self.population
    
    def get_best_solution(self):
        self.population.sort()
        return self.population[0]
    
    def get_worst_solution(self):
        self.population.sort()
        return self.population[self.pop_size - 1]
    
    def get_m(self):
        return self.m
    
dim = 10
nes = dxnes(dim = dim, pop_size = 50, m = 5.0, sigma = 5.0, seed = 0)

for itr in range(1000):
    nes.sampling()
    evaluate(func = Sphere, poplation = nes.get_population())
    nes.do_one_generation()
    print(nes.get_best_solution())
