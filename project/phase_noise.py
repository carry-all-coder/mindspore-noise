from mindquantum.core.gates import T, H, X, Power, BARRIER
from mindquantum.core.noise_module import PhaseFlipChannel
from mindquantum.core.circuit import Circuit, UN
from mindquantum.simulator import Simulator
from mindquantum.algorithm.library import qft
import numpy as np
n = 4
circ = Circuit()
circ += UN(H, n) 
circ += X.on(n)  
circ += PhaseFlipChannel(0.7).on(0) # 引入噪声
circ.svg()
for i in range(n):
    circ += Power(T, 2**i).on(n, n - i - 1) 
circ.svg()
circ += BARRIER
circ += qft(range(n)).hermitian() 
circ.svg()
from mindquantum.core.gates import Measure
sim = Simulator('mqvector', circ.n_qubits)                      # 创建模拟器
sim.apply_circuit(circ)                                         # 用模拟器演化线路
qs = sim.get_qs()                                               # 获得演化得到的量子态
res = sim.sampling(UN(Measure(), circ.n_qubits - 1), shots=100) # 在寄存器1中加入测量门并对线路进行100次采样，获得统计结果
res.svg()
index = np.argmax(np.abs(qs))
print(bin(index)[2:])

bit_string = bin(index)[2:].zfill(circ.n_qubits)[1:]        
bit_string = bit_string[::-1]                               
print(bit_string)

theta_exp = int(bit_string, 2) / 2**n
theta_exp




