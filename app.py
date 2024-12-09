import streamlit as st
import quantum_game_core as core
import matplotlib.pyplot as plt

# Initialize session state variables
if "level" not in st.session_state:
    st.session_state.level = None
if "target_circuit" not in st.session_state:
    st.session_state.target_circuit = None
if "target_state" not in st.session_state:
    st.session_state.target_state = None
if "attempts" not in st.session_state:
    st.session_state.attempts = 0

# Functions
def reset_game(level):
    """Reset the game with a new target circuit."""
    st.session_state.level = level
    st.session_state.target_circuit, st.session_state.target_state = core.generate_target(level)
    st.session_state.attempts = 0

def render_circuit_image(circuit):
    """Render a quantum circuit as a colorized image."""
    fig, ax = plt.subplots(figsize=(8, 4))
    circuit.draw(output="mpl", ax=ax)
    return fig


# Streamlit UI
st.title("Quantum Puzzle Game")
st.write("Solve the quantum puzzle by matching your circuit to the target state!")

# Step 1: Select Level
level = st.selectbox("Select Level", ["Beginner", "Intermediate", "Advanced"], key="level_selector")
if st.button("Start Game"):
    reset_game(level.lower())

# Step 2: Display Target Circuit
if st.session_state.target_circuit:
    st.subheader("Target Circuit")
    target_circuit_image = render_circuit_image(st.session_state.target_circuit)
    st.pyplot(target_circuit_image)

# Step 3: Input Gate Sequence
if st.session_state.target_circuit:
    st.subheader("Your Solution")
    user_input = st.text_input(
        "Enter your gate sequence (e.g., [('H', 0), ('CX', (0, 1))]):",
        placeholder="[('H', 0)]",
    )
    if st.button("Submit Solution"):
        try:
            # Parse the input and apply gates
            player_gates = eval(user_input)
            num_qubits = len(st.session_state.target_circuit.qubits)
            player_circuit = core.apply_player_gates(player_gates, num_qubits)

            # Increment attempts
            st.session_state.attempts += 1

            # Display Player Circuit
            st.write("Your Circuit:")
            player_circuit_image = render_circuit_image(player_circuit)
            st.pyplot(player_circuit_image)

            # Validate Solution
            if core.validate_solution(player_circuit, st.session_state.target_state):
                st.success(f"Congratulations! You matched the target state in {st.session_state.attempts} attempt(s)!")
                st.balloons()
                st.button("Start New Game", on_click=lambda: reset_game(level.lower()))
            else:
                st.error("Not quite right! Try again.")
        except Exception as e:
            st.error(f"Error: {e}")

# Step 4: Reset Game Button
if st.session_state.target_circuit:
    st.button("Generate New Target", on_click=lambda: reset_game(level.lower()))
