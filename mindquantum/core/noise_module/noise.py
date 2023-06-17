import numpy as np

from mindquantum import mqbackend as mb
from mindquantum.utils.f import _check_num_array

from .basic import BasicGate, NoiseGate, NonHermitianGate, SelfHermitianGate

class PauliChannel(NoiseGate, SelfHermitianGate):

    def __init__(self, px: float, py: float, pz: float, **kwargs):
        
        if 'name' not in kwargs:
            kwargs['name'] = 'PC'
        kwargs['n_qubits'] = 1
        NoiseGate.__init__(self, **kwargs)
        SelfHermitianGate.__init__(self, **kwargs)
        self.projectq_gate = None
        self.px = float(px)
        self.py = float(py)
        self.pz = float(pz)

    def __extra_prop__(self):
        
        return {'px': self.px, 'py': self.py, 'pz': self.pz}

    def get_cpp_obj(self):
        
        return mb.gate.PauliChannel(self.px, self.py, self.pz, self.obj_qubits, self.ctrl_qubits)

    def define_projectq_gate(self):
        
        self.projectq_gate = None

    def __eq__(self, other):
        
        if isinstance(other, PauliChannel):
            if BasicGate.__eq__(self, other) and self.px == other.px and self.py == other.py and self.pz == other.pz:
                return True
        return False


class BitFlipChannel(PauliChannel):
    def __init__(self, p: float, **kwargs):
        
        kwargs['name'] = 'BFC'
        kwargs['n_qubits'] = 1
        kwargs['px'] = p
        kwargs['py'] = 0
        kwargs['pz'] = 0
        PauliChannel.__init__(self, **kwargs)
        self.p = p

    def __extra_prop__(self):
        
        prop = super().__extra_prop__()
        prop['p'] = self.p
        return prop

    def __str_in_circ__(self):
        
        return f"BF({self.p})"


class PhaseFlipChannel(PauliChannel):
    def __init__(self, p: float, **kwargs):
        
        kwargs['name'] = 'PFC'
        kwargs['n_qubits'] = 1
        kwargs['px'] = 0
        kwargs['py'] = 0
        kwargs['pz'] = p
        PauliChannel.__init__(self, **kwargs)
        self.p = p

    def __extra_prop__(self):
        
        prop = super().__extra_prop__()
        prop['p'] = self.p
        return prop

    def __str_in_circ__(self):
        
        return f"PF({self.p})"

class AmplitudeDampingChannel(NoiseGate, NonHermitianGate):

    def __init__(self, gamma: float, **kwargs):
        kwargs['name'] = 'ADC'
        kwargs['n_qubits'] = 1
        NoiseGate.__init__(self, **kwargs)
        NonHermitianGate.__init__(self, **kwargs)
        self.projectq_gate = None
        if not isinstance(gamma, (int, float)):
            raise TypeError(f"Unsupported type for gamma, get {type(gamma)}.")
        if 0 <= gamma <= 1:
            self.gamma = gamma
        else:
            raise ValueError("Required damping coefficient gamma ∈ [0,1].")

    def get_cpp_obj(self):
        return mb.gate.AmplitudeDampingChannel(self.hermitianed, self.gamma, self.obj_qubits, self.ctrl_qubits)

    def define_projectq_gate(self):
        self.projectq_gate = None

    def __eq__(self, other):
        return BasicGate.__eq__(self, other) and self.gamma == other.gamma

    def __str_in_circ__(self):
        return f"AD({self.gamma})"