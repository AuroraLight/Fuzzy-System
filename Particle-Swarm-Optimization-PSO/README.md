#  Particle Swarm Optimization(PSO)
PSO function desciption

#### RBFN.py
>* Function normalize_data(): 正規化資料(e.g. -1 <= xi <= 1, -1 <= yi <= 1)
>* Function normalize_input_data(): 正規化傳入資料(e.g. train4dAll.txt的資料)
>* Function anti_normalization_f(): 反正規化f(e.g. f從-1~1變成-40~40)
>* Function calcu_F(): 計算RBFN得到的output F
>* Function calcu_fitness(): 計算適應函式值
>* Function train(): RBFN訓練函式，當中會呼叫PSO演算法來趨近最佳鍵結值
>* Function test(): 輸入input到RBFN，之後由最佳的參數(權重、m、sigma)得的方向盤角度

#### PSO.py
>* Function update_individual_vector(): PSO更新方程式，讓個體往最佳值移動
>* Function update_min_vector(): 找到群體中最小E(n)並儲存、更新個體最小E(n)並儲存

#### Car.py
>* Function calculate_b(): 計算出線性方程式的b(y=mx+’b’)
>* Function calculate_m(): 計算出線性方程式的m(斜率)
>* Function find_intersection(): 找到線性方程式的交點
>* Function calculate_distant(): 計算出點到點之間的距離
>* Function get_distant(): 算出傳入角度的線性方程式，並找到該線與軌道的交點，最後得到交點與車子距離
>* Function get_sensor_data(): 得到三個不同角度(車子正前、左45度、右45度)的距離
>* Function judge_arrive(): 判斷是否到達終點區域
>* Function get_next_wheel_degree(): 給input x去呼叫RBFN的test function
>* Function run(): 運行模擬車

#### GUI.py
>* Function open_data(): 開啟想要的訓練資料
>* Function load_data(): 讀取指定訓練資料
>* Function draw_arrived_track(): 在GUI Canvas上繪出模擬車行進軌跡
>* Function run(): 當使用者按下GUI上的Run按鈕後，執行RBFN訓練以及運行車子
>* Function init開頭的以及place為GUI上的各種元件設定
>* Function draw_car_track(): 在GUI Canvas上繪出一開始的模擬車軌道以及車子起始位置
