import time
import streamlit as st

from agents import build_reader_agent, build_search_agent, writter_chain, critic_chain

# ------------------------------------------------------------------
# Page config
# ------------------------------------------------------------------
st.set_page_config(
    page_title="Research AI | Multi-Agent System",
    page_icon="🟢",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ------------------------------------------------------------------
# Styling
# ------------------------------------------------------------------
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
  --bg: #050807;
  --panel: rgba(255,255,255,0.04);
  --panel-border: rgba(255,255,255,0.08);
  --accent: #3fb68b;
  --accent-soft: rgba(63,182,139,0.15);
  --text: #f2f5f4;
  --muted: #8a9a94;
}

html, body, [class*="css"], .stApp {
  font-family: 'Inter', sans-serif !important;
  color: var(--text);
}

.stApp {
  background:
    radial-gradient(ellipse 70% 40% at 50% 0%, rgba(63,182,139,0.10), transparent 70%),
    var(--bg);
}

/* hide streamlit chrome */
#MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; height: 0; }
.block-container { max-width: 1100px; padding-top: 3.5rem; padding-bottom: 5rem; }

/* ---------- hero ---------- */
.hero { text-align: center; margin-bottom: 1.5rem; }
.hero h1 {
  font-size: 3.4rem; font-weight: 600; line-height: 1.15;
  letter-spacing: -0.02em; margin: 0 0 1.2rem 0;
}
.hero h1 .accent { color: var(--accent); }
.hero p {
  max-width: 640px; margin: 0 auto; color: var(--muted);
  font-size: 0.95rem; line-height: 1.7;
}
.badge {
  display: inline-block; padding: 6px 14px; border-radius: 999px;
  background: var(--accent-soft); color: var(--accent);
  font-size: 0.75rem; font-weight: 500; margin-bottom: 1.4rem;
  border: 1px solid rgba(63,182,139,0.3);
}

/* ---------- input ---------- */
div[data-testid="stTextInput"] div[data-baseweb="input"],
div[data-testid="stTextInput"] div[data-baseweb="base-input"] {
  background: #111917 !important;
  border: 1px solid var(--panel-border) !important;
  border-radius: 999px !important;
}
div[data-testid="stTextInput"] div[data-baseweb="input"]:focus-within {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 3px rgba(63,182,139,0.18) !important;
}
div[data-testid="stTextInput"] input {
  background: transparent !important;
  border: none !important;
  padding: 0.9rem 1.4rem !important;
  color: #f2f5f4 !important;
  -webkit-text-fill-color: #f2f5f4 !important;
  caret-color: var(--accent) !important;
  font-size: 0.95rem !important;
  pointer-events: auto !important;
}
div[data-testid="stTextInput"] input::placeholder {
  color: #6f7f79 !important;
  -webkit-text-fill-color: #6f7f79 !important;
}
div[data-testid="stTextInput"] label { display: none; }

/* ---------- buttons ---------- */
.stButton > button, .stDownloadButton > button {
  background: var(--accent) !important; color: #04130d !important;
  border: none !important; border-radius: 999px !important;
  padding: 0.75rem 1.6rem !important; font-weight: 600 !important;
  width: 100%; transition: all .2s ease;
}
.stButton > button:hover, .stDownloadButton > button:hover {
  transform: translateY(-1px);
  box-shadow: 0 8px 24px rgba(63,182,139,0.35);
}

/* ---------- glowing arc ---------- */
.arc-wrap { position: relative; height: 230px; margin: 2.5rem 0 1rem 0; overflow: hidden; }
.arc {
  position: absolute; left: 50%; top: 70px; transform: translateX(-50%);
  width: 900px; height: 900px; border-radius: 50%;
  background: radial-gradient(circle at 50% 0%, rgba(63,182,139,0.18), rgba(5,8,7,0) 60%);
  border-top: 2px solid rgba(63,182,139,0.55);
  box-shadow: 0 -20px 80px rgba(63,182,139,0.25);
}
.float-card {
  position: absolute; background: rgba(20,28,25,0.85);
  border: 1px solid var(--panel-border); border-radius: 20px;
  padding: 14px 18px; backdrop-filter: blur(8px);
  box-shadow: 0 12px 40px rgba(0,0,0,0.5);
  animation: floaty 6s ease-in-out infinite;
}
.float-card .label {
  font-size: 0.65rem; color: var(--muted); text-transform: uppercase; letter-spacing: .08em;
}
.float-card .value { font-size: 1.05rem; font-weight: 600; color: var(--accent); margin-top: 2px; }
.fc1 { left: 8%;  top: 60px;  transform: rotate(-8deg); }
.fc2 { left: 38%; top: 110px; animation-delay: 1s; }
.fc3 { right: 8%; top: 50px;  transform: rotate(7deg); animation-delay: 2s; }
@keyframes floaty { 0%,100% { margin-top: 0; } 50% { margin-top: -10px; } }

/* ---------- pipeline steps ---------- */
.steps { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin: 1.5rem 0; }
.step {
  background: var(--panel); border: 1px solid var(--panel-border);
  border-radius: 18px; padding: 18px; transition: all .3s ease;
}
.step .num { font-size: 0.7rem; color: var(--muted); letter-spacing: .1em; }
.step .name { font-weight: 600; margin: 6px 0 2px 0; }
.step .desc { font-size: 0.78rem; color: var(--muted); }
.step .state { margin-top: 10px; font-size: 0.72rem; font-weight: 500; color: var(--muted); }
.step.active {
  border-color: var(--accent); background: var(--accent-soft);
  box-shadow: 0 0 30px rgba(63,182,139,0.2);
}
.step.active .state { color: var(--accent); }
.step.done { border-color: rgba(63,182,139,0.35); }
.step.done .state { color: var(--accent); }

/* ---------- result area ---------- */
.stTabs [data-baseweb="tab-list"] { gap: 8px; border-bottom: none; }
.stTabs [data-baseweb="tab"] {
  background: var(--panel); border-radius: 999px; padding: 8px 20px;
  border: 1px solid var(--panel-border); color: var(--muted);
}
.stTabs [aria-selected="true"] {
  background: var(--accent-soft) !important; color: var(--accent) !important;
  border-color: rgba(63,182,139,0.4) !important;
}
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display: none; }

.result-card {
  background: var(--panel); border: 1px solid var(--panel-border);
  border-radius: 20px; padding: 1.6rem 1.8rem; margin-top: 1rem;
}
.section-title { font-size: 1.1rem; font-weight: 600; margin: 2.2rem 0 0.4rem 0; }

@media (max-width: 800px) {
  .hero h1 { font-size: 2.2rem; }
  .steps { grid-template-columns: repeat(2, 1fr); }
  .float-card { display: none; }
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ------------------------------------------------------------------
# Hero
# ------------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
      <span class="badge">● Multi-Agent Research System</span>
      <h1>Your <span class="accent">AI Research</span><br>Assistant for Everyday Work</h1>
      <p>Search the web, scrape the best sources, draft a structured report and get it
      reviewed by a critic, all handled by a team of specialised AI agents.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------
# Input row
# ------------------------------------------------------------------
def start_research():
    """Runs before the rerun: save the typed topic, then clear the input box."""
    st.session_state["pending_topic"] = st.session_state.get("topic_input", "").strip()
    st.session_state["topic_input"] = ""


_, col_in, col_btn, _ = st.columns([0.6, 4, 1.4, 0.6], vertical_alignment="center")
with col_in:
    st.text_input(
        "Topic",
        key="topic_input",
        placeholder="Enter a research topic, e.g. Future of solid-state batteries",
        label_visibility="collapsed",
    )
with col_btn:
    st.button("Start Research ↗", on_click=start_research)

# topic captured by the button callback (None if the button wasn't clicked)
topic = st.session_state.pop("pending_topic", None)
run = topic is not None

# ------------------------------------------------------------------
# Decorative arc (only on the landing state)
# ------------------------------------------------------------------
if "result" not in st.session_state and not run:
    st.markdown(
        """
        <div class="arc-wrap">
          <div class="arc"></div>
          <div class="float-card fc1"><div class="label">Step 1</div><div class="value">Search Agent</div></div>
          <div class="float-card fc2"><div class="label">Step 2</div><div class="value">Reader Agent</div></div>
          <div class="float-card fc3"><div class="label">Step 3 &amp; 4</div><div class="value">Writer + Critic</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ------------------------------------------------------------------
# Pipeline step tracker
# ------------------------------------------------------------------
STEPS = [
    ("Search Agent", "Finds recent, reliable sources"),
    ("Reader Agent", "Scrapes the most relevant page"),
    ("Writer", "Drafts the full report"),
    ("Critic", "Reviews and gives feedback"),
]


def render_steps(placeholder, current: int):
    """current: index of active step; len(STEPS) means all done; -1 means none started."""
    html = '<div class="steps">'
    for i, (name, desc) in enumerate(STEPS):
        if i < current:
            cls, state = "done", "✓ Completed"
        elif i == current:
            cls, state = "active", "● Working..."
        else:
            cls, state = "", "Waiting"
        html += (
            f'<div class="step {cls}"><div class="num">STEP {i + 1}</div>'
            f'<div class="name">{name}</div><div class="desc">{desc}</div>'
            f'<div class="state">{state}</div></div>'
        )
    html += "</div>"
    placeholder.markdown(html, unsafe_allow_html=True)


# ------------------------------------------------------------------
# Pipeline (same logic as pipline.py, with live progress)
# ------------------------------------------------------------------
def run_pipeline_with_progress(topic: str, steps_ph) -> dict:
    state = {}

    render_steps(steps_ph, 0)
    search_agent = build_search_agent()
    search_result = search_agent.invoke(
        {"messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]}
    )
    state["search_results"] = search_result["messages"][-1].content

    render_steps(steps_ph, 1)
    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke(
        {
            "messages": [
                (
                    "user",
                    f"Based on the following search results about '{topic}', "
                    f"pick the most relevant URL and scrape it for deeper content.\n\n"
                    f"Search Results\n{state['search_results'][:800]}",
                )
            ]
        }
    )
    state["scraped_content"] = reader_result["messages"][-1].content

    render_steps(steps_ph, 2)
    research_combined = (
        f"SEARCH RESULTS: \n {state['search_results']} \n\n"
        f"DETAILED SCRAPED CONTENT: \n{state['scraped_content']}"
    )
    state["report"] = writter_chain.invoke({"topic": topic, "research": research_combined})

    render_steps(steps_ph, 3)
    state["feedback"] = critic_chain.invoke({"report": state["report"]})

    render_steps(steps_ph, len(STEPS))
    return state


# ------------------------------------------------------------------
# Run
# ------------------------------------------------------------------
steps_ph = st.empty()

if run:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        start = time.time()
        try:
            result = run_pipeline_with_progress(topic.strip(), steps_ph)
            result["topic"] = topic.strip()
            result["elapsed"] = time.time() - start
            st.session_state["result"] = result
        except Exception as e:
            st.error(f"Something went wrong while running the agents: {e}")
elif "result" in st.session_state:
    render_steps(steps_ph, len(STEPS))

# ------------------------------------------------------------------
# Results
# ------------------------------------------------------------------
if "result" in st.session_state:
    res = st.session_state["result"]

    st.markdown(
        f'<div class="section-title">Results for “{res["topic"]}”</div>',
        unsafe_allow_html=True,
    )
    st.caption(f"Completed in {res['elapsed']:.1f}s")

    tab_report, tab_feedback, tab_search, tab_scrape = st.tabs(
        ["📄 Final Report", "🧐 Critic Feedback", "🔎 Search Results", "🌐 Scraped Content"]
    )

    with tab_report:
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown(res["report"])
        st.markdown("</div>", unsafe_allow_html=True)
        st.download_button(
            "Download Report (.md)",
            data=res["report"],
            file_name="research_report.md",
            mime="text/markdown",
        )

    with tab_feedback:
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown(res["feedback"])
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_search:
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown(res["search_results"])
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_scrape:
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown(res["scraped_content"])
        st.markdown("</div>", unsafe_allow_html=True)