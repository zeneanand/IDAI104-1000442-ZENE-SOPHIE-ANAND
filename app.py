
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io, re, time, requests

# ── PAGE CONFIG (must be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="Crypto Volatility Visualizer",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",   # ← ALWAYS EXPANDED so sidebar shows
)

DRIVE_FILE_ID = "1BXxft5n2Hf8amI4cVtm4TfCrDKf-S45L"

# ══════════════════════════════════════════════════════════════════════════════
#  GLOBAL CSS — decorative only, zero interactive widget trapping
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, .stApp {
    background: #060D1A !important;
    color: #E2E8F0 !important;
    font-family: 'Space Grotesk', sans-serif !important;
}
.block-container { padding-top: 1.5rem !important; padding-bottom: 2rem !important; max-width: 100% !important; }
/* FIX 1: Removed 'header' from hidden so the Sidebar Arrow stays visible! */
#MainMenu, footer { visibility: hidden; }
header { background: transparent !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #080F1C !important;
    border-right: 1px solid #1E3A5F !important;
    min-width: 260px !important;
}
[data-testid="stSidebar"] .block-container { padding-top: 1rem !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab"] { color: #475569; font-family: 'Space Grotesk',sans-serif; font-size: 14px; font-weight:600; }
.stTabs [aria-selected="true"] { color: #38BDF8 !important; border-bottom-color: #38BDF8 !important; }

/* ── Buttons ── */
button[kind="primary"] {
    background: linear-gradient(135deg,#0EA5E9,#38BDF8) !important;
    border: none !important; border-radius: 10px !important;
    font-family: 'Space Grotesk',sans-serif !important;
    font-weight: 600 !important; color: #020917 !important;
}
button[kind="secondary"] {
    background: #0D1B2E !important; border: 1px solid #1E3A5F !important;
    border-radius: 10px !important; color: #94A3B8 !important;
    font-family: 'Space Grotesk',sans-serif !important;
}

/* ── Inputs ── */
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    background: #0A1628 !important; border: 1px solid #1E3A5F !important;
    color: #E2E8F0 !important; border-radius: 8px !important;
    font-family: 'Space Grotesk',sans-serif !important; font-size: 14px !important;
}
div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus {
    border-color: #38BDF8 !important;
    box-shadow: 0 0 0 2px rgba(56,189,248,.15) !important;
}
div[data-testid="stSelectbox"] > div > div {
    background: #0A1628 !important; border: 1px solid #1E3A5F !important;
    border-radius: 8px !important; color: #E2E8F0 !important;
}
div[data-testid="stFileUploader"] {
    background: #0A1628 !important; border: 1px dashed #1E3A5F !important;
    border-radius: 10px !important;
}

/* ── Decorative HTML helpers ── */
.ob-screen { text-align:center; padding:80px 20px 40px; }
.ob-logo   { font-size:80px; margin-bottom:24px; }
.ob-title  { font-size:42px; font-weight:700; color:#F8FAFC; letter-spacing:-1.5px; line-height:1.2; }
.ob-sub    { font-size:14px; color:#475569; margin-top:14px; }
.ob-bar    { width:220px; height:3px; border-radius:3px; margin:40px auto 0;
             background:linear-gradient(90deg,#0F1E33,#38BDF8,#818CF8,#38BDF8,#0F1E33);
             background-size:300% 100%; animation:barMov 2s linear infinite; }
@keyframes barMov { 0%{background-position:0% 50%} 100%{background-position:300% 50%} }
.ob-hint   { font-size:11px; color:#1E3A5F; margin-top:18px; }

.stepper { display:flex; align-items:center; justify-content:center; margin:0 auto 24px; max-width:340px; }
.s-step  { display:flex; flex-direction:column; align-items:center; }
.s-dot   { width:34px; height:34px; border-radius:50%; font-size:13px; font-weight:700;
           display:flex; align-items:center; justify-content:center;
           border:2px solid #1E3A5F; color:#334155; background:#080F1C; }
.s-dot.act  { border-color:#38BDF8; color:#38BDF8; background:rgba(56,189,248,.08); }
.s-dot.done { border-color:#34D399; color:#060D1A; background:#34D399; }
.s-lbl      { font-size:9px; color:#334155; margin-top:5px; }
.s-lbl.act  { color:#38BDF8; font-weight:600; }
.s-lbl.done { color:#34D399; }
.s-line     { width:60px; height:2px; background:#1E3A5F; margin-bottom:16px; }
.s-line.done { background:#34D399; }

.banner { background:linear-gradient(135deg,#080F1C,#0A1628); border:1px solid #1E3A5F;
          border-radius:14px; padding:22px 26px; margin-bottom:20px; }
.banner-icon  { font-size:32px; margin-bottom:10px; }
.banner-title { font-size:20px; font-weight:700; color:#F8FAFC; }
.banner-desc  { font-size:12px; color:#475569; margin-top:6px; line-height:1.6; }

.f-label { display:block; font-size:10px; font-weight:700; color:#64748B;
           text-transform:uppercase; letter-spacing:1px; margin-bottom:3px; margin-top:14px; }
.f-hint  { display:block; font-size:11px; color:#334155; margin-bottom:5px; line-height:1.5; }
.f-err   { background:#1A0707; border-left:3px solid #F87171; border-radius:0 6px 6px 0;
           padding:7px 12px; font-size:11px; color:#F87171; margin-top:4px; }

.terms-box { background:#080F1C; border:1px solid #1E3A5F; border-radius:10px;
             padding:16px; height:175px; overflow-y:auto;
             font-size:11px; color:#475569; line-height:1.9; margin-bottom:8px; }
.terms-box h4 { color:#64748B; font-size:11px; margin:10px 0 2px; }
.profile-summary { background:#080F1C; border:1px solid #1E3A5F; border-radius:10px;
                   padding:14px 18px; font-size:12px; color:#94A3B8; line-height:2.1; margin-bottom:12px; }

.dash-header { background:linear-gradient(90deg,#0A1628,#060D1A); border-left:4px solid #38BDF8;
               border-radius:10px; padding:16px 22px; margin-bottom:20px;
               display:flex; align-items:center; gap:16px; }
.dh-av    { width:44px; height:44px; border-radius:50%; flex-shrink:0;
            background:linear-gradient(135deg,#38BDF8,#818CF8);
            display:flex; align-items:center; justify-content:center; font-size:20px; }
.dh-title { font-size:17px; font-weight:700; color:#F8FAFC; }
.dh-sub   { font-size:11px; color:#64748B; margin-top:3px; }

.metrics-row { display:flex; gap:10px; margin-bottom:16px; flex-wrap:wrap; }
.mc { flex:1; min-width:110px; background:#0D1B2E; border:1px solid #1E3A5F; border-radius:12px;
      padding:14px 10px; display:flex; flex-direction:column; align-items:center;
      justify-content:center; text-align:center; min-height:90px;
      transition: transform 0.2s ease, box-shadow 0.2s ease; }
.mc:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(56,189,248,0.1); }
.mc-l { font-size:9px; color:#475569; text-transform:uppercase; letter-spacing:1px; margin-bottom:6px; }
.mc-v { font-size:19px; font-weight:700; color:#38BDF8; line-height:1.1; }
.mc-s { font-size:9px; color:#334155; margin-top:5px; }

.sh { font-size:10px; font-weight:700; color:#38BDF8; text-transform:uppercase;
      letter-spacing:2px; border-bottom:1px solid #1E3A5F; padding-bottom:5px; margin-bottom:10px; }

/* Enhanced Info Boxes */
.ib { background:linear-gradient(90deg,#0A1628,#080F1C); border-left:4px solid #38BDF8; border-radius:6px; padding:14px 18px; font-size:13px; color:#94A3B8; margin:10px 0 20px 0; line-height:1.6;}
.wb { background:linear-gradient(90deg,#1A1000,#080F1C); border-left:4px solid #FCD34D; border-radius:6px; padding:14px 18px; font-size:13px; color:#FCD34D; margin:10px 0 20px 0; line-height:1.6;}
.gb { background:linear-gradient(90deg,#081A0E,#080F1C); border-left:4px solid #34D399; border-radius:6px; padding:14px 18px; font-size:13px; color:#34D399; margin:10px 0 20px 0; line-height:1.6;}
.rb { background:linear-gradient(90deg,#1A0707,#080F1C); border-left:4px solid #F87171; border-radius:6px; padding:14px 18px; font-size:13px; color:#F87171; margin:10px 0 20px 0; line-height:1.6;}

.fb-card  { background:#0D1B2E; border:1px solid #1E3A5F; border-radius:12px; padding:18px 22px; margin-bottom:10px; }
.fb-name  { font-size:14px; font-weight:600; color:#F8FAFC; }
.fb-meta  { font-size:11px; color:#334155; }
.fb-stars { color:#FCD34D; font-size:14px; }
.fb-badge { background:#1E3A5F; color:#38BDF8; font-size:10px; padding:2px 10px; border-radius:20px; display:inline-block; margin:6px 0; }
.fb-body  { font-size:13px; color:#64748B; margin-top:8px; line-height:1.7; }
.fb-time  { font-size:10px; color:#1E3A5F; margin-top:8px; }

.mono { font-family:'JetBrains Mono',monospace; font-size:13px; color:#38BDF8;
        background:#080F1C; padding:4px 10px; border-radius:6px; display:inline-block; margin:4px 0 10px; }

.demo-badge { display:inline-block; background:#1E3A5F; color:#38BDF8;
              font-size:10px; font-weight:700; padding:2px 10px; border-radius:20px;
              letter-spacing:1px; margin-left:8px; vertical-align:middle; }
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
        df=None, df_loaded=False, df_source="",   # "drive" | "upload" | "preloaded"
        drive_error="",
        feedbacks=[],
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
    h = f'<span class="f-label">{text}</span>'
    if hint: h += f'<span class="f-hint">{hint}</span>'
    st.markdown(h, unsafe_allow_html=True)

def ferr(msg):
    if msg: st.markdown(f'<div class="f-err">⚠ {msg}</div>', unsafe_allow_html=True)

def mrow(items):
    cards = "".join(
         f'<div class="mc"><div class="mc-l" style="color: white;">{l}</div><div class="mc-v">{v}</div><div class="mc-s" style="color: white;">{s}</div></div>'
         for l, v, s in items
    )
    st.markdown(f'<div class="metrics-row">{cards}</div>', unsafe_allow_html=True)

def draw_stepper(current):
    steps = [("1","Identity"),("2","Academic"),("3","Agree")]
    h = '<div class="stepper">'
    for i,(num,label) in enumerate(steps):
        idx = i+1
        dc = "s-dot done" if idx<current else ("s-dot act" if idx==current else "s-dot")
        lc = "s-lbl done" if idx<current else ("s-lbl act"  if idx==current else "s-lbl")
        nd = "✓" if idx<current else num
        h += f'<div class="s-step"><div class="{dc}">{nd}</div><div class="{lc}">{label}</div></div>'
        if i < 2:
            h += f'<div class="s-line{"  done" if idx<current else ""}"></div>'
    st.markdown(h+"</div>", unsafe_allow_html=True)

def draw_banner(icon, title, desc):
    st.markdown(
        f'<div class="banner"><div class="banner-icon">{icon}</div>'
        f'<div class="banner-title">{title}</div>'
        f'<div class="banner-desc">{desc}</div></div>', unsafe_allow_html=True)

def hex_rgba(h, a):
    h = h.lstrip("#")
    return f"rgba({int(h[:2],16)},{int(h[2:4],16)},{int(h[4:],16)},{a})"


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: ONBOARDING (3-second splash + Start Journey)
# ══════════════════════════════════════════════════════════════════════════════
def page_onboard():
    # Only show the loading animation once.
    if not ss.get("loading_done", False):
        st.markdown("""
        <style>
        .ob-screen-anim { text-align:center; padding:80px 20px 40px; }
        </style>
        <div class="ob-screen-anim">
          <div class="ob-logo">📈</div>
          <div class="ob-title">Crypto Volatility<br>Visualizer</div>
          <div class="ob-sub">Mathematics for AI &nbsp;·&nbsp; FA-2 &nbsp;·&nbsp; CRS Artificial Intelligence</div>
          <div class="ob-bar"></div>
          <div class="ob-hint">Loading your experience…</div>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(3)
        ss["loading_done"] = True
        st.rerun()

    # The Hero Page with "Slide Up" effect, image background, text, and button.
    st.markdown("""
    <style>
    /* Trigger a slide-up keyframe on the main layout */
    @keyframes slideUp {
      0% { opacity: 0; transform: translateY(60px); }
      100% { opacity: 1; transform: translateY(0); }
    }
    
    .hero-container {
      animation: slideUp 1s cubic-bezier(0.16, 1, 0.3, 1) forwards;
      background: linear-gradient(135deg, rgba(6,13,26,0.95) 0%, rgba(10,22,40,0.85) 100%), 
                  url('https://images.unsplash.com/photo-1621504450181-5d356f61d307?q=80&w=2600&auto=format&fit=crop');
      background-size: cover;
      background-position: center;
      background-attachment: fixed;
      border-radius: 20px;
      border: 1px solid #1E3A5F;
      padding: 60px 40px;
      margin-top: 20px;
      min-height: 500px;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }
    
    .hero-title {
      font-size: 56px;
      font-weight: 700;
      color: #F8FAFC;
      letter-spacing: -1.5px;
      line-height: 1.1;
      margin-bottom: 20px;
      max-width: 600px;
    }
    
    .hero-title span {
      background: -webkit-linear-gradient(0deg, #0EA5E9, #38BDF8);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    
    .hero-desc {
      font-size: 16px;
      color: #94A3B8;
      line-height: 1.8;
      max-width: 550px;
      margin-bottom: 40px;
    }
    
    /* Adding neon glow shadow to the Streamlit primary button */
    .stButton > button[kind="primary"] {
      box-shadow: 0 0 20px rgba(14, 165, 233, 0.6);
      transition: all 0.3s ease;
    }
    
    .stButton > button[kind="primary"]:hover {
      box-shadow: 0 0 30px rgba(56, 189, 248, 0.9);
      transform: translateY(-2px);
    }
    </style>
    
    <div class="hero-container">
      <div class="hero-title">Crypto Volatility<br><span>Visualizer</span></div>
      <div class="hero-desc">
        Explore real-world market datasets, dive into complex mathematical models, and understand financial risk simulations like never before.<br><br>
        Built for the FA-2 Assessment in Mathematics for AI.
      </div>
    </div>
    <br>
    """, unsafe_allow_html=True)
    
    # We use columns to position the button cleanly on the left under the text
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Start Your Journey →", type="primary", use_container_width=True):
            nav("auth")


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: AUTH  (Login / Sign Up / Demo)
# ══════════════════════════════════════════════════════════════════════════════
def page_auth():
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("""
<div style="text-align:center;padding:5px 0 10px">
  <div style="font-size:42px">📈</div>
  <div style="font-size:22px;font-weight:700;color:#F8FAFC;letter-spacing:-1px;margin-top:5px">
    Crypto Volatility Visualizer
  </div>
</div>""", unsafe_allow_html=True)

        mode = ss.setdefault("auth_mode", "login")

        # ── COMMON CSS FOR AUTH ──────────────────────────────────────────────
        st.markdown("""
        <style>
        .auth-box {
            background: rgba(10, 22, 40, 0.4);
            border: 1px solid #1E3A5F;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
        }
        .demo-box {
            background: linear-gradient(135deg, rgba(14, 165, 233, 0.1), rgba(10, 22, 40, 0.8));
            border: 1px solid rgba(56, 189, 248, 0.3);
            border-radius: 16px;
            padding: 30px 20px;
            text-align: center;
            margin-top: 5px;
            box-shadow: 0 8px 32px rgba(56, 189, 248, 0.1);
        }
        .text-link-btn button {
            background: none !important;
            border: none !important;
            color: #38BDF8 !important;
            font-size: 13px !important;
            padding: 0 !important;
            box-shadow: none !important;
            margin-top: -5px;
        }
        .text-link-btn button:hover {
            color: #7DD3FC !important;
            text-decoration: underline !important;
        }
        /* Make form elements tighter */
        div[data-testid="stTextInput"] {
            margin-bottom: -10px;
        }
        </style>
        """, unsafe_allow_html=True)

        # ── LOGIN ────────────────────────────────────────────────────────────
        if mode == "login":
            # Using an invisible spacer to align text
            st.markdown('<div style="margin-top:10px;"></div>', unsafe_allow_html=True)
            flabel("Username / Email")
            em = st.text_input("login_email", label_visibility="collapsed",
                               placeholder="aditya@example.com", key="li_email")
            flabel("Password")
            pw = st.text_input("login_pwd", type="password", label_visibility="collapsed",
                               placeholder="••••••••", key="li_pwd")
            
            st.markdown('<div style="height:2px"></div>', unsafe_allow_html=True)
            
            # Row for text links
            link_col1, link_col2 = st.columns(2)
            with link_col1:
                st.markdown('<div class="text-link-btn" style="text-align:left;">', unsafe_allow_html=True)
                if st.button("Create an account", key="btn_to_signup"):
                    ss.update(auth_mode="signup")
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            with link_col2:
                st.markdown('<div class="text-link-btn" style="text-align:right;">', unsafe_allow_html=True)
                if st.button("Forgot Password?", key="btn_forgot"):
                    ss.update(auth_mode="forgot")
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div style="height:15px"></div>', unsafe_allow_html=True)
            
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                if st.button("Login →", use_container_width=True, type="primary", key="btn_login"):
                    errs = []
                    if not em.strip() or not valid_email(em): errs.append("Valid email required.")
                    if not pw.strip(): errs.append("Password is required.")
                    if errs:
                        for e in errs: st.markdown(f'<div class="rb" style="margin-top:5px; font-size:12px;">⚠ {e}</div>', unsafe_allow_html=True)
                    else:
                        ss.update(name="Aditya Sahani", email=em.strip(), school="Mumbai University",
                                  role="Student", level="Intermediate",
                                  is_demo=False, page="dashboard")
                        st.rerun()
                        
            with btn_col2:
                if st.button("Skip / Demo", use_container_width=True, key="btn_just_demo"):
                    ss.update(auth_mode="demo")
                    st.rerun()

        # ── SIGN UP ──────────────────────────────────────────────────────────
        elif mode == "signup":
            st.markdown('<div class="text-link-btn" style="margin-bottom:15px">', unsafe_allow_html=True)
            if st.button("← Back to Login", key="su_back_login"):
                ss.update(auth_mode="login")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

            draw_stepper(ss["prof_step"])
            draw_banner(
                ["👤","🎓","📋"][ss["prof_step"]-1],
                ["Create Your Profile","Role & Experience","Review & Agree"][ss["prof_step"]-1],
                ["All fields required to continue.",
                 "Helps personalise your dashboard.",
                 "Read the terms and enter the dashboard."][ss["prof_step"]-1])

            step = ss["prof_step"]

            if step == 1:
                flabel("Full Name","Your first and last name")
                name = st.text_input("su_name", label_visibility="collapsed",
                                     value=ss["name"], placeholder="e.g. Aditya Sahani", key="su_n")
                ferr(ss["err_name"])
                flabel("School / Institution","University or organisation")
                school = st.text_input("su_school", label_visibility="collapsed",
                                       value=ss["school"], placeholder="e.g. Mumbai University", key="su_s")
                ferr(ss["err_school"])
                flabel("Email Address","Session only — never shared externally")
                email = st.text_input("su_email", label_visibility="collapsed",
                                      value=ss["email"], placeholder="e.g. aditya@example.com", key="su_e")
                ferr(ss["err_email"])
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Continue Profile Setup →", use_container_width=True, type="primary", key="su_s1"):
                    en = "" if name.strip()  else "Name is required."
                    es = "" if school.strip() else "School is required."
                    ee = ("Email is required." if not email.strip()
                          else "" if valid_email(email) else "Enter a valid email.")
                    ss.update(err_name=en, err_school=es, err_email=ee)
                    if not any([en,es,ee]):
                        ss.update(name=name.strip(),school=school.strip(),
                                  email=email.strip(),prof_step=2)
                    st.rerun()

            elif step == 2:
                opts = ["","Student","Researcher","Data Analyst",
                        "FinTech Professional","Educator","Other"]
                cur  = opts.index(ss["role"]) if ss["role"] in opts else 0
                flabel("I am a…","Select your role")
                role = st.selectbox("su_role", opts, index=cur,
                                    label_visibility="collapsed",
                                    format_func=lambda x:"— Select role —" if x=="" else x, key="su_r")
                ferr(ss["err_role"])
                flabel("Experience Level","Comfort with maths & coding")
                level = st.select_slider("su_level",
                    options=["Beginner","Intermediate","Advanced","Expert"],
                    value=ss["level"], label_visibility="collapsed", key="su_lv")
                st.markdown("<br>", unsafe_allow_html=True)
                b1,b2 = st.columns(2)
                with b1:
                    if st.button("← Back", use_container_width=True, key="su_s2b"):
                        ss["prof_step"]=1; st.rerun()
                with b2:
                    if st.button("Continue to Terms →", use_container_width=True,
                                 type="primary", key="su_s2n"):
                        ss["err_role"] = "" if role else "Please select your role."
                        if not ss["err_role"]:
                            ss.update(role=role,level=level,prof_step=3)
                        st.rerun()

            else:  # step 3
                st.markdown("""
<div class="terms-box">
<h4>Terms of Use</h4>
<b>1. Educational Purpose</b><br>
Academic use only — CRS AI · Mathematics for AI-II · FA-2. Simulations are mathematical models, not financial advice.<br>
<h4></h4><b>2. Dataset</b><br>
btcusd_1-min_data.csv is public historical data for learning only.<br>
<h4></h4><b>3. Privacy</b><br>
Profile data stored in browser session only — never transmitted externally.<br>
<h4></h4><b>4. Intellectual Property</b><br>
Code, models and visualisations are original academic work.<br>
<h4></h4><b>5. Disclaimer</b><br>
Past patterns do not predict future behaviour. No liability assumed.<br>
<h4></h4><b>6. Academic Integrity</b><br>
You confirm ethical use per your institution's policies.
</div>""", unsafe_allow_html=True)
                st.markdown(
                    f'<div class="profile-summary">'
                    f'<b style="color:#38BDF8;font-size:10px">YOUR PROFILE</b><br>'
                    f'<b>{ss["name"]}</b> · {ss["email"]}<br>'
                    f'{ss["school"]}<br>{ss["role"]} · Level: {ss["level"]}'
                    f'</div>', unsafe_allow_html=True)
                agreed = st.checkbox("I have read and agree to the Terms of Use",
                                     value=ss["agreed"], key="su_agree")
                if not agreed:
                    st.markdown('<div class="wb">⚠ Tick the box to unlock the dashboard.</div>',
                                unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                b1,b2 = st.columns(2)
                with b1:
                    if st.button("← Back", use_container_width=True, key="su_s3b"):
                        ss["prof_step"]=2; st.rerun()
                with b2:
                    if st.button("🚀 Complete Sign Up", use_container_width=True,
                                 type="primary", key="su_s3n", disabled=not agreed):
                        ss.update(agreed=True, is_demo=False, page="dashboard")
                        st.rerun()

        # ── DEMO ─────────────────────────────────────────────────────────────
        elif mode == "demo":
            st.markdown('<div class="text-link-btn" style="margin-bottom:5px">', unsafe_allow_html=True)
            if st.button("← Back to Login", key="demo_back_login"):
                ss.update(auth_mode="login")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("""
<div class="demo-box">
  <div style="font-size:54px;margin-bottom:12px;filter:drop-shadow(0 0 10px rgba(56,189,248,0.5))">🚀</div>
  <div style="font-size:22px;font-weight:700;color:#F8FAFC;margin-bottom:12px">
    Instant Sandbox Access
  </div>
  <div style="font-size:14px;color:#94A3B8;margin:0 auto 24px auto;line-height:1.8;max-width:380px;">
    Skip the setup and jump straight into the data.<br>
    Explore the full dashboard, simulations, and charts with a temporary session.
  </div>
""", unsafe_allow_html=True)
            if st.button("Launch Sandbox Database →", use_container_width=True,
                         type="primary", key="btn_demo"):
                ss.update(
                    name="Demo User", email="demo@cryptoviz.app",
                    school="CRS Artificial Intelligence",
                    role="Student", level="Intermediate",
                    agreed=True, is_demo=True, page="dashboard")
                st.rerun()
            st.markdown("""
  <div style="font-size:11px;color:#475569;margin-top:16px;">
    <i>Note: All sandbox session data is cleared upon browser refresh.</i>
  </div>
</div>""", unsafe_allow_html=True)

        # ── FORGOT PASSWORD ──────────────────────────────────────────────────
        elif mode == "forgot":
            st.markdown('<div class="auth-box"><div class="auth-title"><i>🔒</i> Reset Password</div>', unsafe_allow_html=True)
            st.markdown('<div style="font-size:13px;color:#94A3B8;margin-bottom:20px;">Enter your email and we will send you a reset link.</div>', unsafe_allow_html=True)
            
            flabel("Email Address")
            em = st.text_input("forgot_email", label_visibility="collapsed",
                               placeholder="aditya@example.com", key="fg_email")
            
            st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
            if st.button("Send Reset Link", use_container_width=True, type="primary", key="btn_forgot_send"):
                st.success("If an account exists, a reset link has been sent.")
                
            st.markdown('<div class="text-link-btn" style="text-align:center;margin-top:20px;">', unsafe_allow_html=True)
            if st.button("← Back to Login", key="btn_forgot_back"):
                ss.update(auth_mode="login")
                st.rerun()
            st.markdown('</div></div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: EDIT PROFILE
# ══════════════════════════════════════════════════════════════════════════════
def page_edit():
    if not ss["ep_filled"]:
        ss.update(ep_name=ss["name"], ep_email=ss["email"], ep_school=ss["school"],
                  ep_role=ss["role"], ep_level=ss["level"], ep_filled=True)

    if st.button("← Back to Dashboard", key="edit_back"):
        ss.update(page="dashboard", ep_filled=False); st.rerun()

    st.markdown('<div style="font-size:22px;font-weight:700;color:#F8FAFC;margin-bottom:4px">✏️ Edit Profile</div>',
                unsafe_allow_html=True)
    st.markdown('<div style="font-size:12px;color:#475569;margin-bottom:20px">Changes apply to your current session immediately.</div>',
                unsafe_allow_html=True)

    _, col, _ = st.columns([1, 1.4, 1])
    with col:
        with st.form("edit_form"):
            flabel("Full Name")
            n  = st.text_input("ef_n",  label_visibility="collapsed", value=ss["ep_name"],  placeholder="Aditya Sahani")
            flabel("Email Address")
            e  = st.text_input("ef_e",  label_visibility="collapsed", value=ss["ep_email"],  placeholder="aditya@example.com")
            flabel("School / Institution")
            sc = st.text_input("ef_sc", label_visibility="collapsed", value=ss["ep_school"], placeholder="Mumbai University")
            flabel("Role")
            roles = ["Student","Researcher","Data Analyst","FinTech Professional","Educator","Other"]
            ri = roles.index(ss["ep_role"]) if ss["ep_role"] in roles else 0
            r  = st.selectbox("ef_r", roles, index=ri, label_visibility="collapsed")
            flabel("Experience Level")
            lv = st.select_slider("ef_lv",
                options=["Beginner","Intermediate","Advanced","Expert"],
                value=ss["ep_level"], label_visibility="collapsed")
            st.markdown("<br>", unsafe_allow_html=True)
            c1,c2 = st.columns(2)
            with c1: cancel = st.form_submit_button("Cancel",        use_container_width=True)
            with c2: save   = st.form_submit_button("💾 Save Changes", use_container_width=True, type="primary")
            if save:
                errs=[]
                if not n.strip():      errs.append("Name required.")
                if not valid_email(e): errs.append("Valid email required.")
                if not sc.strip():     errs.append("School required.")
                if errs:
                    for m in errs: st.markdown(f'<div class="rb">⚠ {m}</div>', unsafe_allow_html=True)
                else:
                    ss.update(name=n.strip(),email=e.strip(),school=sc.strip(),
                              role=r,level=lv,page="dashboard",ep_filled=False)
                    st.success("Profile updated!"); time.sleep(0.4); st.rerun()
            if cancel:
                ss.update(page="dashboard", ep_filled=False); st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: FEEDBACK FORM
# ══════════════════════════════════════════════════════════════════════════════
def page_feedback_form():
    if st.button("← Back to Dashboard", key="fb_back"):
        ss["page"]="dashboard"; st.rerun()

    st.markdown('<div style="font-size:22px;font-weight:700;color:#F8FAFC;margin-bottom:4px">💬 Share Your Feedback</div>',
                unsafe_allow_html=True)
    st.markdown('<div style="font-size:12px;color:#475569;margin-bottom:20px">Help improve this app — your feedback matters.</div>',
                unsafe_allow_html=True)

    _, col, _ = st.columns([1, 1.4, 1])
    with col:
        with st.form("fb_form", clear_on_submit=True):
            flabel("Overall Rating")
            rating = st.select_slider("fb_r",
                options=["1 - Poor","2 - Fair","3 - Good","4 - Great","5 - Excellent"],
                value="4 - Great", label_visibility="collapsed")
            flabel("Category")
            cat = st.selectbox("fb_cat",
                ["General","Simulation Charts","Real Dataset","UI / Design",
                 "Performance","Bug Report","Feature Request"],
                label_visibility="collapsed")
            flabel("Your Message","Be as detailed as you like")
            msg = st.text_area("fb_msg", label_visibility="collapsed",
                               placeholder="e.g. The comparison mode really helped me understand volatility…",
                               height=120)
            st.markdown("<br>", unsafe_allow_html=True)
            c1,c2 = st.columns(2)
            with c1: cancel = st.form_submit_button("Cancel", use_container_width=True)
            with c2: submit = st.form_submit_button("📨 Submit", use_container_width=True, type="primary")
            if submit:
                if not msg.strip():
                    st.markdown('<div class="rb">⚠ Please write a message.</div>', unsafe_allow_html=True)
                else:
                    ss["feedbacks"].append(dict(
                        name=ss["name"], role=ss["role"], school=ss["school"],
                        rating=int(rating[0]), category=cat,
                        message=msg.strip(), ts=time.strftime("%d %b %Y, %H:%M"),
                        demo=ss["is_demo"]))
                    ss["page"]="dashboard"
                    st.success("Thank you! Feedback submitted."); time.sleep(0.5); st.rerun()
            if cancel:
                ss["page"]="dashboard"; st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
#  DATA: GOOGLE DRIVE LOADER
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
    return (f"https://drive.google.com/uc?export=download&confirm={token}&id={fid}"
            if token else url)

@st.cache_data(show_spinner=False, ttl=7200)
def load_btc_csv(fid):
    url  = _resolve_url(fid)
    sess = requests.Session()
    resp = sess.get(url, stream=True, timeout=300)
    resp.raise_for_status()
    buf = io.BytesIO(resp.content)
    return pd.read_csv(buf)

def drive_err(code):
    M={"network":("🔌","No internet","Check your connection."),
       "timeout":("⏱","Timed out","Large file — try again."),
       "403":("🔒","Access denied","Set Drive share to Anyone with link → Viewer."),
       "404":("❌","File not found","Check DRIVE_FILE_ID."),
       "empty":("📄","File empty","No rows downloaded."),
       "csv":("⚠","Parse error","Check file is valid CSV.")}
    ico,title,detail = M.get(code,("❌","Error",code[:80]))
    return f'<div class="rb"><b>{ico} {title}</b><br><span style="font-size:11px">{detail}</span></div>'


# ══════════════════════════════════════════════════════════════════════════════
#  DATA: UPLOADED CSV LOADER
# ══════════════════════════════════════════════════════════════════════════════
def load_uploaded_csv(uploaded_file):
    """Load user-uploaded CSV file."""
    try:
        df = pd.read_csv(uploaded_file)
        return df, ""
    except Exception as ex:
        return None, str(ex)[:120]


# ══════════════════════════════════════════════════════════════════════════════
#  DATA: PRE-LOADED DEMO DATASET  (synthetic BTC-like, no download needed)
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data(show_spinner=False)
def make_preloaded_demo():
    """
    Generates a synthetic Bitcoin-style 1-minute OHLCV dataset.
    Uses sine + noise + drift to match FA-2 mathematical models.
    Rubric: Stage 4 Data Preparation — always available, no network needed.
    """
    np.random.seed(2024)
    # FIX 2: Increased demo data generation to 1 Million rows!
    n = 1_000_000 
    ts_start = 1_325_412_060  # Jan 2012 (same epoch as real dataset)
    timestamps = np.arange(ts_start, ts_start + n*60, 60)

    x = np.linspace(0, 12*np.pi, n)
    # BTC-like price: low-freq cycle + medium-freq noise + long drift + shocks
    base   = 4.58
    trend  = np.linspace(0, 8000, n)
    cycle  = 800 * np.sin(x/4) + 200 * np.cos(x)
    noise  = np.random.normal(0, 120, n)
    shocks = np.where(np.random.random(n) > 0.997,
                      np.random.normal(0, 1500, n), 0)
    close  = np.maximum(base + trend + cycle + noise + shocks, base)

    high   = close * (1 + np.abs(np.random.normal(0, 0.004, n)))
    low    = close * (1 - np.abs(np.random.normal(0, 0.004, n)))
    open_  = np.roll(close, 1); open_[0] = close[0]
    volume = np.random.exponential(5, n) + np.abs(noise/10)

    df = pd.DataFrame({
        "Timestamp": timestamps, "Open": open_, "High": high,
        "Low": low, "Close": close, "Volume": volume
    })
    return df


# ══════════════════════════════════════════════════════════════════════════════
#  DATA: PREPARATION (FA-2 Stage 4 — Distinguished Level)
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data(show_spinner=False)
def prepare(raw: pd.DataFrame) -> pd.DataFrame:
    """
    FA-2 Stage 4 Data Preparation:
    ✅ Loads dataset
    ✅ Renames columns to standard names
    ✅ Converts Unix Timestamp → datetime (auto-detects ms vs s)
    ✅ Converts all OHLCV columns to numeric
    ✅ Fills missing values with column median
    ✅ Computes Volatility = High − Low
    ✅ Sorts by date, drops bad rows
    """
    df = raw.copy()
    df.columns = [c.strip() for c in df.columns]

    # Rename to standard
    rename = {}
    for c in df.columns:
        cl = c.lower()
        if cl in ("timestamp","unix","time","date"):       rename[c]="Timestamp"
        elif cl in ("open","open_price"):                  rename[c]="Open"
        elif cl in ("high","high_price"):                  rename[c]="High"
        elif cl in ("low","low_price"):                    rename[c]="Low"
        elif cl in ("close","close_price","last","price"): rename[c]="Close"
        elif "volume" in cl:                               rename[c]="Volume"
    df = df.rename(columns=rename)

    # Parse timestamp
    if "Timestamp" in df.columns:
        ts = pd.to_numeric(df["Timestamp"].dropna().iloc[0], errors="coerce")
        unit = "ms" if pd.notna(ts) and ts > 1e12 else "s"
        df["Date"] = pd.to_datetime(df["Timestamp"], unit=unit, utc=True, errors="coerce")
        df["Date"] = df["Date"].dt.tz_localize(None)
    elif "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    else:
        df["Date"] = pd.to_datetime(df.iloc[:,0], errors="coerce")

    # Numeric + fill missing
    for col in ("Open","High","Low","Close","Volume"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            df[col] = df[col].fillna(df[col].median())

    # Volatility = High − Low  (core FA-2 metric)
    if {"High","Low"}.issubset(df.columns):
        df["Volatility"] = (df["High"] - df["Low"]).round(6)

    return df.dropna(subset=["Date"]).sort_values("Date").reset_index(drop=True)


def filter_period(df, period):
    if df.empty: return df
    end = df["Date"].max()
    D = {"Last 1 Day":pd.Timedelta(days=1), "Last 1 Week":pd.Timedelta(weeks=1),
         "Last 1 Month":pd.Timedelta(days=30), "Last 3 Months":pd.Timedelta(days=90),
         "Last 1 Year":pd.Timedelta(days=365), "Full Sample":None}
    d = D.get(period)
    return df if d is None else df[df["Date"] >= end-d].copy()

def thin(df, n=2000):
    # This brilliant function is what prevents Plotly from crashing when displaying 1M rows!
    return df if len(df)<=n else df.iloc[::max(1,len(df)//n)].copy()


# ══════════════════════════════════════════════════════════════════════════════
#  SIMULATION  (FA-2 Stage 5/6 — Mathematical Models)
# ══════════════════════════════════════════════════════════════════════════════
CLR = dict(sky="#38BDF8", green="#34D399", red="#F87171",
           purple="#818CF8", gold="#FCD34D",
           bg="#080F1C", grid="#1E3A5F", text="#64748B", paper="#060D1A")

BL = dict(
    paper_bgcolor=CLR["paper"], plot_bgcolor=CLR["bg"],
    font=dict(family="Space Grotesk, sans-serif", size=11, color=CLR["text"]),
    xaxis=dict(gridcolor=CLR["grid"], linecolor=CLR["grid"], showgrid=True, zeroline=False),
    yaxis=dict(gridcolor=CLR["grid"], linecolor=CLR["grid"], showgrid=True, zeroline=False),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=CLR["grid"], borderwidth=1),
    margin=dict(l=55,r=20,t=50,b=45), hovermode="x unified")

def lay(fig, title, xl="", yl=""):
    fig.update_layout(**BL,
        title=dict(text=title, font=dict(size=13, color="#E2E8F0")),
        xaxis_title=xl, yaxis_title=yl)
    return fig

def simulate(pat, A, f, drift, n=300, base=30000., seed=42):
    """
    FA-2 Mathematical Functions:
      Sine:   y = A·sin(f·x) + drift·x + base
      Cosine: y = A·cos(f·x) + drift·x + base
      Noise:  y = N(0, A)    + drift·x + base
    """
    np.random.seed(seed)
    x = np.linspace(0, 4*np.pi, n); t = drift*x
    if pat == "Sine Wave":   return x, A*np.sin(f*x)+t+base
    if pat == "Cosine Wave": return x, A*np.cos(f*x)+t+base
    return x, np.random.normal(0, A, n)+t+base

def smets(y):
    return dict(
        vol=round(float(np.std(y)),2), rng=round(float(y.max()-y.min()),2),
        avg=round(float(y.mean()),2),  peak=round(float(y.max()),2),
        tr="📈 Upward" if y[-1]>y[0] else ("📉 Downward" if y[-1]<y[0] else "➡️ Flat"))

# ── Charts ────────────────────────────────────────────────────────────────────
def chart_sim(x, y, title, color):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name="Price",
        line=dict(color=color, width=2.5),
        fill="tozeroy", fillcolor=hex_rgba(color, 0.10),
        hovertemplate="x: %{x:.2f}<br>$ %{y:,.0f}<extra></extra>"))
    fig.add_trace(go.Scatter(x=x,
        y=np.linspace(float(y[0]),float(y[-1]),len(x)),
        mode="lines", name="Drift",
        line=dict(color=CLR["gold"], width=1.5, dash="dot"),
        hovertemplate="Drift: $ %{y:,.0f}<extra></extra>"))
    return lay(fig, title, "Time (x)", "Simulated Price ($)")

def chart_compare(x1,y1,x2,y2,l1,l2):
    fig = make_subplots(rows=1, cols=2,
        subplot_titles=[f"STABLE: {l1}", f"VOLATILE: {l2}"],
        horizontal_spacing=0.06)
    fig.add_trace(go.Scatter(x=x1,y=y1,mode="lines",
        line=dict(color=CLR["green"],width=2.5),
        hovertemplate="$%{y:,.0f}<extra></extra>"),row=1,col=1)
    fig.add_trace(go.Scatter(x=x2,y=y2,mode="lines",
        line=dict(color=CLR["red"],width=2.5),
        hovertemplate="$%{y:,.0f}<extra></extra>"),row=1,col=2)
    fig.update_xaxes(gridcolor=CLR["grid"],linecolor=CLR["grid"],zeroline=False)
    fig.update_yaxes(gridcolor=CLR["grid"],linecolor=CLR["grid"],zeroline=False)
    fig.update_layout(**{**BL,
        "title":dict(text="Stable vs Volatile Market Comparison",font=dict(size=13,color="#E2E8F0")),
        "showlegend":False, "margin":dict(l=55,r=20,t=65,b=45)})
    return fig

def chart_close(df):
    d = thin(df)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=d["Date"], y=d["Close"], mode="lines",
        line=dict(color=CLR["sky"],width=2),
        fill="tozeroy", fillcolor=hex_rgba(CLR["sky"],0.07),
        hovertemplate="%{x|%Y-%m-%d %H:%M}<br>$ %{y:,.4f}<extra></extra>"))
    return lay(fig, "Bitcoin Close Price Over Time", "Date", "Close (USD)")

def chart_hl(df):
    d = thin(df)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=d["Date"],y=d["High"],mode="lines",name="High",
        line=dict(color=CLR["gold"],width=1.8),
        hovertemplate="High $ %{y:,.4f}<extra></extra>"))
    fig.add_trace(go.Scatter(x=d["Date"],y=d["Low"],mode="lines",name="Low",
        line=dict(color=CLR["red"],width=1.8),
        fill="tonexty", fillcolor=hex_rgba(CLR["red"],0.08),
        hovertemplate="Low $ %{y:,.4f}<extra></extra>"))
    return lay(fig, "High vs Low — Daily Volatility Band", "Date", "Price (USD)")

def chart_volume(df):
    d = thin(df,800)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=d["Date"],y=d["Volume"],
        marker_color=CLR["purple"],opacity=0.7,
        hovertemplate="Volume: %{y:,.2f}<extra></extra>"))
    return lay(fig, "Trading Volume (BTC)", "Date", "Volume")

def chart_vol_periods(df):
    d = thin(df)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=d["Date"],y=d["Close"],mode="lines",
        line=dict(color=CLR["sky"],width=1.5),name="Close",
        hovertemplate="$ %{y:,.4f}<extra></extra>"))
    if "Volatility" in d.columns:
        thr = d["Volatility"].quantile(0.75)
        hot = d[d["Volatility"]>=thr]
        fig.add_trace(go.Scatter(x=hot["Date"],y=hot["Close"],mode="markers",
            name="High Vol (top 25%)",
            marker=dict(color=CLR["red"],size=4,opacity=0.65)))
    return lay(fig, "Stable vs Volatile Periods  (red = top 25% volatility)",
               "Date", "Close (USD)")


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
def page_dashboard():
    # ══════════════════════════════════════════════════════════════════════════
    #  SIDEBAR  (must be rendered FIRST and UNCONDITIONALLY to stay visible)
    # ══════════════════════════════════════════════════════════════════════════
    with st.sidebar:
        # User badge
        demo_badge = '<span class="demo-badge">DEMO</span>' if ss["is_demo"] else ""
        st.markdown(
            f'<div style="background:#0D1B2E;border:1px solid #1E3A5F;border-radius:10px;'
            f'padding:12px 14px;margin-bottom:12px">'
            f'<div style="font-size:13px;font-weight:700;color:#F8FAFC">'
            f'👤 {ss["name"]}{demo_badge}</div>'
            f'<div style="font-size:10px;color:#475569;margin-top:3px">'
            f'{ss["role"]} · {ss["school"]}</div></div>',
            unsafe_allow_html=True)

        # Added Custom CSS to force exact equal heights and alignment on these specific buttons
        st.markdown("""
        <style>
        [data-testid="stSidebar"] div[data-testid="column"] button {
            height: 44px !important;
            padding: 0px 5px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            white-space: nowrap !important;
            overflow: hidden !important;
        }
        [data-testid="stSidebar"] div[data-testid="column"] button p {
            margin: 0 !important;
            padding: 0 !important;
            line-height: 1 !important;
            white-space: nowrap !important;
            font-size: 14px !important;
        }
        </style>
        """, unsafe_allow_html=True)

        c1,c2 = st.columns(2)
        with c1:
            if st.button("✏️ Edit",     use_container_width=True, key="sb_edit"):
                ss.update(page="edit", ep_filled=False); st.rerun()
        with c2:
            if st.button("💬 Feedback", use_container_width=True, key="sb_fb"):
                ss["page"]="feedback"; st.rerun()

        st.divider()

        # ── SIMULATION CONTROLS (FA-2 Stage 6) ───────────────────────────────
        st.markdown('<p class="sh">📊 SIMULATION</p>', unsafe_allow_html=True)
        pattern   = st.selectbox("Wave Pattern",  ["Sine Wave","Cosine Wave","Random Noise"])
        amplitude = st.slider("Amplitude (A — Volatility)", 100., 5000., 1000., 100.,
                              help="Controls price swing size. Higher = more volatile market.")
        frequency = st.slider("Frequency (f — Trading Speed)", 0.5, 10., 2., 0.5,
                              help="How fast price oscillates. Higher = more active market.")
        drift     = st.slider("Drift (Market Trend)", -500., 500., 50., 10.,
                              help="Long-term direction. +ve = Bull market, -ve = Bear market.")

        st.divider()

        # ── COMPARISON MODE (FA-2 Stage 6) ───────────────────────────────────
        st.markdown('<p class="sh">⚡ COMPARISON MODE</p>', unsafe_allow_html=True)
        cmp_on = st.toggle("Enable Side-by-Side", value=False,
                           help="Compare stable vs volatile patterns simultaneously.")
        p2=a2=f2=d2=None
        if cmp_on:
            p2 = st.selectbox("Pattern 2",  ["Random Noise","Sine Wave","Cosine Wave"], key="p2")
            a2 = st.slider("Amplitude 2",  100., 10000., 4000., 200., key="a2")
            f2 = st.slider("Frequency 2",  0.5,  10.,    5.,   0.5,  key="f2")
            d2 = st.slider("Drift 2",     -500.,  500., -100., 10.,  key="d2")

        st.divider()

        # ── REAL DATASET CONTROLS (FA-2 Stage 4) ─────────────────────────────
        st.markdown('<p class="sh">₿ REAL DATASET</p>', unsafe_allow_html=True)
        period = st.selectbox("Time Period",
            ["Last 1 Day","Last 1 Week","Last 1 Month",
             "Last 3 Months","Last 1 Year","Full Sample"], index=5)

        st.markdown('<p style="font-size:10px;color:#64748B;margin-bottom:8px">Data Source:</p>',
                    unsafe_allow_html=True)

        ds_choice = st.radio("data_src", ["Preloaded Data", "Upload Data"],
                             label_visibility="collapsed", key="ds_radio")

        if ds_choice == "Upload Data":
            uploaded = st.file_uploader("Upload your CSV", type=["csv"],
                                        key="csv_upload", label_visibility="collapsed")
            if uploaded is not None:
                with st.spinner("Processing uploaded file (reading all possible rows)…"):
                    raw, err = load_uploaded_csv(uploaded)
                    if err:
                        st.error(f"Error loading CSV file: {err}")
                    elif raw is None or raw.empty:
                        st.error("File is empty or contains no readable data.")
                    else:
                        try:
                            processed_df = prepare(raw)
                            ss.update(df=processed_df, df_loaded=True, df_source="upload")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Formatting failed. The CSV must have OHLCV columns. Error details: {str(e)}")
                            
            st.markdown("""
<div style="font-size:10px;color:#334155;margin-top:6px;line-height:1.8">
Required columns:<br>
<code>Timestamp, Open, High, Low, Close, Volume</code>
</div>""", unsafe_allow_html=True)

        else:  # Preloaded Data
            if st.button("▶️ Load Data", use_container_width=True,
                         type="primary", key="btn_preload"):
                with st.spinner("Generating full dataset (all possible rows)…"):
                    try:
                        raw = make_preloaded_demo()
                        ss.update(df=prepare(raw), df_loaded=True, df_source="preloaded")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error generating demo data: {str(e)}")

        # Dataset status
        if ss["df_loaded"] and ss.get("df") is not None:
            df0  = ss["df"]
            src  = {"upload":"Uploaded CSV","preloaded":"Preloaded Data"}.get(ss["df_source"],"Dataset")
            st.markdown(
                f'<div class="gb">✅ {len(df0):,} rows · {src}<br>'
                f'<span style="font-size:10px">'
                f'{df0["Date"].min().strftime("%b %Y")} → {df0["Date"].max().strftime("%b %Y")}'
                f'</span></div>', unsafe_allow_html=True)

        st.divider()

        # Sign out
        if st.button("🚪 Sign Out", use_container_width=True, key="sb_signout"):
            for k in list(ss.keys()): del ss[k]
            st.rerun()

    # ══════════════════════════════════════════════════════════════════════════
    #  MAIN PANEL
    # ══════════════════════════════════════════════════════════════════════════

    # ── Header ────────────────────────────────────────────────────────────────
    demo_badge = '<span class="demo-badge">DEMO MODE</span>' if ss["is_demo"] else ""
    st.markdown(
        f'<div class="dash-header">'
        f'<div class="dh-av">👤</div>'
        f'<div><div class="dh-title">📈 Crypto Volatility Visualizer{demo_badge}</div>'
        f'<div class="dh-sub">Welcome, <b style="color:#38BDF8">{ss["name"]}</b>'
        f' · {ss["role"]} · {ss["school"]} · Level: {ss["level"]}</div>'
        f'</div></div>', unsafe_allow_html=True)

    # ── Tabs ──────────────────────────────────────────────────────────────────
    tab1,tab2,tab3,tab4,tab5 = st.tabs([
        "📊 Simulation",
        "₿ Real Dataset",
        "📋 Data Summary",
        "💬 Feedback Wall",
        "📐 Math Concepts"])

    # Compute simulation data (shared across tabs)
    x1, y1 = simulate(pattern, amplitude, frequency, drift)
    m1 = smets(y1)
    if cmp_on and p2:
        x2, y2 = simulate(p2, a2, f2, d2, seed=99)
        m2 = smets(y2)

    # ── TAB 1: SIMULATION ─────────────────────────────────────────────────────
    with tab1:
        mrow([
            ("Volatility Index", f"${m1['vol']:,.0f}", "Std Dev σ"),
            ("Price Range",      f"${m1['rng']:,.0f}", "High − Low"),
            ("Average Price",    f"${m1['avg']:,.0f}", "Mean"),
            ("Peak Price",       f"${m1['peak']:,.0f}", "Max"),
            ("Average Drift",    f"{drift:+.0f}", "Mean Change"),
            ("Market Trend",      m1["tr"],             f"drift = {drift:+.0f}"),
        ])
        st.markdown("<br>", unsafe_allow_html=True)

        if cmp_on and p2:
            st.plotly_chart(chart_compare(x1,y1,x2,y2,
                f"{pattern} A={amplitude:.0f}",
                f"{p2} A={a2:.0f}"), use_container_width=True)

            c1,c2 = st.columns(2)
            with c1:
                st.markdown(f"**🟢 Stable Asset — {pattern}**\n\n"
                    f"|Metric|Value|\n|---|---|\n"
                    f"|Volatility σ|${m1['vol']:,.2f}|\n"
                    f"|Price Range|${m1['rng']:,.2f}|\n"
                    f"|Trend|{m1['tr']}|")
            with c2:
                st.markdown(f"**🔴 Volatile Asset — {p2}**\n\n"
                    f"|Metric|Value|\n|---|---|\n"
                    f"|Volatility σ|${m2['vol']:,.2f}|\n"
                    f"|Price Range|${m2['rng']:,.2f}|\n"
                    f"|Trend|{m2['tr']}|")

            st.markdown("""
<div class="ib">
💡 <b>Insightful Explanation (Risk Profiles):</b> When comparing the STABLE and VOLATILE panels side-by-side, notice the vast difference in the Standard Deviation (σ). The STABLE pattern hugs closely to its mean with a tiny price range (low risk/low reward). Conversely, the VOLATILE pattern exhibits massive leaps, mimicking real altcoin behavior (high risk/high potential reward). This demonstrates how adjusting mathematical parameters (Amplitude and Noise) directly simulates financial risk. 
</div>""", unsafe_allow_html=True)
        else:
            st.plotly_chart(
                chart_sim(x1, y1,
                    f"{pattern}  |  A = {amplitude:.0f}  ·  f = {frequency:.1f}  ·  drift = {drift:+.0f}",
                    CLR["sky"]), use_container_width=True)
            st.markdown("""
<div class="ib">
💡 <b>Insightful Explanation (Mathematical Modifiers):</b> This chart dynamically translates math into market behavior.
<br>• <b>Amplitude (A)</b> dictates the severity of price swings (Volatility).
<br>• <b>Frequency (f)</b> dictates how rapidly those swings occur (Trading Speed).
<br>• <b>Drift</b> dictates the overarching macro trend—a positive drift forces the entire wave upwards, simulating a long-term Bull Market, regardless of the short-term noise.
</div>""", unsafe_allow_html=True)

    # ── TAB 2: REAL DATASET ───────────────────────────────────────────────────
    with tab2:
        df = ss.get("df")
        if df is None or (isinstance(df,pd.DataFrame) and df.empty):
            st.markdown("""
<div style="background:#080F1C;border:1px dashed #1E3A5F;border-radius:14px;
            padding:40px 20px;text-align:center;margin:16px 0">
  <div style="font-size:44px;margin-bottom:14px">₿</div>
  <div style="font-size:15px;font-weight:700;color:#E2E8F0;margin-bottom:8px">No Dataset Loaded</div>
  <div style="font-size:12px;color:#475569;max-width:440px;margin:0 auto;line-height:1.9">
    Choose a data source in the sidebar:<br>
    <b style="color:#38BDF8">▶️ Preloaded Data</b> — instant mathematical simulation<br>
    <b style="color:#38BDF8">📁 Upload CSV</b> — use your own OHLCV dataset
  </div>
</div>""", unsafe_allow_html=True)
            st.markdown("#### Expected CSV Format")
            st.dataframe(pd.DataFrame({
                "Timestamp":[1325412060,1325412120,1325412180],
                "Open":[4.58,4.58,4.58],"High":[4.58,4.59,4.60],
                "Low":[4.57,4.57,4.56],"Close":[4.58,4.58,4.59],"Volume":[0.1,0.2,0.3]}),
                use_container_width=True)
            st.caption("Timestamps = Unix seconds  ·  Prices in USD  ·  Volume in BTC")
        else:
            sub = filter_period(df, period)
            mrow([
                ("Dataset Rows",  f"{len(df):,}",                          f"Source: {ss['df_source']}"),
                ("Period Rows",   f"{len(sub):,}",                         period),
                ("From",          sub["Date"].min().strftime("%Y-%m-%d"), "Start Date"),
                ("To",            sub["Date"].max().strftime("%Y-%m-%d"), "End Date"),
                ("Avg Volatility",(f"${sub['Volatility'].mean():,.4f}"
                                   if "Volatility" in sub.columns else "N/A"), "Avg High−Low"),
            ])
            st.markdown("<br>", unsafe_allow_html=True)

            # FA-2 Stage 5: All 4 required charts + Explanations
            
            # Chart 1: Close Line
            st.plotly_chart(chart_close(sub), use_container_width=True)
            st.markdown("""<div class="ib">💡 <b>Insightful Explanation (Market Trend):</b> The Close Price line chart exposes the macro momentum of the asset over time. Sharp, sustained upward slopes indicate strong buying pressure (bullish sentiment), while extended flat areas indicate market consolidation and indecision.</div>""", unsafe_allow_html=True)

            # Chart 2 & 3: High/Low Spread & Volume Bar
            c1,c2 = st.columns(2)
            with c1: 
                st.plotly_chart(chart_hl(sub), use_container_width=True)
                st.markdown("""<div class="wb">💡 <b>Insightful Explanation (Volatility Spread):</b> This filled-area chart tracks intra-period risk. The wider the shaded red band, the larger the gap between the Highest and Lowest trades. Wide bands signal massive market friction and elevated financial risk.</div>""", unsafe_allow_html=True)
            with c2: 
                st.plotly_chart(chart_volume(sub), use_container_width=True)
                st.markdown("""<div class="gb">💡 <b>Insightful Explanation (Trading Volume):</b> Volume is the fuel of price movement. Massive purple spikes indicate a surge in trades, which often correlates with major market events, confirming breakouts or signaling panic sell-offs.</div>""", unsafe_allow_html=True)

            # Chart 4: Volatile Periods Overlay
            st.plotly_chart(chart_vol_periods(sub), use_container_width=True)
            st.markdown("""
<div class="rb">
💡 <b>Insightful Explanation (Market Shocks):</b> The red dots identify the top 25% most volatile intervals in your selected timeframe. When these dots cluster together heavily, it clearly identifies "Market Shocks" — periods where major news, whale orders, or heavy liquidation fundamentally disrupted the normal pricing rhythm.
</div>""", unsafe_allow_html=True)

            with st.expander("📄 Preview last 100 rows"):
                st.dataframe(sub.tail(100), use_container_width=True)

    # ── TAB 3: DATA SUMMARY ───────────────────────────────────────────────────
    with tab3:
        st.markdown("#### 📋 Data Preparation Report")
        df = ss.get("df")
        if df is None or (isinstance(df,pd.DataFrame) and df.empty):
            st.markdown('<div class="wb">⚠ Load a dataset first (sidebar → Real Dataset).</div>',
                        unsafe_allow_html=True)
        else:
            # FA-2 Stage 4 evidence — full data exploration
            c1,c2 = st.columns(2)
            with c1:
                st.markdown("**Dataset Shape**")
                st.info(f"Rows: {len(df):,}  |  Columns: {len(df.columns)}")
                st.markdown("**Column Names**")
                st.code(", ".join(df.columns.tolist()))
                st.markdown("**Date Range**")
                st.info(f"{df['Date'].min().strftime('%Y-%m-%d %H:%M')} → "
                        f"{df['Date'].max().strftime('%Y-%m-%d %H:%M')}")
            with c2:
                st.markdown("**Missing Values**")
                mv = df.isnull().sum()
                if mv.sum() == 0:
                    st.markdown('<div class="gb">✅ No missing values found.</div>',
                                unsafe_allow_html=True)
                else:
                    st.dataframe(mv[mv>0].rename("Missing Count"), use_container_width=True)
                st.markdown("**Volatility = High − Low**")
                if "Volatility" in df.columns:
                    v = df["Volatility"]
                    st.info(f"Min: {v.min():.6f} | Max: {v.max():.4f} | Mean: {v.mean():.4f}")

            st.markdown("---")
            st.markdown("**Statistical Summary (OHLCV)**")
            cols = [c for c in ["Open","High","Low","Close","Volume","Volatility"]
                    if c in df.columns]
            st.dataframe(df[cols].describe().round(4), use_container_width=True)

            st.markdown("---")
            st.markdown("**First 10 Rows (after cleaning)**")
            st.dataframe(df.head(10), use_container_width=True)

            st.markdown("""
<div class="ib">
📌 <b>Stage 4 Complete:</b> Dataset loaded ✅ · Timestamps converted ✅ ·
Column names standardised ✅ · Missing values filled with median ✅ ·
Volatility = High − Low computed ✅ · Subset available for clarity ✅
</div>""", unsafe_allow_html=True)

    # ── TAB 4: FEEDBACK WALL ──────────────────────────────────────────────────
    with tab4:
        if st.button("✍️ Write Feedback", type="primary", key="tab_fb_btn"):
            ss["page"]="feedback"; st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)
        fbs = ss.get("feedbacks",[])
        if not fbs:
            st.markdown("""
<div style="text-align:center;padding:60px 20px">
  <div style="font-size:40px;margin-bottom:12px">💬</div>
  <div style="color:#334155;font-size:13px">No feedback yet — be the first!</div>
</div>""", unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="font-size:11px;color:#334155;margin-bottom:14px">'
                        f'{len(fbs)} submission{"s" if len(fbs)!=1 else ""}</div>',
                        unsafe_allow_html=True)
            for fb in reversed(fbs):
                stars = "★"*fb["rating"] + "☆"*(5-fb["rating"])
                demo_tag = ' <span class="demo-badge">DEMO</span>' if fb.get("demo") else ""
                st.markdown(
                    f'<div class="fb-card">'
                    f'<div style="display:flex;justify-content:space-between;align-items:flex-start">'
                    f'<div><span class="fb-name">{fb["name"]}</span>{demo_tag}'
                    f' <span class="fb-meta">· {fb["role"]} · {fb["school"]}</span></div>'
                    f'<span class="fb-stars">{stars}</span></div>'
                    f'<div class="fb-badge">{fb["category"]}</div>'
                    f'<div class="fb-body">{fb["message"]}</div>'
                    f'<div class="fb-time">🕐 {fb["ts"]}</div></div>',
                    unsafe_allow_html=True)

    # ── TAB 5: MATH CONCEPTS ─────────────────────────────────────────────────
    with tab5:
        c1,c2,c3 = st.columns(3)
        with c1:
            st.markdown("#### 〰️ Sine Wave")
            st.markdown('<div class="mono">y = A·sin(f·x) + drift·x</div>', unsafe_allow_html=True)
            st.markdown("""
| Parameter | Market Meaning |
|-----------|----------------|
| A (Amplitude) | Swing size = volatility |
| f (Frequency) | Speed of market cycles |
| drift > 0 | Bull market (upward trend) |
| drift < 0 | Bear market (downward) |

Models **predictable** market cycles like bull/bear phases. Used for assets with seasonal patterns.
""")
        with c2:
            st.markdown("#### 〜 Cosine Wave")
            st.markdown('<div class="mono">y = A·cos(f·x) + drift·x</div>', unsafe_allow_html=True)
            st.markdown("""
| Behaviour | Meaning |
|-----------|---------|
| Starts at +A | Market opens at peak |
| Periodic dips | Regular correction cycles |
| ± drift | Long-term direction |

Like sine but **phase-shifted** — starts at maximum. Represents different market entry scenarios.
""")
        with c3:
            st.markdown("#### ⚡ Random Noise")
            st.markdown('<div class="mono">y = N(0, A) + drift·x</div>', unsafe_allow_html=True)
            st.markdown("""
**Stochastic** market shocks:
- Breaking news / regulations
- Whale buy/sell orders
- Market panic or FOMO events
- Exchange outages

Most closely mirrors **real BTC** price behaviour. Unpredictable and event-driven.
""")

        st.divider()
        c1,c2 = st.columns(2)
        with c1:
            st.markdown("#### 📐 Formula Reference")
            st.markdown("""
| Concept | Formula | Domain |
|---------|---------|--------|
| 1-min Volatility | `High − Low` | Statistics |
| Sine price cycle | `A·sin(f·x)+drift·x` | Trigonometry |
| Cosine price cycle | `A·cos(f·x)+drift·x` | Trigonometry |
| Market shock | `N(0,A)+drift·x` | Stochastic |
| Bull market | `drift > 0` | Calculus |
| Bear market | `drift < 0` | Calculus |
| Volatility index σ | `√(Σ(x−μ)²/n)` | Statistics |
| Price Range | `High − Low` | Statistics |
""")
        with c2:
            st.markdown("#### ❓ Critical Thinking Questions")
            st.markdown("""
1. **Amplitude ↑** → larger swings → higher σ (volatility index)
2. **Frequency ↑** → more oscillations → intense short-term trading activity
3. **Positive drift** = long-term bull market (integral of positive slope)
4. **Random Noise ≈ real BTC** → both are unpredictable and event-driven
5. **High−Low small** = stablecoin; **large** = volatile altcoin
6. **Volume spike + price spike** = stronger trend confirmation
7. **1-min data** captures micro-volatility invisible in daily charts
8. Why does higher amplitude always increase the **standard deviation**?
9. Can a market show **high volatility but still trend upward**? (High A + positive drift)
10. What makes **Sine vs Random Noise** fundamentally different models?
""")

        st.divider()
        st.markdown("#### 🔗 Mathematical Models → Market Behaviour")
        st.markdown("""
| Dashboard Control | Math Function | Market Insight |
|-------------------|---------------|----------------|
| Pattern: Sine | y = A·sin(f·x) | Cyclical bull/bear markets |
| Pattern: Cosine | y = A·cos(f·x) | Cycle starting at market peak |
| Pattern: Random Noise | y = N(0,A) | Sudden news-driven shocks |
| Amplitude slider ↑ | A increases | More volatile / risky asset |
| Frequency slider ↑ | f increases | Faster trading cycles |
| Drift slider > 0 | +drift·x | Long-term upward trend |
| Drift slider < 0 | −drift·x | Long-term downward trend |
| Comparison mode ON | Two functions side-by-side | Stable vs volatile comparison |
| Volatility chart | High − Low per row | Real market risk measurement |
""")


# ══════════════════════════════════════════════════════════════════════════════
#  ROUTER
# ══════════════════════════════════════════════════════════════════════════════
def main():
    page = ss.get("page","onboard")
    if   page == "onboard":  page_onboard()
    elif page == "auth":     page_auth()
    elif page == "edit":     page_edit()
    elif page == "feedback": page_feedback_form()
    else:                    page_dashboard()

if __name__ == "__main__":
    main()