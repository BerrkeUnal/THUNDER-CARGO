import streamlit as st
import time
from views import guest, admin, customer

# CONFIGURATION 
st.set_page_config(page_title="Thunder Cargo", layout="wide", page_icon="⚡")

# SESSION STATE MANAGEMENT 
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = 'guest' 
if 'username' not in st.session_state:
    st.session_state['username'] = ''

# AUTHENTICATION FUNCTIONS 
def login_process(username, password):
    if username == "admin" and password == "admin123":
        st.session_state['user_role'] = 'admin'
        st.session_state['username'] = 'Administrator'
        st.success("Login Successful! Redirecting...")
        time.sleep(0.5)
        st.rerun()
    elif username == "client" and password == "1234":
        st.session_state['user_role'] = 'customer'
        st.session_state['username'] = 'Ahmet Yilmaz' 
        st.success("Login Successful! Redirecting...")
        time.sleep(0.5)
        st.rerun()
    else:
        st.error("Invalid Username or Password")

def logout_process():
    st.session_state['user_role'] = 'guest'
    st.session_state['username'] = ''
    st.rerun()

# --- GUEST NAVIGATION ---
if st.session_state['user_role'] == 'guest':
    
    # Ekranı dikeyde biraz ortalamak için boşluk bırakalım
    st.write("") 
    st.write("")

    # Ekranı 3 sütuna bölüyoruz: [Boşluk] [Giriş Formu] [Boşluk]
    # Ortadaki sütun (col2) daha geniş olacak.
    col1, col2, col3 = st.columns([1, 3, 1])

    with col2:
        # Bir kutu (container) içine alarak çerçeveli görünüm veriyoruz
        with st.container(border=True):
            col_img1, col_img2, col_img3 = st.columns([1,1,1])
            with col_img2:
                st.image("thunderimage.png", width=200)
            
            st.markdown("<h1 style='text-align: center;' >Thunder Cargo ⚡</h1>", unsafe_allow_html=True)
            st.write("<h4 style='text-align: center;' >Reach Light Speed with Thunder Cargo</h4>", unsafe_allow_html=True)
            
            # Form yapısı: Enter tuşuna basınca giriş yapmayı sağlar
            with st.form("login_form"):
                user_input = st.text_input("Username", placeholder="Enter your username")
                pass_input = st.text_input("Password", type="password", placeholder="Enter your password")
                
                # Giriş Butonu (Tam genişlikte olması için use_container_width=True)
                submitted = st.form_submit_button("Sign In", use_container_width=True, type="primary")
                
                if submitted:
                    login_process(user_input, pass_input)

            # Demo hesap bilgileri
            st.info("Demo Accounts:\n\n👤 **Admin:** admin / admin123\n👤 **Customer:** client / 1234")
            about_thunder = st.radio("Informations",["About Us","Branches","Where is My Cargo?"])
            if about_thunder == "About Us":
                guest.show_about()
            elif about_thunder == "Branches":
                guest.show_branch_locator()
            elif about_thunder == "Where is My Cargo?":    
                guest.show_public_tracking()




# --- ADMIN NAVIGATION ---
elif st.session_state['user_role'] == 'admin':
    st.sidebar.success(f"User: **{st.session_state['username']}**")
    st.sidebar.subheader("Admin Panel")
    page_selection = st.sidebar.radio("Operations", 
        ["📊 Dashboard", "📦 Cargo Tracking", "📋 All Shipments", "➕ New Registration","👥 Employee Management","🔧 Admin"])
    
    st.sidebar.divider()
    if st.sidebar.button("Logout"):
        logout_process()

    # Yönlendirme
    if page_selection == "📊 Dashboard":
        admin.show_dashboard()
    elif page_selection == "📦 Cargo Tracking":
        admin.show_tracking()
    elif page_selection == "📋 All Shipments":
        admin.show_all_shipments()
    elif page_selection == "➕ New Registration":
        admin.show_new_registration()
    elif page_selection == "👥 Employee Management":
        admin.show_employee_management()
    elif page_selection == "🔧 Admin":
        admin.show_admin_tools()



# --- CUSTOMER NAVIGATION ---
elif st.session_state['user_role'] == 'customer':
    st.sidebar.info(f"Welcome, **{st.session_state['username']}**")
    st.sidebar.subheader("Customer Portal")
    
    # Menü seçeneklerini genişlettik
    page_selection = st.sidebar.radio("My Account", 
        ["📊 Dashboard", "📦 My Shipments", "📥 Incoming Deliveries", "🧾 Invoices"])
    
    st.sidebar.divider()
    if st.sidebar.button("Logout"):
        logout_process()

    # Yönlendirmeler
    if page_selection == "📊 Dashboard":
        customer.show_dashboard()
    elif page_selection == "📦 My Shipments":
        customer.show_my_shipments()
    elif page_selection == "📥 Incoming Deliveries":
        customer.show_incoming()
    elif page_selection == "🧾 Invoices":
        customer.show_invoices()
    elif page_selection == "🚚 Request Courier":
        customer.show_courier_request()