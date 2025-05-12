import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Page configuration
st.set_page_config(page_title="OSync Simulator", layout="centered")

# Custom title with CSS
st.markdown("""     
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap');
    .classic-title {
        font-family: "Lucida Console", "Courier New", monospace;
        font-size: 40px;
        color: #ff2c2c;
        text-align: center;
        font-weight: 500;
        letter-spacing: 1.0px;
        margin-bottom: 25px;
        padding-bottom: 12px;
        background: linear-gradient(90deg, #004e92, #000428);
        text-shadow:
            1px 1px 2px rgba(0, 0, 0, 0.2),
            2px 2px 4px rgba(0, 0, 0, 0.15);
        border-bottom: 2px dashed #777;
        transition: all 0.3s ease-in-out;
    }
    .classic-title:hover {
        transform: scale(1.03);
        letter-spacing: 1.5px;
    }
    .stButton>button {
        font-family: "Lucida Console", "Courier New", monospace;
        background-color: #007BFF;
        color: white;
        font-size: 18px;
        font-weight: 500;
        border-radius: 12px;
        border: none;
        padding: 12px 30px;
        width: 100%;
        cursor: pointer;
        transition: background-color 0.3s ease, transform 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        font-size: 22px;
        transform: scale(1.05);
    }
    </style>

    <h1 class="classic-title">🌀 OSync: Page Replacement & Scheduling Simulator</h1>
""", unsafe_allow_html=True)

st.image('img/back.jpg', use_column_width=True) 
st.markdown("<h4 style='text-align:center; color: gray;'>Visualize. Simulate. Learn.</h4>", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "home"

def go_to_page(name):
    st.session_state.page = name

# HOME PAGE
if st.session_state.page == "home":
    st.subheader("Your Interactive OS Learning Tool")

    st.markdown("""
    **OSync** is a simulator designed to help students understand **Page Replacement Algorithms** and **CPU Scheduling Algorithms**.

    It supports:
    - **Page Replacement:** FIFO, LRU  
    - **CPU Scheduling:** Round Robin, Shortest Job First (SJF)

    Input your data and visualize algorithm behavior step-by-step.
    """)

    st.markdown("## 🚀 Explore Simulators:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📄 Page Replacement"):
            go_to_page("page_replacement")
    with col2:
        if st.button("📊 Process Scheduling"):
            go_to_page("process_scheduling")

# PAGE REPLACEMENT SIMULATOR
elif st.session_state.page == "page_replacement":
    st.header("📄 Page Replacement Simulator")
    if st.button("⬅ Back to Home"):
        go_to_page("home")

    algo = st.selectbox("Choose Algorithm", ["FIFO", "LRU"])
    num_pages = st.number_input("Enter number of pages", min_value=1)
    pages = st.text_input("Page reference string (comma-separated)", placeholder="7, 0, 1, 2, 0, 3, 0, 4")
    frames = st.number_input("Enter number of frames", min_value=1)

    if st.button("Simulate"):
        if not pages.strip():
            st.error("Please enter a valid page reference string.")
        else:
            try:
                page_list = list(map(int, pages.split(',')))
                frame_count = int(frames)

                timeline = []
                faults = 0
                hits = 0
                frame_history = []
                display_labels = []

                if algo == "FIFO":
                    frame = []
                    for i, page in enumerate(page_list):
                        if page in frame:
                            hits += 1
                        else:
                            faults += 1
                            if len(frame) < frame_count:
                                frame.append(page)
                            else:
                                frame.pop(0)
                                frame.append(page)
                        frame_history.append(frame.copy())
                        display_labels.append(f"{'Hit' if page in frame else 'Fault'}: {page}")

                elif algo == "LRU":
                    frame = []
                    recent = {}
                    for i, page in enumerate(page_list):
                        if page in frame:
                            hits += 1
                        else:
                            faults += 1
                            if len(frame) < frame_count:
                                frame.append(page)
                            else:
                                lru = min(recent, key=recent.get)
                                frame[frame.index(lru)] = page
                                del recent[lru]
                        recent[page] = i
                        frame_history.append(frame.copy())
                        display_labels.append(f"{'Hit' if page in frame else 'Fault'}: {page}")

                st.success(f"Simulation complete! Total Page Faults: {faults}, Hits: {hits}")

                st.markdown("### 🔍 Frame History Table")
                df = pd.DataFrame(frame_history, columns=[f"Frame {i+1}" for i in range(frame_count)])
                df.index = [f"Step {i+1} ({lbl})" for i, lbl in enumerate(display_labels)]
                st.dataframe(df)

                st.markdown("### 📈 Matplotlib Visualization")
                fig, ax = plt.subplots()
                for i in range(frame_count):
                    ax.plot(range(len(frame_history)), [f[i] if i < len(f) else None for f in frame_history], label=f'Frame {i+1}', marker='o')
                ax.set_title(f"{algo} Page Replacement")
                ax.set_xlabel("Steps")
                ax.set_ylabel("Page Number")
                ax.legend()
                st.pyplot(fig)

                st.markdown("### 📊 Plotly Timeline")
                fig2 = go.Figure()
                for i in range(frame_count):
                    fig2.add_trace(go.Scatter(
                        x=[f"Step {j+1}" for j in range(len(frame_history))],
                        y=[f[i] if i < len(f) else None for f in frame_history],
                        mode='lines+markers',
                        name=f"Frame {i+1}"
                    ))
                fig2.update_layout(title=f"{algo} Frame Timeline", xaxis_title="Step", yaxis_title="Page")
                st.plotly_chart(fig2)

            except Exception as e:
                st.error(f"Error in simulation: {e}")

# PROCESS SCHEDULING SIMULATOR
elif st.session_state.page == "process_scheduling":
    st.header("📊 Process Scheduling Simulator")

    if st.button("⬅ Back to Home"):
        go_to_page("home")

    sched_algo = st.selectbox("Choose Algorithm", ["Round Robin", "Shortest Job First (SJF)"])
    num_processes = st.number_input("Enter number of processes", min_value=1)
    burst_input = st.text_area("Enter burst times (comma-separated)", placeholder="5, 3, 8, 6")

    if sched_algo == "Round Robin":
        quantum = st.number_input("Enter time quantum", min_value=1)

    if st.button("Simulate"):
        try:
            burst_times = list(map(int, burst_input.split(',')))

            if len(burst_times) != num_processes:
                st.error(f"Please enter exactly {num_processes} burst times.")
            else:
                st.success(f"Running {sched_algo}...")

                def round_robin_process_scheduling(burst_times, quantum):
                    n = len(burst_times)
                    remaining = burst_times[:]
                    t = 0
                    result = []
                    queue = list(range(n))
                    while any(remaining):
                        for i in queue:
                            if remaining[i] > 0:
                                exec_time = min(quantum, remaining[i])
                                result.append(f"P{i+1} ran for {exec_time} units (Remaining: {remaining[i] - exec_time})")
                                t += exec_time
                                remaining[i] -= exec_time
                    return result

                def sjf_process_scheduling(burst_times):
                    sorted_processes = sorted(enumerate(burst_times), key=lambda x: x[1])
                    result = []
                    time = 0
                    for i, bt in sorted_processes:
                        result.append(f"P{i+1} ran from time {time} to {time + bt}")
                        time += bt
                    return result

                if sched_algo == "Round Robin":
                    result = round_robin_process_scheduling(burst_times, quantum)
                else:
                    result = sjf_process_scheduling(burst_times)

                st.info("📋 Scheduling Output:")
                for r in result:
                    st.write(r)

        except ValueError:
            st.error("Invalid burst times input. Please ensure the input is comma-separated integers.")
