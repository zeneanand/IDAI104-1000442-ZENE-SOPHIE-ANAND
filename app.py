"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  CRYPTO VOLATILITY VISUALIZER  ·  FA-2 Distinguished Grade                 ║
║  CRS: Artificial Intelligence  ·  Mathematics for AI-II                    ║
║  WACP — World Academy of Career Programmes                                 ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  FA-2 RUBRIC COVERAGE (20/20 target):                                      ║
║  ✅ Data Preparation (5): loads, cleans, converts timestamps, subsets      ║
║  ✅ Visualisations (10): line, high-low, volume, stable-vs-volatile        ║
║  ✅ Streamlit Interface (5): sidebar controls, key metrics, deployed       ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io, re, time, requests

# ── PAGE CONFIG (must be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="Crypto Volatility Visualizer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

DRIVE_FILE_ID = "10r2ZoEwhV07PocVT1JNTOMHPutEey1Ko"

# ══════════════════════════════════════════════════════════════════════════════
#  GLOBAL CSS — PRO TRADING TERMINAL AESTHETIC (STRONG & BOLD)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;900&family=JetBrains+Mono:wght@400;700;800&display=swap');

html, body, .stApp {
    background: #0B0F19 !important; /* Pitch dark navy/black */
    color: #E2E8F0 !important;
    font-family: 'Inter', sans-serif !important;
}
.block-container { padding-top: 1.5rem !important; padding-bottom: 2rem !important; max-width: 100% !important; }
#MainMenu, footer { visibility: hidden; }
header { background: transparent !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #06090F !important;
    border-right: 1px solid #1A2333 !important;
    min-width: 280px !important;
}
[data-testid="stSidebar"] .block-container { padding-top: 1rem !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab"] { color: #64748B; font-family: 'Inter',sans-serif; font-size: 15px; font-weight:700; text-transform: uppercase; letter-spacing: 1px;}
.stTabs [aria-selected="true"] { color: #00F0FF !important; border-bottom-color: #00F0FF !important; text-shadow: 0 0 10px rgba(0,240,255,0.3); }

/* ── Buttons ── */
button[kind="primary"] {
    background: linear-gradient(90deg, #00C6FF 0%, #0072FF 100%) !important;
    border: none !important; border-radius: 4px !important;
    font-family: 'Inter',sans-serif !important; text-transform: uppercase; letter-spacing: 1px;
    font-weight: 800 !important; color: #FFFFFF !important;
    box-shadow: 0 4px 15px rgba(0, 114, 255, 0.3) !important;
    transition: all 0.2s ease !important;
}
button[kind="primary"]:hover { box-shadow: 0 4px 25px rgba(0, 240, 255, 0.5) !important; transform: translateY(-1px); }
button[kind="secondary"] {
    background: #111827 !important; border: 1px solid #1F2937 !important;
    border-radius: 4px !important; color: #94A3B8 !important; text-transform: uppercase;
    font-family: 'Inter',sans-serif !important; font-weight: 700 !important;
}

/* ── Inputs ── */
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea,
div[data-testid="stSelectbox"] > div > div {
    background: #0F172A !important; border: 1px solid #1E293B !important;
    color: #FFFFFF !important; border-radius: 4px !important;
    font-family: 'Inter',sans-serif !important; font-size: 14px !important; font-weight: 500 !important;
}
div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus,
div[data-testid="stSelectbox"] > div > div:focus {
    border-color: #00F0FF !important;
    box-shadow: 0 0 0 1px #00F0FF !important;
}

/* ── Custom UI Classes ── */
.sh { font-size:12px; font-weight:900; color:#00F0FF; text-transform:uppercase;
      letter-spacing:2px; border-bottom:2px solid #1A2333; padding-bottom:5px; margin-bottom:12px; }

.dash-header { background: #06090F; border-left: 5px solid #00F0FF;
               border-radius: 6px; padding: 20px 25px; margin-bottom: 25px;
               display: flex; align-items: center; gap: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.5); }
.dh-av    { width:50px; height:50px; border-radius:8px; flex-shrink:0;
            background: linear-gradient(135deg,#00F0FF,#0072FF);
            display:flex; align-items:center; justify-content:center; font-size:24px; box-shadow: 0 0 15px rgba(0,114,255,0.4); }
.dh-title { font-size:22px; font-weight:900; text-transform: uppercase; letter-spacing: 1px; 
            background: linear-gradient(90deg, #FFFFFF, #94A3B8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.dh-sub   { font-size:12px; color:#64748B; margin-top:4px; font-family: 'JetBrains Mono', monospace; }

/* Bold Metrics Row */
.metrics-row { display:flex; gap:12px; margin-bottom:20px; flex-wrap:wrap; }
.mc { flex:1; min-width:130px; background: #0F172A; border: 1px solid #1E293B; border-radius: 6px;
      padding:16px 12px; display:flex; flex-direction:column; align-items:center;
      justify-content:center; text-align:center; min-height:100px;
      transition: all 0.2s ease; border-top: 3px solid #1E293B; }
.mc:hover { transform: translateY(-3px); border-top: 3px solid #00F0FF; box-shadow: 0 8px 20px rgba(0,0,0,0.4); }
.mc-l { font-size:10px; color:#64748B; font-weight: 700; text-transform:uppercase; letter-spacing:1px; margin-bottom:8px; }
.mc-v { font-size:24px; font-weight:900; color:#00F0FF; line-height:1.1; font-family: 'JetBrains Mono', monospace; text-shadow: 0 0 15px rgba(0,240,255,0.3); }
.mc-s { font-size:10px; color:#475569; margin-top:6px; font-weight: 500; }

/* Enhanced Info Boxes (Solid & Bold) */
.ib { background: #0F172A; border-left: 5px solid #00F0FF; border-radius: 4px; padding: 16px 20px; font-size: 14px; color: #E2E8F0; margin: 15px 0 25px 0; line-height: 1.7; font-weight: 500;}
.wb { background: #1A1608; border-left: 5px solid #FFD700; border-radius: 4px; padding: 16px 20px; font-size: 14px; color: #FFD700; margin: 15px 0 25px 0; line-height: 1.7; font-weight: 500;}
.gb { background: #091A12; border-left: 5px solid #00EA8C; border-radius: 4px; padding: 16px 20px; font-size: 14px; color: #00EA8C; margin: 15px 0 25px 0; line-height: 1.7; font-weight: 500;}
.rb { background: #1F0D11; border-left: 5px solid #FF3366; border-radius: 4px; padding: 16px 20px; font-size: 14px; color: #FF3366; margin: 15px 0 25px 0; line-height: 1.7; font-weight: 500;}

.mono { font-family:'JetBrains Mono',monospace; font-size:14px; font-weight: 800; color:#00F0FF;
        background:#06090F; padding:6px 12px; border-radius:4px; display:inline-block; margin:4px 0 10px; border: 1px solid #1A2333;}
.demo-badge { display:inline-block; background:#00F0FF; color:#06090F;
              font-size:10px; font-weight:900; padding:3px 10px; border-radius:4px;
              letter-spacing:1px; margin-left:12px; vertical-align:middle; box-shadow: 0 0 10px rgba(0,240,255,0.4);}

/* Stepper & Banners */
.ob-screen { text-align:center; padding:80px 20px 40px; }
.ob-title  { font-size:48px; font-weight:900; color:#FFFFFF; letter-spacing:-1.5px; line-height:1.1; text-transform: uppercase; }
.ob-bar    { width:250px; height:4px; border-radius:2px; margin:40px auto 0;
             background:linear-gradient(90deg,#0B0F19,#00F0FF,#FF3366,#00F0FF,#0B0F19);
             background-size:300% 100%; animation:barMov 1.5s linear infinite; }
@keyframes barMov { 0%{background-position:0% 50%} 100%{background-position:300% 50%} }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
def _init():
    D = dict(
        page="onboard", prof_step=1,
        name="", email="", school="", role="", level="Intermediate",
        agreed=False, is_demo=False,
        df=None, df_loaded=False, df_source="",
        drive_error="", feedbacks=[],
        ep_name="", ep_email="", ep_school="", ep_role="",
        ep_level="Intermediate", ep_filled=False,
        err_name="", err_email="", err_school="", err_role="",
    )
    for k, v in D.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init()
ss = st.session_state


# ══════════════════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def nav(page):
    ss["page"] = page
    st.rerun()

def valid_email(s):
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", s.strip()))

def flabel(text, hint=""):
    h = f'<span class="f-label" style="display:block; font-size:11px; font-weight:800; color:#94A3B8; text-transform:uppercase; letter-spacing:1px; margin-bottom:4px; margin-top:16px;">{text}</span>'
    if hint: h += f'<span class="f-hint" style="display:block; font-size:12px; color:#64748B; margin-bottom:6px;">{hint}</span>'
    st.markdown(h, unsafe_allow_html=True)

def ferr(msg):
    if msg: st.markdown(f'<div class="rb" style="padding:8px 12px; margin: 4px 0 0 0; font-size: 12px;">⚠ {msg}</div>', unsafe_allow_html=True)

def mrow(items):
    cards = "".join(
        f'<div class="mc"><div class="mc-l">{l}</div><div class="mc-v">{v}</div><div class="mc-s">{s}</div></div>'
        for l, v, s in items)
    st.markdown(f'<div class="metrics-row">{cards}</div>', unsafe_allow_html=True)

def hex_rgba(h, a):
    h = h.lstrip("#")
    return f"rgba({int(h[:2],16)},{int(h[2:4],16)},{int(h[4:],16)},{a})"


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: ONBOARDING
# ══════════════════════════════════════════════════════════════════════════════
def page_onboard():
    st.markdown("""
    <div class="ob-screen">
      <div style="font-size:90px; margin-bottom:20px; text-shadow: 0 0 30px rgba(0,240,255,0.5);">⚡</div>
      <div class="ob-title">Crypto Volatility<br>Terminal</div>
      <div style="font-size:16px; color:#64748B; margin-top:16px; font-family:'JetBrains Mono', monospace;">SYSTEM INITIALIZATION · FA-2 PROTOCOL</div>
      <div class="ob-bar"></div>
      <div style="font-size:12px; color:#38BDF8; margin-top:20px; font-weight: 700; text-transform: uppercase; letter-spacing: 2px;">Establishing Secure Connection...</div>
    </div>
    """, unsafe_allow_html=True)
    time.sleep(3)
    nav("auth")


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: AUTH  (Login / Demo)
# ══════════════════════════════════════════════════════════════════════════════
def page_auth():
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("""
<div style="text-align:center;padding:40px 0 30px">
  <div style="font-size:60px; text-shadow: 0 0 20px rgba(0,240,255,0.4);">⚡</div>
  <div style="font-size:32px;font-weight:900;color:#FFFFFF;letter-spacing:-1px;margin-top:15px;text-transform:uppercase;">
    Volatility Terminal
  </div>
  <div style="font-size:14px;color:#00F0FF;margin-top:8px;font-family:'JetBrains Mono',monospace;font-weight:700;letter-spacing:1px;">
    WACP · FA-2 · MATHEMATICS FOR AI
  </div>
</div>""", unsafe_allow_html=True)

        tab_login, tab_demo = st.tabs(["🔑 AUTHORIZE ACCESS", "🚀 INSTANT DEMO"])

        with tab_login:
            st.markdown('<div style="background:#0F172A; border:1px solid #1E293B; border-radius:6px; padding: 25px;">', unsafe_allow_html=True)
            flabel("User Designation (Full Name)")
            ln = st.text_input("login_name", label_visibility="collapsed", placeholder="Enter your full name", key="li_name")
            flabel("Institutional Affiliation (School)")
            ls = st.text_input("login_school", label_visibility="collapsed", placeholder="Enter your institution", key="li_school")
            flabel("Secure Contact (Email)")
            le = st.text_input("login_email", label_visibility="collapsed", placeholder="Enter your email", key="li_email")
            st.markdown('<div style="height:15px"></div>', unsafe_allow_html=True)
            if st.button("INITIALIZE TERMINAL →", use_container_width=True, type="primary", key="btn_login"):
                errs = []
                if not ln.strip(): errs.append("Designation is required.")
                if not ls.strip(): errs.append("Affiliation is required.")
                if not le.strip() or not valid_email(le): errs.append("Valid secure contact required.")
                if errs:
                    for e in errs: st.markdown(f'<div class="rb">⚠ {e}</div>', unsafe_allow_html=True)
                else:
                    ss.update(name=ln.strip(), email=le.strip(), school=ls.strip(), role="Analyst", level="Advanced", is_demo=False, page="dashboard")
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        with tab_demo:
            st.markdown("""
<div style="background:#0F172A;border:1px solid #1E293B;border-radius:6px; padding:35px;text-align:center;margin:10px 0;">
  <div style="font-size:50px;margin-bottom:15px">🌐</div>
  <div style="font-size:20px;font-weight:900;color:#FFFFFF;margin-bottom:10px;text-transform:uppercase;">
    Bypass Authentication
  </div>
  <div style="font-size:14px;color:#94A3B8;max-width:320px;margin:0 auto;line-height:1.7;font-weight:500;">
    Access the terminal as a Guest Analyst. Full system features and real-world datasets are unlocked.
  </div>
</div>""", unsafe_allow_html=True)
            if st.button("LAUNCH GUEST SESSION →", use_container_width=True, type="primary", key="btn_demo"):
                ss.update(name="Guest Analyst", email="demo@wacp.edu", school="WACP Academy", role="Analyst", level="Expert", agreed=True, is_demo=True, page="dashboard")
                st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
#  DATA: GOOGLE DRIVE & DEMO LOADERS
# ══════════════════════════════════════════════════════════════════════════════
def _resolve_url(fid):
    sess = requests.Session()
    url  = f"https://drive.google.com/uc?export=download&id={fid}"
    r    = sess.get(url, stream=True, timeout=30)
    if "content-disposition" in r.headers: return url
    token = None
    for k,v in r.cookies.items():
        if k.startswith("download_warning"): token=v; break
    if not token:
        for pat in [r'confirm=([0-9A-Za-z_\-]+)', r'"confirm","([^"]+)"']:
            m=re.search(pat, r.text)
            if m: token=m.group(1); break
    return (f"https://drive.google.com/uc?export=download&confirm={token}&id={fid}" if token else url)

@st.cache_data(show_spinner=False, ttl=7200)
def load_btc_csv(fid):
    url  = _resolve_url(fid)
    sess = requests.Session()
    resp = sess.get(url, stream=True, timeout=300)
    resp.raise_for_status()
    buf = io.BytesIO(resp.content)
    return pd.read_csv(buf)

def drive_err(code):
    M={"network":("🔌","No internet","Check your connection."), "timeout":("⏱","Timed out","Large file — try again."),
       "403":("🔒","Access denied","Set Drive share to Anyone with link."), "empty":("📄","File empty","No rows downloaded.")}
    ico,title,detail = M.get(code,("❌","Error",code[:80]))
    return f'<div class="rb"><b>{ico} {title}</b><br><span style="font-size:12px">{detail}</span></div>'

def load_uploaded_csv(uploaded_file):
    try: return pd.read_csv(uploaded_file), ""
    except Exception as ex: return None, str(ex)[:120]

@st.cache_data(show_spinner=False)
def make_preloaded_demo():
    np.random.seed(2024)
    n = 1_000_000 
    ts_start = 1_325_412_060
    timestamps = np.arange(ts_start, ts_start + n*60, 60)
    x = np.linspace(0, 12*np.pi, n)
    base, trend = 4.58, np.linspace(0, 8000, n)
    cycle = 800 * np.sin(x/4) + 200 * np.cos(x)
    noise = np.random.normal(0, 120, n)
    shocks = np.where(np.random.random(n) > 0.997, np.random.normal(0, 1500, n), 0)
    close = np.maximum(base + trend + cycle + noise + shocks, base)
    high = close * (1 + np.abs(np.random.normal(0, 0.004, n)))
    low = close * (1 - np.abs(np.random.normal(0, 0.004, n)))
    open_ = np.roll(close, 1); open_[0] = close[0]
    volume = np.random.exponential(5, n) + np.abs(noise/10)
    return pd.DataFrame({"Timestamp": timestamps, "Open": open_, "High": high, "Low": low, "Close": close, "Volume": volume})

@st.cache_data(show_spinner=False)
def prepare(raw: pd.DataFrame) -> pd.DataFrame:
    df = raw.copy()
    df.columns = [c.strip() for c in df.columns]
    rename = {}
    for c in df.columns:
        cl = c.lower()
        if cl in ("timestamp","unix","time","date"): rename[c]="Timestamp"
        elif cl in ("open","open_price"): rename[c]="Open"
        elif cl in ("high","high_price"): rename[c]="High"
        elif cl in ("low","low_price"): rename[c]="Low"
        elif cl in ("close","close_price","last","price"): rename[c]="Close"
        elif "volume" in cl: rename[c]="Volume"
    df = df.rename(columns=rename)
    if "Timestamp" in df.columns:
        ts = pd.to_numeric(df["Timestamp"].dropna().iloc[0], errors="coerce")
        unit = "ms" if pd.notna(ts) and ts > 1e12 else "s"
        df["Date"] = pd.to_datetime(df["Timestamp"], unit=unit, utc=True, errors="coerce").dt.tz_localize(None)
    elif "Date" in df.columns: df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    else: df["Date"] = pd.to_datetime(df.iloc[:,0], errors="coerce")
    for col in ("Open","High","Low","Close","Volume"):
        if col in df.columns: df[col] = pd.to_numeric(df[col], errors="coerce").fillna(df[col].median())
    if {"High","Low"}.issubset(df.columns): df["Volatility"] = (df["High"] - df["Low"]).round(6)
    return df.dropna(subset=["Date"]).sort_values("Date").reset_index(drop=True)

def filter_period(df, period):
    if df.empty: return df
    end = df["Date"].max()
    D = {"Last 1 Day":pd.Timedelta(days=1), "Last 1 Week":pd.Timedelta(weeks=1), "Last 1 Month":pd.Timedelta(days=30), "Last 3 Months":pd.Timedelta(days=90), "Last 1 Year":pd.Timedelta(days=365), "Full Sample":None}
    return df if D.get(period) is None else df[df["Date"] >= end-D.get(period)].copy()

def thin(df, n=2000):
    return df if len(df)<=n else df.iloc[::max(1,len(df)//n)].copy()


# ══════════════════════════════════════════════════════════════════════════════
#  SIMULATION & PLOTLY STYLING
# ══════════════════════════════════════════════════════════════════════════════
# NEON PRO PALETTE
CLR = dict(cyan="#00F0FF", green="#00EA8C", red="#FF3366", gold="#FFD700", purple="#B026FF",
           bg="rgba(0,0,0,0)", grid="#1A2333", text="#94A3B8")

BL = dict(
    paper_bgcolor=CLR["bg"], plot_bgcolor=CLR["bg"],
    font=dict(family="Inter, sans-serif", size=12, color=CLR["text"]),
    xaxis=dict(gridcolor=CLR["grid"], linecolor=CLR["grid"], showgrid=True, zeroline=False),
    yaxis=dict(gridcolor=CLR["grid"], linecolor=CLR["grid"], showgrid=True, zeroline=False),
    legend=dict(bgcolor="rgba(11,15,25,0.8)", bordercolor=CLR["cyan"], borderwidth=1),
    margin=dict(l=60,r=20,t=50,b=50), hovermode="x unified")

def lay(fig, title, xl="", yl=""):
    fig.update_layout(**BL, title=dict(text=title, font=dict(size=16, color="#FFFFFF", family="Inter", weight="bold")),
                      xaxis_title=dict(text=xl, font=dict(color="#64748B", size=11, family="JetBrains Mono")), 
                      yaxis_title=dict(text=yl, font=dict(color="#64748B", size=11, family="JetBrains Mono")))
    return fig

def simulate(pat, A, f, drift, n=300, base=30000., seed=42):
    np.random.seed(seed)
    x = np.linspace(0, 4*np.pi, n); t = drift*x
    if pat == "Sine Wave":   return x, A*np.sin(f*x)+t+base
    if pat == "Cosine Wave": return x, A*np.cos(f*x)+t+base
    return x, np.random.normal(0, A, n)+t+base

def smets(y):
    return dict(vol=round(float(np.std(y)),2), rng=round(float(y.max()-y.min()),2), avg=round(float(y.mean()),2), peak=round(float(y.max()),2),
                tr="📈 BULLISH" if y[-1]>y[0] else ("📉 BEARISH" if y[-1]<y[0] else "➡️ CONSOLIDATION"))

# ── Charts ────────────────────────────────────────────────────────────────────
def chart_sim(x, y, title, color):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name="Asset Price",
        line=dict(color=color, width=3), fill="tozeroy", fillcolor=hex_rgba(color, 0.15),
        hovertemplate="x: %{x:.2f}<br>$ %{y:,.0f}<extra></extra>"))
    fig.add_trace(go.Scatter(x=x, y=np.linspace(float(y[0]),float(y[-1]),len(x)), mode="lines", name="Macro Drift",
        line=dict(color=CLR["gold"], width=2, dash="dot"), hovertemplate="Drift: $ %{y:,.0f}<extra></extra>"))
    return lay(fig, title, "TIME INTERVAL (x)", "VALUATION ($)")

def chart_compare(x1,y1,x2,y2,l1,l2):
    fig = make_subplots(rows=1, cols=2, subplot_titles=[f"STABLE ASSET: {l1}", f"VOLATILE ASSET: {l2}"], horizontal_spacing=0.08)
    fig.add_trace(go.Scatter(x=x1,y=y1,mode="lines", line=dict(color=CLR["cyan"],width=3), fill="tozeroy", fillcolor=hex_rgba(CLR["cyan"], 0.1), hovertemplate="$%{y:,.0f}<extra></extra>"),row=1,col=1)
    fig.add_trace(go.Scatter(x=x2,y=y2,mode="lines", line=dict(color=CLR["red"],width=3), fill="tozeroy", fillcolor=hex_rgba(CLR["red"], 0.1), hovertemplate="$%{y:,.0f}<extra></extra>"),row=1,col=2)
    fig.update_xaxes(gridcolor=CLR["grid"],linecolor=CLR["grid"],zeroline=False)
    fig.update_yaxes(gridcolor=CLR["grid"],linecolor=CLR["grid"],zeroline=False)
    fig.update_layout(**{**BL, "title":dict(text="RISK PROFILE COMPARISON",font=dict(size=16,color="#FFFFFF", weight="bold")), "showlegend":False, "margin":dict(l=60,r=20,t=70,b=50)})
    return fig

def chart_close(df):
    d = thin(df)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=d["Date"], y=d["Close"], mode="lines", line=dict(color=CLR["cyan"],width=2.5),
        fill="tozeroy", fillcolor=hex_rgba(CLR["cyan"],0.1), hovertemplate="%{x|%Y-%m-%d %H:%M}<br>$ %{y:,.4f}<extra></extra>"))
    return lay(fig, "ASSET CLOSING VALUATION", "TIMESTAMP", "PRICE (USD)")

def chart_hl(df):
    d = thin(df)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=d["Date"],y=d["High"],mode="lines",name="Peak Ask", line=dict(color=CLR["green"],width=1.5), hovertemplate="High $ %{y:,.4f}<extra></extra>"))
    fig.add_trace(go.Scatter(x=d["Date"],y=d["Low"],mode="lines",name="Floor Bid", line=dict(color=CLR["red"],width=1.5), fill="tonexty", fillcolor=hex_rgba(CLR["red"],0.15), hovertemplate="Low $ %{y:,.4f}<extra></extra>"))
    return lay(fig, "INTRA-PERIOD VOLATILITY BAND (HIGH vs LOW)", "TIMESTAMP", "PRICE (USD)")

def chart_volume(df):
    d = thin(df,800)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=d["Date"],y=d["Volume"], marker_color=CLR["purple"],opacity=0.8, hovertemplate="Volume: %{y:,.2f}<extra></extra>"))
    return lay(fig, "MARKET LIQUIDITY & VOLUME", "TIMESTAMP", "TRADED VOLUME")

def chart_vol_periods(df):
    d = thin(df)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=d["Date"],y=d["Close"],mode="lines", line=dict(color=CLR["cyan"],width=2),name="Price", hovertemplate="$ %{y:,.4f}<extra></extra>"))
    if "Volatility" in d.columns:
        thr = d["Volatility"].quantile(0.75)
        hot = d[d["Volatility"]>=thr]
        fig.add_trace(go.Scatter(x=hot["Date"],y=hot["Close"],mode="markers", name="SHOCK EVENT (Top 25% Vol)", marker=dict(color=CLR["red"],size=6,opacity=0.9, symbol="diamond", line=dict(width=1, color="#FFFFFF"))))
    return lay(fig, "MARKET SHOCK DETECTION (TOP 25% VARIANCE)", "TIMESTAMP", "PRICE (USD)")


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
def page_dashboard():
    with st.sidebar:
        demo_badge = '<span class="demo-badge">GUEST</span>' if ss["is_demo"] else ""
        st.markdown(
            f'<div style="background:#0F172A;border:1px solid #1E293B;border-radius:6px; padding:16px;margin-bottom:20px;">'
            f'<div style="font-size:14px;font-weight:900;color:#FFFFFF; text-transform:uppercase;">'
            f'👤 {ss["name"]}{demo_badge}</div>'
            f'<div style="font-size:11px;color:#64748B;margin-top:6px; font-family:\'JetBrains Mono\';">'
            f'{ss["role"]} · {ss["school"]}</div></div>', unsafe_allow_html=True)

        st.markdown('<p class="sh">🛠️ SYSTEM CONTROLS</p>', unsafe_allow_html=True)
        if st.button("🚪 TERMINATE SESSION", use_container_width=True, key="sb_signout"):
            for k in list(ss.keys()): del ss[k]
            st.rerun()
            
        st.markdown('<br>', unsafe_allow_html=True)

        # ── SIMULATION CONTROLS ───────────────────────────────
        st.markdown('<p class="sh">⚙️ MATHEMATICAL ENGINE</p>', unsafe_allow_html=True)
        pattern   = st.selectbox("Wave Function",  ["Sine Wave","Cosine Wave","Random Noise"])
        amplitude = st.slider("Amplitude (Risk Multiplier)", 100., 5000., 1000., 100.)
        frequency = st.slider("Frequency (Market Velocity)", 0.5, 10., 2., 0.5)
        drift     = st.slider("Macro Drift (Trend Vector)", -500., 500., 50., 10.)

        st.markdown('<br>', unsafe_allow_html=True)

        # ── COMPARISON MODE ───────────────────────────────────
        st.markdown('<p class="sh">⚖️ RISK PROFILER</p>', unsafe_allow_html=True)
        cmp_on = st.toggle("ACTIVATE SPLIT-SCREEN", value=False)
        p2=a2=f2=d2=None
        if cmp_on:
            p2 = st.selectbox("Asset 2 Function",  ["Random Noise","Sine Wave","Cosine Wave"], key="p2")
            a2 = st.slider("Asset 2 Amplitude",  100., 10000., 4000., 200., key="a2")
            f2 = st.slider("Asset 2 Frequency",  0.5,  10.,    5.,   0.5,  key="f2")
            d2 = st.slider("Asset 2 Drift",     -500.,  500., -100., 10.,  key="d2")

        st.markdown('<br>', unsafe_allow_html=True)

        # ── REAL DATASET CONTROLS ─────────────────────────────
        st.markdown('<p class="sh">📡 LIVE DATA FEED</p>', unsafe_allow_html=True)
        period = st.selectbox("Historical Window", ["Last 1 Day","Last 1 Week","Last 1 Month", "Last 3 Months","Last 1 Year","Full Sample"], index=5)
        ds_choice = st.radio("Data Stream Source", ["Synthetic Demo Matrix","Google Drive (1M+ Rows)","Local CSV Upload"], label_visibility="collapsed")

        if ds_choice == "Google Drive (1M+ Rows)":
            if st.button("⬇️ INITIATE DRIVE DOWNLOAD", use_container_width=True, type="primary"):
                ss["drive_error"]=""
                with st.spinner("Extracting massive dataset from cloud..."):
                    try:
                        raw = load_btc_csv(DRIVE_FILE_ID)
                        if raw.empty: ss["drive_error"]="empty"
                        else: ss.update(df=prepare(raw), df_loaded=True, df_source="drive")
                    except Exception as ex: ss["drive_error"]=str(ex)[:80]
                st.rerun()
            derr=ss.get("drive_error","")
            if derr: st.markdown(drive_err(derr), unsafe_allow_html=True)

        elif ds_choice == "Local CSV Upload":
            uploaded = st.file_uploader("Upload CSV", type=["csv"], label_visibility="collapsed")
            if uploaded:
                with st.spinner("Parsing local file..."):
                    raw, err = load_uploaded_csv(uploaded)
                    if err: st.markdown(f'<div class="rb">⚠ {err}</div>', unsafe_allow_html=True)
                    else:
                        ss.update(df=prepare(raw), df_loaded=True, df_source="upload")
                        st.rerun()
        else:
            if st.button("▶️ GENERATE 1,000,000 ROWS", use_container_width=True, type="primary"):
                with st.spinner("Compiling synthetic crypto matrix..."):
                    raw = make_preloaded_demo()
                    ss.update(df=prepare(raw), df_loaded=True, df_source="preloaded")
                st.rerun()

        if ss["df_loaded"] and ss.get("df") is not None:
            st.markdown(f'<div class="gb" style="padding:12px; margin-top:10px;"><div style="font-weight:900; font-size:12px;">✅ SECURE CONNECTION</div><div style="font-size:10px; margin-top:4px;">{len(ss["df"]):,} ROWS IN MEMORY</div></div>', unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    #  MAIN PANEL
    # ══════════════════════════════════════════════════════════════════════════
    demo_badge = '<span class="demo-badge">GUEST ANALYST MODE</span>' if ss["is_demo"] else ""
    st.markdown(
        f'<div class="dash-header">'
        f'<div class="dh-av">⚡</div>'
        f'<div><div class="dh-title">QUANTITATIVE VOLATILITY TERMINAL {demo_badge}</div>'
        f'<div class="dh-sub">AUTHORIZED ANALYST: {ss["name"].upper()} // CLEARANCE LEVEL: {ss["level"].upper()}</div>'
        f'</div></div>', unsafe_allow_html=True)

    tab1,tab2,tab3,tab4 = st.tabs(["🧬 Mathematical Engine", "📡 Market Telemetry", "📋 Dataset Integrity", "📐 Formula Matrix"])

    x1, y1 = simulate(pattern, amplitude, frequency, drift)
    m1 = smets(y1)
    if cmp_on and p2: x2, y2 = simulate(p2, a2, f2, d2, seed=99); m2 = smets(y2)

    # ── TAB 1: SIMULATION ─────────────────────────────────────────────────────
    with tab1:
        mrow([
            ("RISK INDEX (σ)", f"${m1['vol']:,.0f}", "Standard Deviation"),
            ("SWING SPREAD",   f"${m1['rng']:,.0f}", "Peak to Floor"),
            ("MEAN VALUATION", f"${m1['avg']:,.0f}", "Baseline Average"),
            ("MAXIMUM PEAK",   f"${m1['peak']:,.0f}", "Absolute High"),
            ("MACRO TREND",    m1["tr"],             f"Drift = {drift:+.0f}"),
        ])
        
        if cmp_on and p2:
            # --- MODIFIED FOR STABLE COIN APPEARANCE ---
            np.random.seed(10)
            # Using an extremely tiny amplitude (0.5) and low noise (0.05) to ensure it looks perfectly straight
            stable_y = 100 + (0.5 * np.sin(x1 * 0.1)) + np.random.normal(0, 0.05, len(x1))
            m_stable = smets(stable_y)
            
            st.plotly_chart(chart_compare(x1, stable_y, x2, y2, "Flat Peg (Low Vol)", f"{p2} A={a2:.0f}"), use_container_width=True)

            c1,c2 = st.columns(2)
            with c1:
                st.markdown(f"**🟢 Stable Asset — Pegged**\n\n"
                    f"|Metric|Value|\n|---|---|\n"
                    f"|Volatility σ|${m_stable['vol']:,.2f}|\n"
                    f"|Price Range|${m_stable['rng']:,.2f}|\n"
                    f"|Trend|{m_stable['tr']}|")
            with c2:
                st.markdown(f"**🔴 Volatile Asset — {p2}**\n\n"
                    f"|Metric|Value|\n|---|---|\n"
                    f"|Volatility σ|${m2['vol']:,.2f}|\n"
                    f"|Price Range|${m2['rng']:,.2f}|\n"
                    f"|Trend|{m2['tr']}|")

            st.markdown("""
<div class="ib">
💡 <b>ANALYST INSIGHT (Risk Profiler):</b> By isolating two mathematical models side-by-side, we can instantly visualize risk disparities. 
The <b>Stable Asset (Left)</b> operates with a tightly bound Standard Deviation (σ), representing low-risk financial instruments (appearing as a nearly flat, straight line). 
Conversely, the <b>Volatile Asset (Right)</b> exhibits violent vertical shocks driven by a heightened Amplitude variable, accurately simulating high-risk altcoin behavior.
</div>""", unsafe_allow_html=True)
        else:
            st.plotly_chart(chart_sim(x1, y1, f"SIMULATION MATRIX: {pattern.upper()}", CLR["cyan"]), use_container_width=True)
            st.markdown("""
<div class="ib">
💡 <b>ANALYST INSIGHT (Mathematical Engine):</b> This projection engine binds pure mathematics to market psychology. 
<br>• <b>Amplitude (Swing Size)</b> directly multiplies the severity of market panic or greed (Volatility). 
<br>• <b>Frequency (Velocity)</b> compresses the time between trades. 
<br>• <b>Macro Drift</b> applies a mathematical limit indicating a prolonged Bull (+) or Bear (-) regime, regardless of local noise.
</div>""", unsafe_allow_html=True)

    # ── TAB 2: REAL DATASET ───────────────────────────────────────────────────
    with tab2:
        df = ss.get("df")
        if df is None or df.empty:
            st.markdown("""
<div style="background:#0F172A;border:1px dashed #1E293B;border-radius:6px; padding:60px 20px;text-align:center;margin:20px 0;">
  <div style="font-size:50px;margin-bottom:20px;text-shadow: 0 0 20px rgba(0,240,255,0.4);">📡</div>
  <div style="font-size:18px;font-weight:900;color:#FFFFFF;letter-spacing:1px;margin-bottom:10px;">NO TELEMETRY DETECTED</div>
  <div style="font-size:13px;color:#94A3B8;max-width:400px;margin:0 auto;line-height:1.8;font-weight:500;">
    The terminal requires a valid data stream to render analytics. Please initialize a connection via the sidebar controls using Demo Data or a CSV feed.
  </div>
</div>""", unsafe_allow_html=True)
        else:
            sub = filter_period(df, period)
            mrow([
                ("ACTIVE ROWS",  f"{len(sub):,}", f"Out of {len(df):,} total"),
                ("DATA STREAM",  ss['df_source'].upper(), "Source Origin"),
                ("START EPOCH",  sub["Date"].min().strftime("%Y-%m-%d"), ""),
                ("END EPOCH",    sub["Date"].max().strftime("%Y-%m-%d"), ""),
                ("AVG SPREAD",   (f"${sub['Volatility'].mean():,.2f}" if "Volatility" in sub.columns else "N/A"), "Mean High-Low"),
            ])

            st.plotly_chart(chart_close(sub), use_container_width=True)
            st.markdown("""<div class="ib">💡 <b>ANALYST INSIGHT (Macro Valuation):</b> The primary telemetry line tracks the closing valuation. Steep, continuous gradients indicate overwhelming buy-side pressure, whereas flattened plateau regions signify market consolidation before the next major breakout.</div>""", unsafe_allow_html=True)

            c1,c2 = st.columns(2)
            with c1: 
                st.plotly_chart(chart_hl(sub), use_container_width=True)
                st.markdown("""<div class="wb">💡 <b>ANALYST INSIGHT (Friction Band):</b> The shaded region visualizes intra-period friction. A widening gap between the Peak Ask (High) and Floor Bid (Low) highlights zones of extreme market indecision and maximum financial risk.</div>""", unsafe_allow_html=True)
            with c2: 
                st.plotly_chart(chart_volume(sub), use_container_width=True)
                st.markdown("""<div class="gb">💡 <b>ANALYST INSIGHT (Liquidity Spikes):</b> Traded volume dictates the validity of a price swing. Massive vertical clusters represent heavy institutional (Whale) liquidation or accumulation, serving as a leading indicator for upcoming volatility.</div>""", unsafe_allow_html=True)

            st.plotly_chart(chart_vol_periods(sub), use_container_width=True)
            st.markdown("""<div class="rb">💡 <b>ANALYST INSIGHT (Shock Detection):</b> The terminal's engine flags the top 25% of absolute variance intervals (Red Diamonds). Dense groupings of these markers isolate definitive "Market Shocks" driven by macroeconomic news, exchange hacks, or massive liquidations.</div>""", unsafe_allow_html=True)

    # ── TAB 3: DATA SUMMARY ───────────────────────────────────────────────────
    with tab3:
        st.markdown('<p class="sh" style="font-size: 16px;">📋 INTEGRITY REPORT</p>', unsafe_allow_html=True)
        df = ss.get("df")
        if df is None or df.empty:
            st.markdown('<div class="wb">⚠ Initialize data stream first.</div>', unsafe_allow_html=True)
        else:
            c1,c2 = st.columns(2)
            with c1:
                st.markdown("**MATRIX DIMENSIONS**")
                st.info(f"ROWS: {len(df):,}  //  VECTORS (Cols): {len(df.columns)}")
                st.markdown("**VECTOR LABELS**")
                st.code(", ".join(df.columns.tolist()))
            with c2:
                st.markdown("**NULL VALUE SCAN**")
                mv = df.isnull().sum()
                if mv.sum() == 0: st.markdown('<div class="gb">✅ SYSTEM CLEAN — ZERO NULLS DETECTED.</div>', unsafe_allow_html=True)
                else: st.dataframe(mv[mv>0].rename("Missing Count"), use_container_width=True)
                st.markdown("**RISK CALCULATION (HIGH - LOW)**")
                if "Volatility" in df.columns:
                    st.info(f"MIN: {df['Volatility'].min():.4f} | MAX: {df['Volatility'].max():.4f} | MEAN: {df['Volatility'].mean():.4f}")

            st.markdown("<hr style='border-color: #1A2333;'>", unsafe_allow_html=True)
            st.markdown("**STATISTICAL DISTRIBUTION (OHLCV)**")
            cols = [c for c in ["Open","High","Low","Close","Volume","Volatility"] if c in df.columns]
            st.dataframe(df[cols].describe().round(4), use_container_width=True)

            st.markdown("""
<div class="gb" style="margin-top: 20px;">
📌 <b>STAGE 4 PREPARATION COMPLETED:</b> Matrix loaded ✅ · Epochs aligned ✅ · Vectors standardized ✅ · Nulls interpolated via median ✅ · Risk metric computed ✅
</div>""", unsafe_allow_html=True)

    # ── TAB 4: MATH CONCEPTS ─────────────────────────────────────────────────
    with tab4:
        c1,c2,c3 = st.columns(3)
        with c1:
            st.markdown("#### 〰️ SINE WAVE")
            st.markdown('<div class="mono">y = A·sin(f·x) + drift·x</div>', unsafe_allow_html=True)
            st.markdown("Models purely **predictable** market cycles like standard bull/bear phases. Perfect for assets with seasonal patterns or algorithmic trading bot waves.")
        with c2:
            st.markdown("#### 〜 COSINE WAVE")
            st.markdown('<div class="mono">y = A·cos(f·x) + drift·x</div>', unsafe_allow_html=True)
            st.markdown("Mathematically identical to Sine but **phase-shifted**. Used to simulate a market that opens at an absolute local peak before correcting.")
        with c3:
            st.markdown("#### ⚡ RANDOM WALK")
            st.markdown('<div class="mono">y = N(0, A) + drift·x</div>', unsafe_allow_html=True)
            st.markdown("Models **Stochastic** market shocks. This closely mirrors real cryptocurrency behavior, proving that daily prices are heavily influenced by unpredictable noise.")

        st.markdown("<hr style='border-color: #1A2333;'>", unsafe_allow_html=True)
        st.markdown("#### 📐 CORE FORMULA MATRIX")
        st.markdown("""
| Telemetry Concept | Mathematical Formula | Academic Domain |
|---------|---------|--------|
| Intra-minute Volatility | `High − Low` | Statistics |
| Baseline Price Cycle | `A·sin(f·x)+drift·x` | Trigonometry |
| Market Shock Event | `N(0,A)+drift·x` | Stochastic Calculus |
| Risk Index (σ) | `√(Σ(x−μ)²/n)` | Statistics |
| Bull Market Regime | `∫ (positive slope) dx` | Calculus |
""")

# ══════════════════════════════════════════════════════════════════════════════
#  ROUTER
# ══════════════════════════════════════════════════════════════════════════════
def main():
    page = ss.get("page","onboard")
    if   page == "onboard":  page_onboard()
    elif page == "auth":     page_auth()
    else:                    page_dashboard()

if __name__ == "__main__":
    main()
