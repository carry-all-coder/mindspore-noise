from mindquantum.core.circuit import Circuit, UN
from mindquantum.core.gates import H, ZZ, RX
from mindquantum.core.noise_module import AmplitudeDampingChannel
from mindquantum.core.operators import Hamiltonian, QubitOperator
from mindquantum.simulator import Simulator
from scipy.optimize import minimize
import networkx as nx
import mindspore as ms
ms.set_context(mode=ms.PYNATIVE_MODE, device_target="CPU")

g = nx.Graph()
nx.add_path(g, [0, 1])
nx.add_path(g, [1, 2])
nx.add_path(g, [2, 3])
nx.add_path(g, [3, 4])
nx.add_path(g, [0, 4])
nx.add_path(g, [0, 2])
nx.draw(g, with_labels=True, font_weight='bold')

gamma = 0.005                                        
circ = Circuit(UN(H, g.nodes))                      
circ += UN(AmplitudeDampingChannel(gamma), g.nodes)  

for i in range(4):
    for j in g.edges:
        circ += ZZ(f'g{i}').on(j)                    
    circ.barrier(False)
    for j in g.nodes:
        circ += RX(f'b{i}').on(j)                   
        circ += AmplitudeDampingChannel(gamma).on(j) 
    circ.barrier(False)

ham = QubitOperator()
for i in g.edges:
    ham += QubitOperator(f'Z{i[0]} Z{i[1]}')
ham = Hamiltonian(ham)

sim = Simulator('mqvector', circ.n_qubits)          

def func(x):
    sim.reset()                                     
    sim.apply_circuit(circ, x)                       
    f = sim.get_expectation(ham).real               
    return f

n_paras = len(circ.params_name)
init_amp = [0.0 for i in range(n_paras)]

res = minimize(func, init_amp, method='nelder-mead') 
cut = (len(g.edges) - res.fun) / 2                   
print('max cut:', cut)                               