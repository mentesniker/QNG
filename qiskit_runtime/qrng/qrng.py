# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Source code for the QRNG Qiskit Runtime program."""

from qiskit.aqua.algorithms import QGAN
from qiskit import Aer

def prepare_qgan(dataset,backend,iterations,batch_size,bounds):
    qgan = QGAN(data=dataset,num_epochs=iterations,bounds=bounds,batch_size=batch_size, 
                quantum_instance = backend)
    qgan.train()
    return qgan

def generate_number(params,backend,qc,num_shots):
    new_circuit = qc.assign_parameters(parameters = params)
    new_circuit.measure_all()
    return [int(x,2) for x in backend.run(new_circuit,shots=num_shots,memory=True).result().get_memory()]

def main(
    backend,
    user_messenger,
    dataset,
    sample_size,
    **kwargs,
):
    back = Aer.get_backend("qasm_simulator")
    qgan = prepare_qgan(dataset,back,5,[0,2],1)
    qc = qgan.generator.generator_circuit
    params = list(qgan.generator.parameter_values)
    qc = qc.bind_parameters(params)
    result = generate_number(params,back,qc,sample_size)
    user_messenger.publish(zip(result.get_counts(),qgan.g_loss), final=True)  # publish the final result

