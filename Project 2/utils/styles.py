import streamlit as st


def apply_custom_css():
    st.markdown("""
    <style>
        .stAppHeader { background: linear-gradient(135deg, #1a1a2e, #16213e) !important; }
        .stApp { background: #0f0f1a; }
        .block-container { padding-top: 1.5rem !important; }

        h1, h2, h3 { color: #e0e0ff !important; font-weight: 600 !important; }
        h1 { background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2.2rem !important; margin-bottom: 0.3rem !important; }
        .subtitle { color: #8888aa; font-size: 1rem; margin-bottom: 1.5rem; margin-top: -0.3rem; }

        .stButton > button {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white; border: none; border-radius: 8px; padding: 0.5rem 1.5rem;
            font-weight: 500; transition: all 0.2s; box-shadow: 0 4px 15px rgba(102,126,234,0.3);
        }
        .stButton > button:hover {
            transform: translateY(-2px); box-shadow: 0 6px 20px rgba(102,126,234,0.5);
        }
        .stButton > button[kind="secondary"] {
            background: transparent; border: 1px solid #667eea; color: #667eea;
            box-shadow: none;
        }
        .stButton > button[kind="secondary"]:hover {
            background: rgba(102,126,234,0.1); border-color: #764ba2; color: #764ba2;
        }

        div[data-testid="stMetric"] {
            background: linear-gradient(135deg, #1a1a3e, #16213e);
            border: 1px solid #2a2a5e; border-radius: 12px; padding: 1rem 0.8rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }
        div[data-testid="stMetric"] label { color: #8888bb !important; font-size: 0.8rem !important; text-transform: uppercase; letter-spacing: 1px; }
        div[data-testid="stMetric"] [data-testid="stMetricValue"] { color: #e0e0ff !important; font-size: 1.6rem !important; font-weight: 700; }

        div[data-testid="stExpander"] {
            border: 1px solid #2a2a5e !important; border-radius: 10px !important;
            background: linear-gradient(135deg, #14142a, #1a1a35);
            margin-bottom: 0.5rem;
        }
        div[data-testid="stExpander"] summary { color: #c0c0e0 !important; font-weight: 500; padding: 0.5rem 0; }
        div[data-testid="stExpander"] summary:hover { color: #667eea !important; }

        .stTextArea textarea, div[data-testid="stFileUploader"] {
            background: #14142a !important; border: 1px solid #2a2a5e !important;
            border-radius: 8px !important; color: #e0e0ff !important;
        }
        .stTextArea textarea:focus { border-color: #667eea !important; box-shadow: 0 0 10px rgba(102,126,234,0.2); }

        div[data-testid="stFileUploader"] { padding: 0.5rem; }
        div[data-testid="stFileUploader"] section { border: 1px dashed #3a3a6e !important; border-radius: 8px !important; padding: 1.5rem; }

        div[data-testid="stDataFrame"] { border: 1px solid #2a2a5e !important; border-radius: 10px !important; overflow: hidden; }
        .stDataFrame thead tr th { background: #1a1a3e !important; color: #667eea !important; font-weight: 600; }
        .stDataFrame tbody tr:nth-child(even) { background: rgba(20,20,42,0.5); }
        .stDataFrame tbody tr:hover { background: rgba(102,126,234,0.1); }

        div[data-testid="stAlert"] {
            background: linear-gradient(135deg, #1a1a3e, #16213e);
            border: 1px solid #2a2a5e; border-radius: 10px; color: #c0c0e0;
        }
        .stAlert > div[data-testid="stMarkdownContainer"] p { color: #c0c0e0; }

        .stProgress > div > div > div { background: linear-gradient(135deg, #667eea, #764ba2); }

        div[data-baseweb="tab-list"] { border-bottom: 1px solid #2a2a5e; }
        button[data-baseweb="tab"] { color: #8888bb !important; font-weight: 500; }
        button[data-baseweb="tab"][aria-selected="true"] { color: #667eea !important; border-bottom: 2px solid #667eea; }

        .st-spinner { color: #667eea !important; }

        .card {
            background: linear-gradient(135deg, #14142a, #1a1a35);
            border: 1px solid #2a2a5e; border-radius: 12px; padding: 1.2rem;
            margin-bottom: 0.8rem; box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        .card-title { color: #e0e0ff; font-size: 1.05rem; font-weight: 600; margin-bottom: 0.3rem; }
        .card-meta { color: #8888bb; font-size: 0.85rem; }
        .badge {
            display: inline-block; background: linear-gradient(135deg, #667eea33, #764ba233);
            color: #a0a0ff; padding: 0.15rem 0.6rem; border-radius: 12px;
            font-size: 0.75rem; border: 1px solid #3a3a7e; margin-right: 0.3rem; margin-bottom: 0.2rem;
        }

        .status-dot {
            display: inline-block; width: 10px; height: 10px; border-radius: 50%;
            margin-right: 6px;
        }
        .status-dot.green { background: #00cc88; box-shadow: 0 0 8px #00cc8866; }
        .status-dot.yellow { background: #ffaa33; box-shadow: 0 0 8px #ffaa3366; }
        .status-dot.red { background: #ff4466; box-shadow: 0 0 8px #ff446666; }

        hr { border-color: #2a2a5e !important; margin: 1.5rem 0; }

        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: #0f0f1a; }
        ::-webkit-scrollbar-thumb { background: #2a2a5e; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #3a3a7e; }
    </style>
    """, unsafe_allow_html=True)


def status_badge(text: str, status: str):
    dot_color = {"ready": "green", "pending": "yellow", "missing": "red"}.get(status, "yellow")
    return f'<span class="badge"><span class="status-dot {dot_color}"></span>{text}</span>'


def metric_card(title: str, value: str, extra: str = ""):
    col = st.columns(1)[0]
    with col:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#1a1a3e,#16213e);border:1px solid #2a2a5e;
                    border-radius:12px;padding:1rem 0.8rem;box-shadow:0 4px 15px rgba(0,0,0,0.3);
                    text-align:center;">
            <div style="color:#8888bb;font-size:0.75rem;text-transform:uppercase;letter-spacing:1px;">
                {title}</div>
            <div style="color:#e0e0ff;font-size:1.6rem;font-weight:700;">{value}</div>
            {f'<div style="color:#00cc88;font-size:0.75rem;margin-top:0.2rem;">{extra}</div>' if extra else ''}
        </div>
        """, unsafe_allow_html=True)


def section_header(text: str):
    st.markdown(f"<h2 style='margin-top:0.5rem;'>{text}</h2>", unsafe_allow_html=True)
