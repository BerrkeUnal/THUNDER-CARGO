import streamlit as st
import pandas as pd
import random
from database import run_query

def show_about():
    st.title("About Thunder Cargo")
    st.markdown("Established in 2025 by Berke Ünal, Thunder Cargo was born from a vision to redefine modern logistics. We combine cutting-edge technology with a robust global network to ensure your shipments are delivered with lightning speed and precision. Whether it's local distribution or international transit, our mission is simple: to bridge distances reliably and efficiently.")

def mask_name(full_name):
    """İsimleri KVKK gereği yıldızlar: Ahmet Yılmaz -> A**** Y*****"""
    if not full_name or str(full_name) == 'nan': return "******"
    parts = full_name.split()
    masked_parts = [p[0] + "*" * (len(p)-1) if len(p) > 1 else p for p in parts]
    return " ".join(masked_parts)

def init_captcha():
    """Session state'te basit bir matematik sorusu oluşturur."""
    if 'captcha_num1' not in st.session_state:
        st.session_state['captcha_num1'] = random.randint(1, 10)
        st.session_state['captcha_num2'] = random.randint(1, 10)

#  1. ŞUBE BULUCU (BRANCH LOCATOR)

def show_branch_locator():
    st.title("📍 Find a Branch")
    st.write("Locate the nearest Thunder Cargo branch for shipping and pickup.")
    
    # 1. Adım: Şehir Seçimi
    cities_res = run_query("SELECT DISTINCT BranchCity FROM CargoBranches ORDER BY BranchCity")
    cities = [row['BranchCity'] for row in cities_res] if cities_res else []
    
    selected_city = st.selectbox("Select City", ["Choose..."] + cities)
    
    if selected_city != "Choose...":
        # 2. Adım: İlçeleri Çek
        districts_res = run_query("SELECT DISTINCT BranchDistrict FROM CargoBranches WHERE BranchCity = %s ORDER BY BranchDistrict", (selected_city,))
        districts = [row['BranchDistrict'] for row in districts_res] if districts_res else []
        
        selected_district = st.selectbox("Select District", ["All Districts"] + districts)
        
        # 3. Adım: Şubeleri Listele
        query = "SELECT * FROM CargoBranches WHERE BranchCity = %s"
        params = [selected_city]
        
        if selected_district != "All Districts":
            query += " AND BranchDistrict = %s"
            params.append(selected_district)
            
        branches = run_query(query, tuple(params))
        
        st.divider()
        st.subheader(f"Branches in {selected_city}")
        
        if branches:
            # Şubeleri Kartlar Halinde Göster
            for b in branches:
                with st.container(border=True):
                    c1, c2 = st.columns([3, 1])
                    with c1:
                        st.markdown(f"### 🏢 {b['BranchName']}")
                        st.markdown(f"**📍 Address:** {b['BranchAddress']}")
                        st.markdown(f"**🏙️ District:** {b['BranchDistrict']} / {b['BranchCity']}")
                    with c2:
                        st.markdown(f"**📞 Phone:**\n`{b['BranchNumber']}`")
                        st.markdown(f"**📧 Email:**\n{b['BranchEmail']}")
                        st.button(f"Show on Map", key=b['BranchID'], disabled=True, help="Map integration requires Lat/Long data.")
        else:
            st.warning("No branches found in this location.")

# 2. DETAYLI KARGO TAKİP 

def show_public_tracking():
    st.title("🔎 Track Your Shipment")
    st.write("Enter your tracking number to see the live status of your cargo.")
    
    # Captcha Başlat
    init_captcha()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        tracking_no = st.text_input("Tracking Number (Cargo ID)", placeholder="Ex: CG001", max_chars=5)
    
    with col2:
        # Güvenlik Kodu (Captcha)
        n1 = st.session_state['captcha_num1']
        n2 = st.session_state['captcha_num2']
        captcha_ans = st.text_input(f"Security Check: {n1} + {n2} = ?", placeholder="Result", max_chars=2)

    search_btn = st.button("Track Cargo", type="primary", use_container_width=True)

    if search_btn:
        # 1. Captcha Kontrolü
        if not captcha_ans.isdigit() or int(captcha_ans) != (n1 + n2):
            st.error("❌ Security check failed. Please calculate correctly.")
            # Soruyu yenile
            st.session_state['captcha_num1'] = random.randint(1, 10)
            st.session_state['captcha_num2'] = random.randint(1, 10)
            return

        if tracking_no:
            # 2. Kargo Bilgilerini Çek
            cargo_sql = """
            SELECT c.CargoID, c.CurrentStatus, c.LastUpdated,
                   s.FirstName as SenderName, s.LastName as SenderLast,
                   r.FirstName as ReceiverName, r.LastName as ReceiverLast,
                   ob.BranchCity as Origin, db.BranchCity as Dest
            FROM Cargos c
            JOIN Customers s ON c.SenderCustID = s.CustID
            JOIN Customers r ON c.ReceiverCustID = r.CustID
            JOIN CargoBranches ob ON c.OriginBranchID = ob.BranchID
            JOIN CargoBranches db ON c.DestBranchID = db.BranchID
            WHERE c.CargoID = %s
            """
            cargo_res = run_query(cargo_sql, (tracking_no,))
            
            if cargo_res:
                cargo = cargo_res[0]
                
                # Üst Bilgi Kartı
                st.success(f"✅ Shipment Found: {tracking_no}")
                
                with st.container(border=True):
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Current Status", cargo['CurrentStatus'])
                    c2.metric("Origin", cargo['Origin'])
                    c3.metric("Destination", cargo['Dest'])
                    # İsimleri Maskele (Ahmet Yılmaz -> A**** Y*****)
                    masked_sender = mask_name(f"{cargo['SenderName']} {cargo['SenderLast']}")
                    masked_receiver = mask_name(f"{cargo['ReceiverName']} {cargo['ReceiverLast']}")
                    c4.metric("Receiver", masked_receiver)

                # 3. Hareket Geçmişi 
                log_sql = """
                SELECT t.LogTimestamps, st.StatusDescription, b.BranchName, b.BranchCity
                FROM TrackingLog t
                JOIN CargoStatusType st ON t.StatusID = st.StatusID
                JOIN CargoBranches b ON t.BranchID = b.BranchID
                WHERE t.CargoID = %s
                ORDER BY t.LogTimestamps DESC
                """
                logs = run_query(log_sql, (tracking_no,))
                
                st.subheader("📅 Shipment Journey")
                
                if logs:
                    # TIMELINE GÖRSELLEŞTİRME
                    for i, log in enumerate(logs):
                        # Tarih formatı
                        ts = log['LogTimestamps']
                        date_str = ts.strftime("%d.%m.%Y")
                        time_str = ts.strftime("%H:%M")
                        
                        # Son işlem ise yeşil, değilse gri ikon
                        icon = "🟢" if i == 0 else "⬇️"
                        if "Delivered" in log['StatusDescription']: icon = "🏁"
                        
                        # Satır Düzeni
                        with st.container():
                            tc1, tc2, tc3 = st.columns([1, 1, 6])
                            with tc1:
                                st.caption(f"{date_str}\n{time_str}")
                            with tc2:
                                st.markdown(f"<h3 style='text-align: center;'>{icon}</h3>", unsafe_allow_html=True)
                            with tc3:
                                st.markdown(f"**{log['StatusDescription']}**")
                                st.write(f"📍 {log['BranchName']} ({log['BranchCity']})")
                            st.divider()
                else:
                    st.info("No movement history available yet.")
                    
            else:
                st.warning("⚠️ No shipment found with this Tracking Number.")
        else:
            st.warning("⚠️ Please enter a Tracking Number.")
    