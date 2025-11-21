import streamlit as st
import pandas as pd
import plotly.express as px
from database import run_query
from utils import get_progress_value

def show_dashboard():
    st.title("📊 Logistics Management Dashboard")
    try:
        # Verileri çek
        total_cargo_res = run_query("SELECT COUNT(*) as count FROM Cargos")
        total_rev_res = run_query("SELECT SUM(ShippingCost) as total FROM Cargos")
        active_branch_res = run_query("SELECT COUNT(*) as count FROM CargoBranches")
        
        total_cargo = total_cargo_res[0]['count'] if total_cargo_res else 0
        total_revenue = total_rev_res[0]['total'] if total_rev_res else 0
        active_branches = active_branch_res[0]['count'] if active_branch_res else 0
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Cargo", f"{total_cargo} Pcs")
        col2.metric("Total Turnover", f"₺{total_revenue:,.2f}")
        col3.metric("Active Branches", active_branches)
        
        st.divider()
        st.subheader("📍 Branch Based Cargo Density")
        branch_data = run_query("""
            SELECT b.BranchName, COUNT(c.CargoID) as CargoCount 
            FROM Cargos c
            JOIN CargoBranches b ON c.OriginBranchID = b.BranchID
            GROUP BY b.BranchName
        """)
        if branch_data:
            df_branch = pd.DataFrame(branch_data)
            fig_bar = px.bar(df_branch, x='BranchName', y='CargoCount', 
                            color='CargoCount', title="Cargo Count by Branch")
            st.plotly_chart(fig_bar, use_container_width=True)
            
    except Exception as e:
        st.error(f"Dashboard Error: {e}")

def show_tracking():
    st.title("🔎 Internal Tracking System (Detailed)")
    cargo_id_input = st.text_input("Enter Cargo ID", max_chars=5)
    
    if st.button("Search"):
        if cargo_id_input:
            query = """
            SELECT c.CargoID, c.CurrentStatus, c.CargoWeight, st.ServiceType,
                    sender.FirstName as SenderName, receiver.FirstName as ReceiverName,
                    origin.BranchCity as FromCity, dest.BranchCity as ToCity
            FROM Cargos c
            JOIN Customers sender ON c.SenderCustID = sender.CustID
            JOIN Customers receiver ON c.ReceiverCustID = receiver.CustID
            JOIN CargoBranches origin ON c.OriginBranchID = origin.BranchID
            JOIN CargoBranches dest ON c.DestBranchID = dest.BranchID
            JOIN ServiceTypes st ON c.ServiceTypeID = st.ServiceTypeID
            WHERE c.CargoID = %s
            """
            data = run_query(query, (cargo_id_input,))
            
            if data:
                cargo = data[0]
                st.subheader("Live Status")
                progress_val = get_progress_value(cargo['CurrentStatus'])
                
                if progress_val == 100:
                    st.success(f"✅ COMPLETED ({cargo['CurrentStatus']})")
                else:
                    st.info(f"🚚 IN PROGRESS: {cargo['CurrentStatus']}")
                
                st.progress(progress_val)
                st.divider()
                
                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"**Status:** {cargo['CurrentStatus']}")
                    st.write(f"**From:** {cargo['FromCity']}")
                    st.write(f"**To:** {cargo['ToCity']}")
                with col2:
                    st.write(f"**Sender:** {cargo['SenderName']}")
                    st.write(f"**Receiver:** {cargo['ReceiverName']}")
                    st.write(f"**Type:** {cargo['ServiceType']}")
            else:
                st.error("Record not found.")

def show_all_shipments():
    st.title("📋 All Active Shipments")
    try:
        data = run_query("SELECT * FROM Cargos")
        if data:
            df = pd.DataFrame(data)
            st.dataframe(
                df, 
                column_config={
                    "CurrentStatus": st.column_config.TextColumn("Durum", validate="^[a-zA-Z0-9]+$"),
                    "ShippingCost": st.column_config.NumberColumn("Fiyat", format="₺%.2f")
                },
                use_container_width=True
            )
    except Exception as e:
        st.error(f"Error: {e}")

def show_new_registration():
    st.title("➕ New Customer Registration (Demo)")
    with st.form("customer_form"):
        name = st.text_input("Name")
        surname = st.text_input("Surname")

        email = st.text_input(
            "Email",
            placeholder="username@example.com"                      
        )
        
        phone = st.text_input(
            "Phone Number", 
            max_chars=10,
            placeholder="5XX XXX XX XX", 
        )
        
        city = st.selectbox("City", ["Istanbul", "Ankara", "Izmir", "Bursa","Antalya","Trabzon","Eskisehir","Adana","Samsun","Gaziantep"])
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            st.success(f"{name} {surname} added successfully! (Simulation)")


def show_employee_management():
    st.title("👥 Employee Management")
    
    # Sayfa içi sekmeler oluşturuyoruz
    tab1, tab2, tab3 = st.tabs(["📋 Employee List", "➕ Add New Employee", "✏️ Update / Delete"])

    # --- TAB 1: LİSTELEME ---
    with tab1:
        st.subheader("All Employees")
        # Şubeleriyle beraber çalışanları çeken sorgu
        sql = """
        SELECT e.EmployeeID, e.FirstName, e.LastName, e.Position, 
               e.Salary, e.Phone, b.BranchName, e.HireDate
        FROM Employees e
        LEFT JOIN CargoBranches b ON e.BranchID = b.BranchID
        ORDER BY e.EmployeeID DESC
        """
        df = pd.DataFrame(run_query(sql))
        
        if not df.empty:
            st.dataframe(
                df,
                column_config={
                    "Salary": st.column_config.NumberColumn("Salary", format="₺%.2f"),
                    "HireDate": st.column_config.DateColumn("Getting Started", format="DD.MM.YYYY"),
                    "Phone": st.column_config.TextColumn("Phone Number")
                },
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("There are no registered personnel yet.")

    # Şube listesini veritabanından çekelim (Selectbox için lazım olacak)
    branches = run_query("SELECT BranchID, BranchName FROM CargoBranches")
    branch_options = {b['BranchName']: b['BranchID'] for b in branches} if branches else {}

    # --- TAB 2: EKLEME ---
    with tab2:
        st.subheader("New Employee Registration")
        with st.form("add_employee_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Name")
                surname = st.text_input("Surname")
                phone = st.text_input("Phone Number", max_chars=10, placeholder="5xxxxxxxxx")
            with col2:
                position = st.selectbox("Position", ["Intern", "Janitor", "Courier", "Branch Manager", "Driver","Regional Manager","Human Resources","Desk Officer"])
                salary = st.number_input("Salary (TL)", min_value=17002.0, step=500.0)
                branch_name = st.selectbox("Branch", list(branch_options.keys()) if branch_options else ["Centre"])
            
            hire_date = st.date_input("Job Start Date")
            
            submitted = st.form_submit_button("Submit", type="primary")
            
            if submitted:
                branch_id = branch_options.get(branch_name)
                insert_sql = """
                INSERT INTO Employees (FirstName, LastName, Phone, Position, Salary, BranchID, HireDate)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                run_query(insert_sql, (name, surname, phone, position, salary, branch_id, hire_date))
                st.success(f"✅ {name} {surname} Submitted.")
                st.rerun() # Listeyi yenilemek için

    # --- TAB 3: GÜNCELLEME & SİLME ---
    with tab3:
        st.subheader("Update Personnel Information")
        
        # Önce kimi güncelleyeceğimizi seçelim
        employees = run_query("SELECT EmployeeID, FirstName, LastName FROM Employees")
        if employees:
            emp_options = {f"{e['EmployeeID']} - {e['FirstName']} {e['LastName']}": e['EmployeeID'] for e in employees}
            selected_emp_str = st.selectbox("Select the Personnel to Edit", list(emp_options.keys()))
            selected_emp_id = emp_options[selected_emp_str]

            # Seçilen personelin mevcut bilgilerini çek
            current_data = run_query("SELECT * FROM Employees WHERE EmployeeID = %s", (selected_emp_id,))[0]

            with st.form("update_employee_form"):
                col1, col2 = st.columns(2)
                with col1:
                    new_pos = st.selectbox("Position", ["Intern", "Janitor", "Courier", "Branch Manager", "Driver","Regional Manager","Human Resources","Desk Officer"],
                                            index=["Intern", "Janitor", "Courier", "Branch Manager", "Driver","Regional Manager","Human Resources","Desk Officer"].index(current_data['Position'])
                                              if current_data['Position'] in ["Intern", "Janitor", "Courier", "Branch Manager", "Driver","Regional Manager","Human Resources","Desk Officer"] else 0)
                    
                    new_phone = st.text_input("Phone Number", value=current_data['Phone'])
                with col2:
                    new_salary = st.number_input("Salary", value=float(current_data['Salary']))
                    # Şube ID'sinden Şube Adını bulup varsayılan yapma kısmı biraz kompleks olabilir, basit tutuyoruz:
                    new_branch = st.selectbox("Branch", list(branch_options.keys()))

                c1, c2 = st.columns([1,1])
                with c1:
                    update_btn = st.form_submit_button("Update Information", type="primary", use_container_width=True)
                with c2:
                    delete_btn = st.form_submit_button("Delete Employee 🗑️", type="secondary", use_container_width=True)

                if update_btn:
                    new_branch_id = branch_options.get(new_branch)
                    upd_sql = "UPDATE Employees SET Position=%s, Salary=%s, Phone=%s, BranchID=%s WHERE EmployeeID=%s"
                    run_query(upd_sql, (new_pos, new_salary, new_phone, new_branch_id, selected_emp_id))
                    st.success("Informations Updated.")
                    st.rerun()
                
                if delete_btn:
                    run_query("DELETE FROM Employees WHERE EmployeeID = %s", (selected_emp_id,))
                    st.error("Employee record deleted")
                    st.rerun()
        else:
            st.warning("No employee found to arrange.")


def show_admin_tools():
    st.title("🔧 Admin Operations Panel")
    st.write("Update cargo status instantly across the system.")
    st.divider()
    
    with st.container(border=True):
        st.subheader("Update Status")
        col1, col2 = st.columns(2)
        
        with col1:
            update_cargo_id = st.text_input("Cargo ID to Update (Ex: CG001)")
        with col2:
            new_status = st.selectbox("New Status", 
                ["Preparing", "In Delivery for Cargo Branch", "Out for Delivery", "Delivered"])
        
        if st.button("Update Status", type="primary"):
            if update_cargo_id:
                update_query = "UPDATE Cargos SET CurrentStatus = %s WHERE CargoID = %s"
                res = run_query(update_query, (new_status, update_cargo_id))
                if res is not None:
                    st.success(f"✅ Cargo **{update_cargo_id}** status updated to **'{new_status}'**")
            else:
                st.warning("⚠️ Please enter a Cargo ID.")