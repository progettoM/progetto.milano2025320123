import os
from urllib.parse import urlencode
import streamlit as st
from supabase import create_client

# -------------------- CONFIG --------------------
st.set_page_config(
    page_title="Nome Applicazione",
    page_icon="💼",
    layout="wide",
)

# -------------------- SUPABASE --------------------
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# -------------------- ROUTING --------------------
PAGES = {
    "home": "Home",
    "login": "Accedi",
    "signup": "Registrati",
    "info": "Info / Scopri di più",
    "voce2": "Voce 2",
    "voce3": "Voce 3",
    "voce4": "Voce 4",
}

def go(page_key: str):
    if page_key not in PAGES:
        page_key = "home"
    st.session_state["page"] = page_key
    st.experimental_set_query_params(**{"page": page_key})
    st.rerun()

query_params = st.experimental_get_query_params()
page = query_params.get("page", [None])[0] or st.session_state.get("page", "home")
if page not in PAGES:
    page = "home"
    st.session_state["page"] = "home"

# -------------------- STILI --------------------
CSS = """
<style>
.main .block-container {max-width: 1100px;}
.menu-wrapper {
    position: fixed; left: 22px; top: 100px;
    width: 260px; background: #f6f8fb;
    border: 1px solid #e5e7eb; border-radius: 22px;
    padding: 16px 14px 18px 14px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.08); z-index: 100;
}
.menu-title { text-align: center; font-weight: 700; margin-bottom: 10px; }
.menu-grid {display: grid; grid-gap: 12px;}
.menu-btn {
    display: block; width: 100%;
    background: #0f4c81; color: #fff !important;
    border: none; border-radius: 16px;
    padding: 12px 14px; text-align: center;
    font-weight: 700; cursor: pointer;
}
.content { margin-left: 310px; }
.stButton>button {
    padding: 0.85rem 2.6rem; border-radius: 16px;
    font-weight: 700; font-size: 1.05rem; border: 0;
}
.subtitle {
    margin-top: -6px; color: #6b7280;
    letter-spacing: 0.12em; font-size: 0.95rem;
    text-transform: uppercase; text-align:center;
}
.footer-note { color:#6b7280; text-align:center; margin-top: 20px; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# -------------------- MENU A TENDINA --------------------
menu_html = """
<div class="menu-wrapper">
    <div class="menu-title">MENU</div>
    <div class="menu-grid">
        <form action="" method="get"><input type="hidden" name="page" value="info"/>
            <button class="menu-btn" type="submit">INFO / SCOPRI DI PIÙ</button></form>
        <form action="" method="get"><input type="hidden" name="page" value="voce2"/>
            <button class="menu-btn" type="submit">VOCE 2</button></form>
        <form action="" method="get"><input type="hidden" name="page" value="voce3"/>
            <button class="menu-btn" type="submit">VOCE 3</button></form>
        <form action="" method="get"><input type="hidden" name="page" value="voce4"/>
            <button class="menu-btn" type="submit">VOCE 4</button></form>
    </div>
</div>
"""
st.markdown(menu_html, unsafe_allow_html=True)

# -------------------- PAGINE --------------------
def page_home():
    st.markdown("<div class='content'>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center; margin-bottom:0'>NOME APPLICAZIONE</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>SOTTOTITOLO</p>", unsafe_allow_html=True)

    IMG_URL = "https://images.unsplash.com/photo-1554224155-3a589877462f?q=80&w=1200&auto=format&fit=crop"
    st.markdown("<div style='display:flex; justify-content:center; margin: 18px 0 12px 0;'>", unsafe_allow_html=True)
    st.image(IMG_URL, caption=None, use_column_width=False, width=520)
    st.markdown("</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2, vertical_alignment="center")
    with c1:
        if st.button("ACCEDI", use_container_width=True):
            go("login")
    with c2:
        if st.button("REGISTRATI", use_container_width=True):
            go("signup")

    st.markdown("<p class='footer-note'>Descrizione Minima funzioni Applicazione</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def page_login():
    st.markdown("<div class='content'>", unsafe_allow_html=True)
    st.title("Accedi")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        try:
            res = supabase.auth.sign_in_with_password({"email": email, "password": password})
            st.success("Login effettuato!")
        except Exception as e:
            st.error(f"Errore login: {e}")
    st.markdown("</div>", unsafe_allow_html=True)

def page_signup():
    st.markdown("<div class='content'>", unsafe_allow_html=True)
    st.title("Registrati")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Crea account"):
        try:
            res = supabase.auth.sign_up({"email": email, "password": password})
            st.success("Registrazione completata! Controlla la mail.")
        except Exception as e:
            st.error(f"Errore registrazione: {e}")
    st.markdown("</div>", unsafe_allow_html=True)

def page_simple(title: str):
    st.markdown("<div class='content'>", unsafe_allow_html=True)
    st.title(title)
    st.info(f"Sei nella pagina: {title}")
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------- ROUTER --------------------
if page == "home":
    page_home()
elif page == "login":
    page_login()
elif page == "signup":
    page_signup()
elif page == "info":
    page_simple("Info / Scopri di più")
elif page == "voce2":
    page_simple("Voce 2")
elif page == "voce3":
    page_simple("Voce 3")
elif page == "voce4":
    page_simple("Voce 4")
else:
    go("home")