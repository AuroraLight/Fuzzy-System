使用python 3.6版開發，
GUI使用python內建的Tkinter，
程式分為五個檔案，
main.py是程式進入點，
RBFN.py為運用RBFN會用到的所有函式，包含訓練RBFN函式、test函式、正規化資料、適應函數計算函式，
GA.py為執行基因演算法流程，包含複製、交配、突變、更新基因，
Car.py為車子要跑到終點所需的所有處理函式，包含得到需要的線性方程式、線性方程式彼此的交點、取得正前方與左右各45度之距離，
GUI.py定義使用者介面，並顯示結果。
 
RBFN.py
RBFN.py:
Function normalize_data(): 正規化資料(e.g. -1 <= xi <= 1, -1 <= yi <= 1)
Function normalize_input_data(): 正規化傳入資料(e.g. train4dAll.txt的資料)
Function anti_normalization_f(): 反正規化(e.g. 計算出來的F需要轉回-40~40度的方向盤角度)
Function calcu_F(): 計算RBFN得到的output F
Function calcu_fitness(): 計算適應函數值
Function train(): 訓練RBFN
Function test():
傳入模擬車的data((車子目前位置x、y)、前方距離、右方距離、左方距離)，使用train function得到的最佳基因當作權重，回傳車子下一刻的方向盤角度
 
GA.py
GA.py:
Function crossover_swap(): 交配時會使用到的基因交換
Function update_vector(): 更新基因，基因演算法流程—複製、交配、突變、更新

 
Car.py
Car.py:
Function calculate_b(): 計算出線性方程式的b(y=mx+’b’)
Function calculate_m(): 計算出線性方程式的m(斜率)
Function find_intersection(): 找到線性方程式的交點
Function calculate_distant(): 計算出點到點之間的距離
Function get_distant(): 算出傳入角度的線性方程式，並找到該線與軌道的交點，最後得到交點與車子距離
Function get_sensor_data(): 得到三個不同角度(車子正前、左45度、右45度)的距離
Function judge_arrive(): 判斷是否到達終點區域
Function get_next_wheel_degree(): 呼叫rbfn的test取得當前距離下的方向盤角度
Function run(): 運行模擬車

 
GUI.py
GUI.py:
Function open_data(): 開啟想要的訓練資料
Function load_data(): 讀取指定訓練資料
Function draw_arrived_track(): 在GUI Canvas上繪出模擬車行進軌跡
Function run(): 當使用者按下GUI上的Run按鈕後，執行RBFN訓練以及運行車子
Function init開頭的以及place為GUI上的各種元件設定
Function draw_car_track(): 在GUI Canvas上繪出一開始的模擬車軌道以及車子起始位置
