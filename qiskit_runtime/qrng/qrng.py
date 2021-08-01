from qiskit import QuantumCircuit


def prepare_bell_circuit():
    bell = QuantumCircuit(2, 2)
    bell.h(0)
    bell.cx(0, 1)
    bell.measure_all()
    return bell


def main(backend, messenger, greeting):
    bell = prepare_bell_circuit()  # prepare the circuits
    messenger.publish(greeting)  # publish interim results
    print(bell.draw(output='text'))  # draw the circuit (captured as part of the logs)
    result = backend.run(bell).result()  # run the circuit
    messenger.publish(result.get_counts(), final=True)  # publish the final result

