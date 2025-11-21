import streamlit as st
import pandas as pd
from database import run_query, generate_id
from datetime import datetime
import time



# --- YARDIMCI FONKSİYONLAR ---

def get_current_cust_id():
    """
    Gerçek senaryoda login olan kullanıcının ID'si session'dan gelir.
    Demo için 'CU001' (Ahmet Yılmaz) kullanıyoruz.
    """
    # Eğer login sisteminde ID'yi session'a attıysan: return st.session_state.get('user_id')
    return 'CU001' 

# --- SAYFA FONKSİYONLARI ---

def show_dashboard():
    cust_id = get_current_cust_id()
    
    # Müşteri Adını Çek
    user_res = run_query("SELECT FirstName, LastName FROM Customers WHERE CustID = %s", (cust_id,))
    full_name = f"{user_res[0]['FirstName']} {user_res[0]['LastName']}" if user_res else "Customer"
    
    st.title(f"👋 Welcome, {full_name}")
    st.markdown("Here is the summary of your logistics operations.")
    
    # İstatistikler
    col1, col2, col3 = st.columns(3)
    
    # 1. Gönderdiklerim (Outgoing)
    out_count = run_query("SELECT COUNT(*) as cnt FROM Cargos WHERE SenderCustID = %s", (cust_id,))[0]['cnt']
    col1.metric("📦 Outgoing Shipments", out_count, delta_color="normal")
    
    # 2. Bana Gelenler (Incoming)
    in_count = run_query("SELECT COUNT(*) as cnt FROM Cargos WHERE ReceiverCustID = %s", (cust_id,))[0]['cnt']
    col2.metric("📥 Incoming Deliveries", in_count, delta="Active")
    
    # 3. Toplam Harcama
    inv_sum = run_query("SELECT SUM(TotalAmount) as total FROM Invoice WHERE CustID = %s", (cust_id,))[0]['total']
    total_spent = float(inv_sum) if inv_sum else 0.0
    col3.metric("💰 Total Spend", f"₺{total_spent:,.2f}")

    st.divider()
    
    # Son Hareketler Tablosu
    st.subheader("🕒 Recent Activity")
    sql = """
    SELECT c.CargoID, c.CurrentStatus, c.LastUpdated, 'Outgoing' as Type
    FROM Cargos c WHERE c.SenderCustID = %s
    UNION
    SELECT c.CargoID, c.CurrentStatus, c.LastUpdated, 'Incoming' as Type
    FROM Cargos c WHERE c.ReceiverCustID = %s
    ORDER BY LastUpdated DESC LIMIT 5
    """
    recent_activity = run_query(sql, (cust_id, cust_id))
    if recent_activity:
        st.dataframe(pd.DataFrame(recent_activity), use_container_width=True, hide_index=True)
    else:
        st.info("No recent activity found.")


def show_my_shipments():
    cust_id = get_current_cust_id()
    st.title("📦 My Outgoing Shipments")
    st.info("Packages you have sent to others.")
    
    sql = """
    SELECT c.CargoID, r.FirstName as ReceiverName, r.City as Destination, 
           c.CurrentStatus, c.ShippingCost, st.ServiceType, c.LastUpdated
    FROM Cargos c
    JOIN Customers r ON c.ReceiverCustID = r.CustID
    JOIN ServiceTypes st ON c.ServiceTypeID = st.ServiceTypeID
    WHERE c.SenderCustID = %s
    ORDER BY c.LastUpdated DESC
    """
    df = pd.DataFrame(run_query(sql, (cust_id,)))
    
    if not df.empty:
        # Filtreleme Seçenekleri
        status_filter = st.multiselect("Filter by Status", df['CurrentStatus'].unique())
        if status_filter:
            df = df[df['CurrentStatus'].isin(status_filter)]
            
        st.dataframe(
            df, 
            column_config={
                "ShippingCost": st.column_config.NumberColumn("Cost", format="₺%.2f"),
                "LastUpdated": st.column_config.DatetimeColumn("Last Update", format="DD.MM.YYYY HH:mm"),
            },
            use_container_width=True, hide_index=True
        )
        
        # Şikayet / Destek Butonu
        st.write("---")
        selected_cargo = st.selectbox("Select Cargo to Report Issue", df['CargoID'])
        if st.button(f"Report Issue for {selected_cargo}"):
            st.success(f"Ticket created for Cargo {selected_cargo}. Support team will contact you.")
            # Buraya gerçek bir 'SupportTickets' tablosuna insert eklenebilir.
    else:
        st.warning("You haven't sent any packages yet.")


def show_incoming():
    cust_id = get_current_cust_id()
    st.title("📥 Incoming Deliveries")
    st.info("Packages coming to you.")
    
    sql = """
    SELECT c.CargoID, s.FirstName as SenderName, s.City as Origin, 
           c.CurrentStatus, st.ServiceType
    FROM Cargos c
    JOIN Customers s ON c.SenderCustID = s.CustID
    JOIN ServiceTypes st ON c.ServiceTypeID = st.ServiceTypeID
    WHERE c.ReceiverCustID = %s AND c.CurrentStatus NOT IN ('Delivered', 'Returned')
    """
    incoming_data = run_query(sql, (cust_id,))
    
    if incoming_data:
        for cargo in incoming_data:
            with st.container(border=True):
                c1, c2, c3 = st.columns([2,2,1])
                c1.markdown(f"### 📦 {cargo['CargoID']}")
                c1.caption(f"From: {cargo['SenderName']} ({cargo['Origin']})")
                
                c2.markdown(f"**Status:** {cargo['CurrentStatus']}")
                c2.markdown(f"**Type:** {cargo['ServiceType']}")
                
                # Aksiyon Butonları
                c3.write("Actions:")
                if c3.button("🏠 I'm Not Home", key=f"home_{cargo['CargoID']}"):
                    # Veritabanına 'Müşteri Talebi' olarak log düşebiliriz
                    # Şimdilik simülasyon:
                    st.toast(f"Driver notified for {cargo['CargoID']}: 'Leave at neighbor/branch'")
                    
                if c3.button("📍 Track Live", key=f"track_{cargo['CargoID']}"):
                    st.session_state['tracking_search'] = cargo['CargoID']
                    st.info("Go to 'Guest > Track Cargo' to see details.")
    else:
        st.success("No active incoming deliveries. You are all caught up!")


def show_invoices():
    cust_id = get_current_cust_id()
    st.title("🧾 Invoices & Payments")
    
    sql = """
    SELECT i.InvoiceID, i.CargoID, i.InvoiceDate, i.TotalAmount, c.PaymentStatus
    FROM Invoice i
    JOIN Cargos c ON i.CargoID = c.CargoID
    WHERE i.CustID = %s
    ORDER BY i.InvoiceDate DESC
    """
    invoices = run_query(sql, (cust_id,))
    df = pd.DataFrame(invoices)
    
    if not df.empty:
        # Ödeme Durumu Renklendirme
        st.dataframe(
            df,
            column_config={
                "TotalAmount": st.column_config.NumberColumn("Amount", format="₺%.2f"),
                "InvoiceDate": st.column_config.DateColumn("Date"),
                "PaymentStatus": st.column_config.TextColumn("Status"),
            },
            use_container_width=True, hide_index=True
        )
        
        col1, col2 = st.columns(2)       

        with col2:
            # Online Ödeme Simülasyonu
            unpaid = df[df['PaymentStatus'] == 'Pending']
            if not unpaid.empty:
                pay_inv_id = st.selectbox("Select Invoice to Pay", unpaid['InvoiceID'])
                if st.button("💳 Pay Online Now"):
                    with st.spinner("Processing Payment..."):
                        time.sleep(1.5)
                        # Ödemeyi güncelle
                        cargo_id_to_pay = unpaid[unpaid['InvoiceID'] == pay_inv_id].iloc[0]['CargoID']
                        run_query("UPDATE Cargos SET PaymentStatus = 'Paid' WHERE CargoID = %s", (cargo_id_to_pay,))
                        st.success("Payment Successful! Status updated.")
                        st.rerun()
            else:
                st.success("All invoices are paid.")

    else:
        st.info("No invoices found.")
