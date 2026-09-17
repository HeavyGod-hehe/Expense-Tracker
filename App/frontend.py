import streamlit as st
import requests


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰"
)


# =========================
# SESSION STATE
# =========================

if "token" not in st.session_state:
    st.session_state.token = None


# =========================
# LOGIN / SIGNUP
# =========================

if st.session_state.token is None:

    st.title("💰 Expense Tracker")

    option = st.radio(
        "Choose an option",
        ["Login", "Sign Up"]
    )


    # =========================
    # LOGIN
    # =========================

    if option == "Login":

        st.subheader("Login")

        email = st.text_input("Email")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            response = requests.post(
                f"{API_URL}/login",
                json={
                    "email": email,
                    "password": password
                }
            )

            if response.status_code == 200:

                result = response.json()

                # Backend currently returns an error message
                # as a normal 200 response for wrong credentials
                if isinstance(result, str) and result.startswith("Email"):
                    st.error(result)

                else:
                    st.session_state.token = result

                    st.success("Login successful!")

                    st.rerun()

            else:

                st.error(
                    "Login failed."
                )


    # =========================
    # SIGN UP
    # =========================

    else:

        st.subheader("Create Account")

        name = st.text_input(
            "Name"
        )

        email = st.text_input(
            "Email"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password"
        )


        if st.button("Sign Up"):

            if name.strip() == "":

                st.error(
                    "Please enter your name."
                )

            elif email.strip() == "":

                st.error(
                    "Please enter your email."
                )

            elif password == "":

                st.error(
                    "Please enter a password."
                )

            elif password != confirm_password:

                st.error(
                    "Passwords do not match."
                )

            else:

                response = requests.post(
                    f"{API_URL}/users",
                    json={
                        "name": name,
                        "email": email,
                        "password": password
                    }
                )


                if response.status_code == 200:

                    st.success(
                        "Account created successfully! "
                        "You can now login."
                    )

                else:

                    st.error(
                        f"Signup failed: {response.text}"
                    )


    st.stop()


# =========================
# AUTH HEADER
# =========================

headers = {
    "Authorization": f"Bearer {st.session_state.token}"
}


# =========================
# SIDEBAR
# =========================

st.sidebar.title("💰 Expense Tracker")

page = st.sidebar.radio(
    "Menu",
    [
        "Dashboard",
        "Expenses",
        "Add Expense",
        "Categories"
    ]
)


if st.sidebar.button("Logout"):

    st.session_state.token = None

    st.rerun()


# =========================
# GET DATA
# =========================

expenses_response = requests.get(
    f"{API_URL}/expenses",
    headers=headers
)

categories_response = requests.get(
    f"{API_URL}/categories"
)


if expenses_response.status_code == 200:
    expenses = expenses_response.json()
else:
    expenses = []


if categories_response.status_code == 200:
    categories = categories_response.json()
else:
    categories = []


# =========================
# DASHBOARD
# =========================

if page == "Dashboard":

    st.title("Dashboard")

    total = sum(
        float(expense["amount"])
        for expense in expenses
    )

    st.metric(
        "Total Expenses",
        f"Rs. {total:,.2f}"
    )

    st.metric(
        "Number of Expenses",
        len(expenses)
    )

    st.divider()

    st.subheader("Recent Expenses")

    if len(expenses) == 0:

        st.info("No expenses yet.")

    else:

        for expense in expenses:

            st.write(
                f"**{expense['description']}** — "
                f"Rs. {expense['amount']}"
            )


# =========================
# EXPENSES
# =========================

elif page == "Expenses":

    st.title("📋 My Expenses")

    if len(expenses) == 0:

        st.info("No expenses found.")

    else:

        for expense in expenses:

            col1, col2 = st.columns([4, 1])

            with col1:

                st.write(
                    f"**{expense['description']}**"
                )

                st.write(
                    f"Rs. {expense['amount']} | "
                    f"Category ID: {expense['category_id']}"
                )

            with col2:

                if st.button(
                    "Delete",
                    key=f"delete_{expense['id']}"
                ):

                    response = requests.delete(
                        f"{API_URL}/expenses/{expense['id']}",
                        headers=headers
                    )

                    if response.status_code == 200:

                        st.success("Deleted!")

                        st.rerun()

                    else:

                        st.error(
                            "Could not delete expense."
                        )

            st.divider()


# =========================
# ADD EXPENSE
# =========================

elif page == "Add Expense":

    st.title("➕ Add Expense")

    amount = st.number_input(
        "Amount",
        min_value=0.0,
        step=100.0
    )

    description = st.text_input(
        "Description"
    )


    if len(categories) > 0:

        category_names = [
            category["name"]
            for category in categories
        ]

        selected_category = st.selectbox(
            "Category",
            category_names
        )

        selected_category_id = next(
            category["id"]
            for category in categories
            if category["name"] == selected_category
        )

    else:

        st.warning(
            "Create a category first."
        )

        selected_category_id = None


    if st.button("Save Expense"):

        if selected_category_id is None:

            st.error(
                "Please create a category first."
            )

        elif amount <= 0:

            st.error(
                "Amount must be greater than 0."
            )

        else:

            response = requests.post(
                f"{API_URL}/expenses",
                headers=headers,
                json={
                    "amount": amount,
                    "description": description,
                    "category_id": selected_category_id
                }
            )

            if response.status_code == 200:

                st.success(
                    "Expense added successfully!"
                )

            else:

                st.error(
                    response.text
                )


# =========================
# CATEGORIES
# =========================

elif page == "Categories":

    st.title("🏷️ Categories")

    st.subheader("Create Category")

    category_name = st.text_input(
        "Category name"
    )

    if st.button("Create Category"):

        if category_name.strip() == "":

            st.error(
                "Category name cannot be empty."
            )

        else:

            response = requests.post(
                f"{API_URL}/categories",
                json={
                    "name": category_name
                }
            )

            if response.status_code == 200:

                st.success(
                    "Category created!"
                )

                st.rerun()

            else:

                st.error(
                    response.text
                )


    st.divider()

    st.subheader("Your Categories")

    for category in categories:

        st.write(
            f"🏷️ {category['name']}"
        )