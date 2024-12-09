from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import random


def generate_beginner_target():
    """Generate a beginner-level target circuit."""
    target_circuit = QuantumCircuit(1)
    gates = [("h", 0), ("x", 0), ("z", 0)]
    selected_gates = random.choices(gates, k=3)  # Randomly select 3 gates
    for gate, qubit in selected_gates:
        if gate == "h":
            target_circuit.h(qubit)
        elif gate == "x":
            target_circuit.x(qubit)
        elif gate == "z":
            target_circuit.z(qubit)
    return target_circuit, Statevector.from_instruction(target_circuit)


def generate_intermediate_target():
    """Generate an intermediate-level target circuit."""
    target_circuit = QuantumCircuit(2)
    gates = [("h", 0), ("x", 0), ("z", 1), ("cx", (0, 1))]
    selected_gates = random.choices(gates, k=4)  # Randomly select 4 gates
    for gate in selected_gates:
        if gate[0] == "h":
            target_circuit.h(gate[1])
        elif gate[0] == "x":
            target_circuit.x(gate[1])
        elif gate[0] == "z":
            target_circuit.z(gate[1])
        elif gate[0] == "cx":
            target_circuit.cx(gate[1][0], gate[1][1])
    return target_circuit, Statevector.from_instruction(target_circuit)


def generate_advanced_target():
    """Generate an advanced-level target circuit."""
    target_circuit = QuantumCircuit(3)
    gates = [
        ("h", 0), ("x", 1), ("z", 2),
        ("cx", (0, 1)), ("cx", (1, 2)), ("swap", (0, 2))
    ]
    selected_gates = random.choices(gates, k=5)  # Randomly select 5 gates
    for gate in selected_gates:
        if gate[0] == "h":
            target_circuit.h(gate[1])
        elif gate[0] == "x":
            target_circuit.x(gate[1])
        elif gate[0] == "z":
            target_circuit.z(gate[1])
        elif gate[0] == "cx":
            target_circuit.cx(gate[1][0], gate[1][1])
        elif gate[0] == "swap":
            target_circuit.swap(gate[1][0], gate[1][1])
    return target_circuit, Statevector.from_instruction(target_circuit)


def generate_target(level):
    """Generate a target circuit based on the chosen level."""
    if level == "beginner":
        return generate_beginner_target()
    elif level == "intermediate":
        return generate_intermediate_target()
    elif level == "advanced":
        return generate_advanced_target()
    else:
        raise ValueError("Invalid level. Choose 'beginner', 'intermediate', or 'advanced'.")


def apply_player_gates(player_gates, num_qubits):
    """Apply player-defined gates to a circuit."""
    player_circuit = QuantumCircuit(num_qubits)
    for gate in player_gates:
        if gate[0] == "H":
            player_circuit.h(gate[1])
        elif gate[0] == "X":
            player_circuit.x(gate[1])
        elif gate[0] == "Z":
            player_circuit.z(gate[1])
        elif gate[0] == "CX":
            player_circuit.cx(gate[1][0], gate[1][1])
        elif gate[0] == "SWAP":
            player_circuit.swap(gate[1][0], gate[1][1])
    return player_circuit


def validate_solution(player_circuit, target_state):
    """Validate the player's circuit against the target state."""
    player_state = Statevector.from_instruction(player_circuit)
    return player_state.equiv(target_state)
