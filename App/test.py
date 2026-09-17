import requests


BASE_URL = "http://127.0.0.1:8000"


# =========================
# 1. ROOT
# =========================

response = requests.get(f"{BASE_URL}/")

print("ROOT:", response.status_code)
print(response.json())


# =========================
# 2. CREATE USER
# =========================

user_data = {
    "name": "Test User",
    "email": "test@example.com",
    "password": "123456"
}

response = requests.post(
    f"{BASE_URL}/users",
    json=user_data
)

print("\nCREATE USER:", response.status_code)
print(response.text)

user = response.json()
user_id = user["user_id"]


# =========================
# 3. CREATE CATEGORY
# =========================

category_data = {
    "name": "Food"
}

response = requests.post(
    f"{BASE_URL}/categories",
    json=category_data
)

print("\nCREATE CATEGORY:", response.status_code)
print(response.text)

category = response.json()
category_id = category["id"]


# =========================
# 4. LOGIN
# =========================

login_data = {
    "email": "test@example.com",
    "password": "123456"
}

response = requests.post(
    f"{BASE_URL}/login",
    json=login_data
)

print("\nLOGIN:", response.status_code)
print(response.text)

token = response.json()


# =========================
# 5. AUTHORIZATION HEADER
# =========================

headers = {
    "Authorization": f"Bearer {token}"
}


# =========================
# 6. CREATE EXPENSE
# =========================

expense_data = {
    "amount": 500,
    "description": "Lunch",
    "category_id": category_id
}

response = requests.post(
    f"{BASE_URL}/expenses",
    json=expense_data,
    headers=headers
)

print("\nCREATE EXPENSE:", response.status_code)
print(response.text)

expense = response.json()
expense_id = expense["id"]


# =========================
# 7. GET EXPENSES
# =========================

response = requests.get(
    f"{BASE_URL}/expenses",
    headers=headers
)

print("\nGET EXPENSES:", response.status_code)
print(response.json())


# =========================
# 8. GET ONE EXPENSE
# =========================

response = requests.get(
    f"{BASE_URL}/expenses/{expense_id}",
    headers=headers
)

print("\nGET ONE EXPENSE:", response.status_code)
print(response.json())


# =========================
# 9. UPDATE EXPENSE
# =========================

update_data = {
    "amount": 750,
    "description": "Dinner"
}

response = requests.patch(
    f"{BASE_URL}/expenses/{expense_id}",
    json=update_data,
    headers=headers
)

print("\nUPDATE EXPENSE:", response.status_code)
print(response.json())


# =========================
# 10. DELETE EXPENSE
# =========================

response = requests.delete(
    f"{BASE_URL}/expenses/{expense_id}",
    headers=headers
)

print("\nDELETE EXPENSE:", response.status_code)
print(response.text)


# =========================
# 11. UPDATE USER
# =========================

update_user = {
    "name": "Updated Test User"
}

response = requests.patch(
    f"{BASE_URL}/users/{user_id}",
    json=update_user
)

print("\nUPDATE USER:", response.status_code)
print(response.text)


# =========================
# 12. GET USERS
# =========================

response = requests.get(
    f"{BASE_URL}/users"
)

print("\nGET USERS:", response.status_code)
print(response.text)


# =========================
# 13. GET CATEGORIES
# =========================

response = requests.get(
    f"{BASE_URL}/categories"
)

print("\nGET CATEGORIES:", response.status_code)
print(response.text)