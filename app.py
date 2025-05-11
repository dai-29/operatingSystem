import streamlit as st

# Set up page config
st.set_page_config(page_title="OSync Simulator", layout="centered")

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
    </style>

    <h1 class="classic-title">🌀 OSync: Page Replacement & Scheduling Simulator</h1>
""", unsafe_allow_html=True)


st.image('img/back.jpg', use_column_width=True) 

st.markdown("<h4 style='text-align:center; color: gray;'>Visualize. Simulate. Learn.</h4>", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "home"

def go_to_page(name):
    st.session_state.page = name

#home 
if st.session_state.page == "home":
    st.subheader("Your Interactive OS Learning Tool")
    
    st.markdown("""
    **Osync** is an educational web-based simulator designed to help students understand two crucial Operating System concepts — **Page Replacement Algorithms** and **Process Scheduling Algorithms**. These abstract topics are often difficult to visualize using traditional methods like lectures and textbooks. Osync offers a practical, hands-on experience where students can input real-time data and observe how these algorithms work step-by-step. 
    
    The simulator supports **FIFO** and **LRU** algorithms for page replacement, and **Round Robin** and **SJF** for CPU scheduling. By offering interactive visualization, students can enhance their understanding, experiment with scenarios, and truly grasp the underlying logic. Osync aims to bridge the gap between theory and practice, making OS concepts more approachable and engaging.
    """)

    st.markdown("## 🚀 Explore Simulators:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📄 Page Replacement"):
            go_to_page("page_replacement")
    with col2:
        if st.button("📊 Process Scheduling"):
            go_to_page("process_scheduling")

#page replacement
elif st.session_state.page == "page_replacement":
    st.header("📄 Page Replacement Simulator")
    if st.button("⬅ Back to Home"):
        go_to_page("home")
    
    algo = st.selectbox("Choose Algorithm", ["FIFO", "LRU"])
    num_pages = st.number_input("Enter number of pages", min_value=1)
    pages = st.text_input("Page reference string (comma-separated)", placeholder="7, 0, 1, 2, 0, 3, 0, 4")
    frames = st.number_input("Enter number of frames", min_value=1)

    if st.button("Simulate"):
        st.success(f"Running {algo}...")
        st.info("Simulation output will appear here.")

#process scheduling
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
        st.success(f"Running {sched_algo}...")
        st.info("Scheduling output will appear here.")
