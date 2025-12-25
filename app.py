import streamlit as st
import os
import pandas as pd
import base64

# ================= BACKGROUND STYLE =================

def set_background(image_file):
    with open(image_file, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# CALL THE FUNCTION
set_background("photo.png")

# ================= FILE HELPERS =================

def ensure_file(file):
    if not os.path.exists(file):
        open(file, "w").close()

def read_file(file):
    ensure_file(file)
    with open(file, "r") as f:
        return [line.strip() for line in f if line.strip()]

def write_file(file, lines):
    with open(file, "w") as f:
        for l in lines:
            f.write(l + "\n")

def append_file(file, line):
    with open(file, "a") as f:
        f.write(line.strip() + "\n")

# ================= INIT FILES =================

for f in ["admins.txt", "users.txt", "cars.txt", "waiting.txt", "returned.txt"]:
    ensure_file(f)

# ================= SAMPLE CARS =================

sample_cars = [
    "Mehran Hatchback 2009 5000 Available",
    "Corolla Sedan 2015 8000 Available",
    "Civic Sedan 2018 10000 Available",
    "Cultus Hatchback 2017 6000 Available",
    "City Sedan 2019 11000 Available",
    "BRV SUV 2021 18000 Available",
    "Yaris Sedan 2022 13000 Available",
    "Alto Hatchback 2020 5000 Available",
    "Fortuner SUV 2023 25000 Available",
    "Sportage SUV 2021 22000 Available",
]

existing = read_file("cars.txt")
models = [c.split()[0] for c in existing]
merged = existing[:]

for car in sample_cars:
    if car.split()[0] not in models:
        merged.append(car)

write_file("cars.txt", merged)

# ================= SESSION =================

if "role" not in st.session_state:
    st.session_state.role = None
    st.session_state.user = None

st.set_page_config("Car Rental System", layout="centered")
set_background("photo.png")

# Custom Title Bar
st.markdown("<div class='title-bar'><h1>Car Rental App 🚗</h1></div>", unsafe_allow_html=True)

st.markdown("<div class='glass'>", unsafe_allow_html=True)


# ================= MAIN MENU =================

if st.session_state.role is None:
    menu = st.selectbox(
        "Menu",
        ["Admin Login", "Admin Signup", "User Login", "User Signup"]
    )

    if menu == "Admin Login":
        u = st.text_input("Admin Username")
        p = st.text_input("Admin Password", type="password")

        if st.button("Login"):
            for a in read_file("admins.txt"):
                parts = a.split()
                if len(parts) >= 2 and u == parts[0] and p == parts[1]:
                    st.session_state.role = "admin"
                    st.session_state.user = u
                    st.rerun()
            st.error("Invalid admin credentials")

    if menu == "Admin Signup":
        u = st.text_input("New Admin Username")
        p = st.text_input("New Admin Password", type="password")

        if st.button("Register"):
            if any(u == a.split()[0] for a in read_file("admins.txt")):
                st.error("Admin already exists")
            else:
                append_file("admins.txt", f"{u} {p}")
                st.success("Admin registered")

    if menu == "User Login":
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")

        if st.button("Login"):
            for usr in read_file("users.txt"):
                parts = usr.split()
                if len(parts) >= 2 and u == parts[0] and p == parts[1]:
                    st.session_state.role = "user"
                    st.session_state.user = u
                    st.rerun()
            st.error("Invalid user credentials")

    if menu == "User Signup":
        u = st.text_input("New Username")
        p = st.text_input("New Password", type="password")

        if st.button("Register"):
            if any(u == usr.split()[0] for usr in read_file("users.txt")):
                st.error("User already exists")
            else:
                append_file("users.txt", f"{u} {p}")
                st.success("User registered")

# ================= ADMIN MENU =================

elif st.session_state.role == "admin":
    st.subheader("🔐 ADMIN MENU")

    option = st.selectbox(
        "Options",
        [
            "Add Car",
            "Remove Car",
            "View All Cars",
            "View Available Cars",
            "View Waiting Queue",
            "View Returned Cars",
            "Logout",
        ],
    )

    if option == "Add Car":
        model = st.text_input("Model")
        ctype = st.text_input("Type")
        year = st.text_input("Year")
        rate = st.text_input("Rate")

        if st.button("Add"):
            append_file("cars.txt", f"{model} {ctype} {year} {rate} Available")
            st.success("Car added")
            st.rerun()

    if option == "Remove Car":
        model = st.text_input("Car model to remove")
        if st.button("Remove"):
            write_file("cars.txt", [c for c in read_file("cars.txt") if not c.startswith(model)])
            st.success("Car removed")

    if option == "View All Cars":
        df = pd.DataFrame([c.split() for c in read_file("cars.txt")],
                          columns=["Model", "Type", "Year", "Rate", "Status"])
        st.dataframe(df, use_container_width=True)

    if option == "View Available Cars":
        cars = [c for c in read_file("cars.txt") if c.endswith("Available")]
        if cars:
            df = pd.DataFrame([c.split() for c in cars],
                              columns=["Model", "Type", "Year", "Rate", "Status"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No available cars")

    if option == "View Waiting Queue":
        st.dataframe(pd.DataFrame(read_file("waiting.txt"), columns=["Waiting Queue"])
                     if read_file("waiting.txt") else st.info("Queue empty"))

    if option == "View Returned Cars":
        st.dataframe(pd.DataFrame(read_file("returned.txt"), columns=["Returned Cars"])
                     if read_file("returned.txt") else st.info("No returned cars"))

    if option == "Logout":
        st.session_state.role = None
        st.session_state.user = None
        st.rerun()

# ================= USER MENU =================

elif st.session_state.role == "user":
    st.subheader("👤 USER MENU")

    option = st.selectbox(
        "Options",
        ["Rent Car", "Return Car", "View Booking", "Logout"]
    )

    if option == "Rent Car":
        model = st.text_input("Car model")
        if st.button("Rent"):
            cars = read_file("cars.txt")
            updated = []
            rented = False

            for c in cars:
                p = c.split()
                if p[0] == model and p[-1] == "Available":
                    p[-1] = "Rented"
                    rented = True
                    append_file("waiting.txt", f"{st.session_state.user} rented {model}")
                updated.append(" ".join(p))

            if rented:
                write_file("cars.txt", updated)
                st.success("Car rented")
                st.rerun()
            else:
                st.error("Car not available")

    if option == "Return Car":
        model = st.text_input("Car model to return")
        if st.button("Return"):
            cars = read_file("cars.txt")
            updated = []
            returned = False

            for c in cars:
                p = c.split()
                if p[0] == model and p[-1] == "Rented":
                    p[-1] = "Available"
                    returned = True
                    append_file("returned.txt", f"{st.session_state.user} returned {model}")
                updated.append(" ".join(p))

            if returned:
                write_file("cars.txt", updated)
                st.success("Car returned")
                st.rerun()
            else:
                st.error("Car not rented")

    if option == "View Booking":
        booked = [c for c in read_file("cars.txt") if c.endswith("Rented")]
        if booked:
            df = pd.DataFrame([c.split() for c in booked],
                              columns=["Model", "Type", "Year", "Rate", "Status"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No bookings")

    if option == "Logout":
        st.session_state.role = None
        st.session_state.user = None
        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)