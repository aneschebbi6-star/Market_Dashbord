import streamlit as st


def inject_global_styles():
    """Inject the global dark theme CSS for the main dashboard."""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

        /* ── Base ── */
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #f8fafc;
            font-family: 'Inter', sans-serif;
        }

        /* ── Metric Cards ── */
        [data-testid="stMetric"] {
            background: rgba(30, 41, 59, 0.5);
            backdrop-filter: blur(5px);
            padding: 20px !important;
            border-radius: 15px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            transition: transform 0.3s ease, border-color 0.3s ease;
        }
        [data-testid="stMetric"]:hover {
            transform: translateY(-5px);
            border-color: #3b82f6 !important;
        }

        /* ── Sidebar ── */
        [data-testid="stSidebar"] {
            background-color: rgba(15, 23, 42, 0.95) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
        }

        /* ── Headings ── */
        h1, h2, h3 {
            font-family: 'Inter', sans-serif;
            font-weight: 700;
            background: linear-gradient(to right, #60a5fa, #a855f7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* ── Buttons ── */
        .stButton > button {
            border-radius: 10px !important;
            background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%) !important;
            color: white !important;
            border: none !important;
            font-weight: 600 !important;
            padding: 0.5rem 2rem !important;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4) !important;
        }

        /* ── Expander ── */
        [data-testid="stExpander"] {
            background: rgba(30, 41, 59, 0.4) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 12px !important;
        }

        /* ── Divider ── */
        hr {
            border-color: rgba(255, 255, 255, 0.08) !important;
        }
        </style>
    """, unsafe_allow_html=True)
