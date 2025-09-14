import os
import streamlit as st
from supabase import create_client

# -------------------- CONFIG --------------------
st.set_page_config(
    page_title="Nome Applicazione",
    page_icon="💼",
    layout="wide",
)

# -------------------- SUPABASE --------------------
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")
supabase = None
if SUPABASE_URL and SUPABASE_ANON_KEY:
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
    st.experimental_set_query_params(page=page_key)
    st.rerun()

# URL → session state
query = st.experimental_get_query_params()
page = query.get("page", [None])[0] or st.session_state.get("page", "home")
if page not in PAGES:
    page = "home"
st.session_state["page"] = page

# -------------------- STILI --------------------
CSS = """
<style>
.main .block-container {max-width: 1100px;}
/* Colonna di sinistra a card */
.left-card {
    background: #f6f8fb;
    border: 1px solid #e5e7eb;
    border-radius: 22px;
    padding: 14px 14px 18px 14px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
}
.menu-title { text-align:center; font-weight:700; margin: 4px 0 12px 0; }
.stButton>button {
    padding: 0.85rem 2.6rem;
    border-radius: 16px;
    font-weight: 700;
    font-size: 1.05rem;
    border: 0;
}
.subtitle {
    margin-top: -6px; color: #6b7280;
    letter-spacing: 0.12em; font-size: 0.95rem;
    text-transform: uppercase; text-align:center;
}
.footer-note { color:#6b7280; text-align:center; margin-top:20px; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# -------------------- LAYOUT A COLONNE --------------------
left, right = st.columns([0.32, 0.68], gap="large")

# ---- MENU a tendina “esterno” (senza HTML form) ----
with left:
    st.markdown("<div class='left-card'>", unsafe_allow_html=True)
    st.markdown("<div class='menu-title'>MENU</div>", unsafe_allow_html=True)

    if st.button("INFO / SCOPRI DI PIÙ", use_container_width=True, key="m_info"):
        go("info")
    if st.button("VOCE 2", use_container_width=True, key="m_v2"):
        go("voce2")
    if st.button("VOCE 3", use_container_width=True, key="m_v3"):
        go("voce3")
    if st.button("VOCE 4", use_container_width=True, key="m_v4"):
        go("voce4")

    st.markdown("</div>", unsafe_allow_html=True)

# ---- CONTENUTO PAGINE ----
def page_home():
    with right:
        st.markdown("<h1 style='text-align:center; margin-bottom:0'>NOME APPLICAZIONE</h1>", unsafe_allow_html=True)
        st.markdown("<p class='subtitle'>SOTTOTITOLO</p>", unsafe_allow_html=True)

        IMG_URL = "https://images.unsplash.com/photo-1554224155-3a589877462f?q=80&w=1200&auto=format&fit=crop"
        st.markdown("<div style='display:flex; justify-content:center; margin:18px 0 12px 0;'>", unsafe_allow_html=True)
        st.image(IMG_URL, caption=None, use_column_width=False, width=520)
        st.markdown("</div>", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            if st.button("ACCEDI", use_container_width=True, key="b_login"):
                go("login")
        with c2:
            if st.button("REGISTRATI", use_container_width=True, key="b_signup"):
                go("signup")

        st.markdown("<p class='footer-note'>Descrizione Minima funzioni Applicazione</p>", unsafe_allow_html=True)

def page_login():
    with right:
        st.title("Accedi")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if not supabase:
                st.error("Configura SUPABASE_URL e SUPABASE_ANON_KEY nei Secrets.")
            else:
                try:
                    supabase.auth.sign_in_with_password({"email": email, "password": password})
                    st.success("Login effettuato!")
                except Exception as e:
                    st.error(f"Errore login: {e}")

def page_signup():
    with right:
        st.title("Registrati")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Crea account"):
            if not supabase:
                st.error("Configura SUPABASE_URL e SUPABASE_ANON_KEY nei Secrets.")
            else:
                try:
                    supabase.auth.sign_up({"email": email, "password": password})
                    st.success("Registrazione completata! Controlla la mail.")
                except Exception as e:
                    st.error(f"Errore registrazione: {e}")

def page_simple(title: str):
    with right:
        st.title(title)
        st.info(f"Sei nella pagina: {title}")

# Router
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