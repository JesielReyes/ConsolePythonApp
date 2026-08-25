customers = {
    1: {
        "id": 1,
        "name": "Alice",
        "username": "alice",
        "password": "pass123"
    },
    2: {
        "id": 2,
        "name": "Bob",
        "username": "bob",
        "password": "pass456"
    }
}


def get_all_customers():
    return customers


def get_customer(customer_id):
    return customers.get(customer_id)