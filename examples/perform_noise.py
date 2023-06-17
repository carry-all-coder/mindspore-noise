from mindquantum.core.gates import X,Y,Z,H
from mindquantum.core.noise_module import PauliChannel
from mindquantum.core.circuit import Circuit

circ = Circuit()
circ += Y.on(0)
circ += PauliChannel(0.1,0.1,0.1).on(0)
circ.measure(0)
print(circ)

from mindquantum.simulator import Simulator
sim = Simulator('mqvector', 1)
result = sim.sampling(circ, shots=10000)
print(result)


from mindquantum.core.noise_module import BitFlipChannel

from mindquantum.core.circuit import Circuit

circ = Circuit()
circ += X.on(0)
circ += BitFlipChannel(0.1).on(0)
circ.measure(0)
print(circ)

from mindquantum.simulator import Simulator

sim = Simulator('mqvector', 1)
result = sim.sampling(circ, shots=10000)
print(result)

from mindquantum.core.noise_module import PhaseFlipChannel
from mindquantum.core.circuit import Circuit

circ = Circuit()
circ += Z.on(0)
circ += PhaseFlipChannel(0.1).on(0)
circ.measure(0)
print(circ)

from mindquantum.simulator import Simulator

sim = Simulator('mqvector', 1)
result = sim.sampling(circ, shots=10000)
# result.svg()
print(result)

from mindquantum.core.noise_module import AmplitudeDampingChannel

circ2 = Circuit()
circ2 += H.on(0)
circ2 += AmplitudeDampingChannel(0.8).on(0)
print(circ2)

for i in range(5):
    sim.reset()                 
    sim.apply_circuit(circ2)    
    print(sim.get_qs(ket=True)) 
    print()


