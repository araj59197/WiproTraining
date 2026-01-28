import pytest
import time
import json
import os
from datetime import datetime


class UserService:
    def __init__(self):
        self.users = {}

    def create_user(self, user_id, name, email):
        if user_id in self.users:
            raise ValueError("User already exists")
        self.users[user_id] = {"name": name, "email": email, "created_at": datetime.now().isoformat()}
        return self.users[user_id]

    def get_user(self, user_id):
        if user_id not in self.users:
            raise KeyError("User not found")
        return self.users[user_id]

    def update_user(self, user_id, name=None, email=None):
        if user_id not in self.users:
            raise KeyError("User not found")
        if name:
            self.users[user_id]["name"] = name
        if email:
            self.users[user_id]["email"] = email
        return self.users[user_id]

    def delete_user(self, user_id):
        if user_id not in self.users:
            raise KeyError("User not found")
        del self.users[user_id]
        return True

    def list_users(self):
        return list(self.users.values())


class OrderService:
    def __init__(self, user_service):
        self.user_service = user_service
        self.orders = {}
        self.order_counter = 0

    def create_order(self, user_id, items, total):
        self.user_service.get_user(user_id)
        self.order_counter += 1
        order_id = f"ORD-{self.order_counter}"
        self.orders[order_id] = {
            "user_id": user_id,
            "items": items,
            "total": total,
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
        return order_id, self.orders[order_id]

    def get_order(self, order_id):
        if order_id not in self.orders:
            raise KeyError("Order not found")
        return self.orders[order_id]

    def update_order_status(self, order_id, status):
        if order_id not in self.orders:
            raise KeyError("Order not found")
        valid_statuses = ["pending", "confirmed", "shipped", "delivered", "cancelled"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {valid_statuses}")
        self.orders[order_id]["status"] = status
        return self.orders[order_id]

    def get_user_orders(self, user_id):
        return {oid: order for oid, order in self.orders.items() if order["user_id"] == user_id}


class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, product_id, name, price, quantity=1):
        for item in self.items:
            if item["product_id"] == product_id:
                item["quantity"] += quantity
                return self.items
        self.items.append({"product_id": product_id, "name": name, "price": price, "quantity": quantity})
        return self.items

    def remove_item(self, product_id):
        self.items = [item for item in self.items if item["product_id"] != product_id]
        return self.items

    def get_total(self):
        return sum(item["price"] * item["quantity"] for item in self.items)

    def clear(self):
        self.items = []
        return self.items


@pytest.fixture
def user_service():
    return UserService()


@pytest.fixture
def order_service(user_service):
    return OrderService(user_service)


@pytest.fixture
def shopping_cart():
    return ShoppingCart()


@pytest.fixture
def sample_user(user_service):
    return user_service.create_user("user1", "John Doe", "john@example.com")


class TestUserServiceFunctional:
    def test_complete_user_lifecycle(self, user_service):
        user = user_service.create_user("u1", "Alice", "alice@test.com")
        assert user["name"] == "Alice"
        
        fetched = user_service.get_user("u1")
        assert fetched["email"] == "alice@test.com"
        
        updated = user_service.update_user("u1", name="Alice Smith")
        assert updated["name"] == "Alice Smith"
        
        result = user_service.delete_user("u1")
        assert result is True
        
        with pytest.raises(KeyError):
            user_service.get_user("u1")

    def test_multiple_users_management(self, user_service):
        users_data = [
            ("u1", "User One", "one@test.com"),
            ("u2", "User Two", "two@test.com"),
            ("u3", "User Three", "three@test.com"),
        ]
        
        for uid, name, email in users_data:
            user_service.create_user(uid, name, email)
        
        all_users = user_service.list_users()
        assert len(all_users) == 3
        
        user_service.delete_user("u2")
        all_users = user_service.list_users()
        assert len(all_users) == 2

    def test_duplicate_user_prevention(self, user_service):
        user_service.create_user("u1", "First User", "first@test.com")
        
        with pytest.raises(ValueError, match="User already exists"):
            user_service.create_user("u1", "Duplicate User", "dup@test.com")


class TestOrderServiceFunctional:
    def test_complete_order_workflow(self, user_service, order_service):
        user_service.create_user("buyer1", "Buyer", "buyer@test.com")
        
        order_id, order = order_service.create_order(
            "buyer1",
            [{"product": "Laptop", "qty": 1}],
            999.99
        )
        assert order["status"] == "pending"
        
        order_service.update_order_status(order_id, "confirmed")
        order = order_service.get_order(order_id)
        assert order["status"] == "confirmed"
        
        order_service.update_order_status(order_id, "shipped")
        order_service.update_order_status(order_id, "delivered")
        
        order = order_service.get_order(order_id)
        assert order["status"] == "delivered"

    def test_order_requires_valid_user(self, order_service):
        with pytest.raises(KeyError, match="User not found"):
            order_service.create_order("nonexistent", [], 0)

    def test_multiple_orders_per_user(self, user_service, order_service):
        user_service.create_user("shopper", "Shopper", "shop@test.com")
        
        order_service.create_order("shopper", [{"item": "Book"}], 29.99)
        order_service.create_order("shopper", [{"item": "Pen"}], 4.99)
        order_service.create_order("shopper", [{"item": "Notebook"}], 9.99)
        
        user_orders = order_service.get_user_orders("shopper")
        assert len(user_orders) == 3


class TestShoppingCartFunctional:
    def test_complete_shopping_experience(self, shopping_cart):
        shopping_cart.add_item("P001", "Keyboard", 79.99, 1)
        shopping_cart.add_item("P002", "Mouse", 29.99, 2)
        shopping_cart.add_item("P003", "Monitor", 299.99, 1)
        
        assert len(shopping_cart.items) == 3
        
        expected_total = 79.99 + (29.99 * 2) + 299.99
        assert shopping_cart.get_total() == pytest.approx(expected_total, 0.01)
        
        shopping_cart.remove_item("P002")
        assert len(shopping_cart.items) == 2
        
        shopping_cart.clear()
        assert len(shopping_cart.items) == 0
        assert shopping_cart.get_total() == 0

    def test_quantity_aggregation(self, shopping_cart):
        shopping_cart.add_item("P001", "Widget", 10.00, 2)
        shopping_cart.add_item("P001", "Widget", 10.00, 3)
        
        assert len(shopping_cart.items) == 1
        assert shopping_cart.items[0]["quantity"] == 5
        assert shopping_cart.get_total() == 50.00


class TestEndToEndScenarios:
    def test_full_ecommerce_flow(self, user_service, order_service, shopping_cart):
        user = user_service.create_user("customer1", "Customer", "cust@shop.com")
        assert user is not None
        
        shopping_cart.add_item("PROD1", "Laptop", 999.99, 1)
        shopping_cart.add_item("PROD2", "Case", 49.99, 1)
        shopping_cart.add_item("PROD3", "Mouse", 29.99, 1)
        
        total = shopping_cart.get_total()
        assert total == pytest.approx(1079.97, 0.01)
        
        order_id, order = order_service.create_order(
            "customer1",
            shopping_cart.items.copy(),
            total
        )
        assert order["status"] == "pending"
        
        shopping_cart.clear()
        assert len(shopping_cart.items) == 0
        
        order_service.update_order_status(order_id, "confirmed")
        order_service.update_order_status(order_id, "shipped")
        order_service.update_order_status(order_id, "delivered")
        
        final_order = order_service.get_order(order_id)
        assert final_order["status"] == "delivered"
        assert final_order["total"] == pytest.approx(1079.97, 0.01)

    def test_order_cancellation_flow(self, user_service, order_service):
        user_service.create_user("canceller", "Cancel User", "cancel@test.com")
        
        order_id, _ = order_service.create_order("canceller", [{"item": "Test"}], 100)
        
        order_service.update_order_status(order_id, "cancelled")
        
        order = order_service.get_order(order_id)
        assert order["status"] == "cancelled"


class TestParallelExecution:
    @pytest.mark.parametrize("test_id", range(1, 11))
    def test_parallel_user_creation(self, user_service, test_id):
        user_id = f"parallel_user_{test_id}"
        user = user_service.create_user(user_id, f"User {test_id}", f"user{test_id}@test.com")
        assert user["name"] == f"User {test_id}"
        time.sleep(0.1)

    @pytest.mark.parametrize("batch", ["A", "B", "C", "D", "E"])
    def test_parallel_cart_operations(self, shopping_cart, batch):
        for i in range(5):
            shopping_cart.add_item(f"{batch}-{i}", f"Product {batch}{i}", 10.00 * (i + 1))
        assert len(shopping_cart.items) == 5
        assert shopping_cart.get_total() > 0
        time.sleep(0.1)


class TestHistoryTracking:
    @pytest.fixture
    def history_file(self, tmp_path):
        return tmp_path / "test_history.json"

    def test_execution_logging(self, history_file):
        execution_record = {
            "timestamp": datetime.now().isoformat(),
            "test_name": "test_execution_logging",
            "status": "passed",
            "duration": 0.05
        }
        
        history = []
        if history_file.exists():
            history = json.loads(history_file.read_text())
        
        history.append(execution_record)
        history_file.write_text(json.dumps(history, indent=2))
        
        loaded = json.loads(history_file.read_text())
        assert len(loaded) >= 1
        assert loaded[-1]["test_name"] == "test_execution_logging"

    def test_history_accumulation(self, history_file):
        for i in range(3):
            record = {
                "timestamp": datetime.now().isoformat(),
                "iteration": i,
                "status": "passed"
            }
            
            history = []
            if history_file.exists():
                history = json.loads(history_file.read_text())
            history.append(record)
            history_file.write_text(json.dumps(history, indent=2))
        
        final_history = json.loads(history_file.read_text())
        assert len(final_history) == 3


"""
=== PYTEST SCALABLE TEST AUTOMATION EXPLANATION ===

1. PARALLEL EXECUTION (pytest-xdist):
   - Install: pip install pytest-xdist
   - Run with multiple CPUs: pytest -n auto (uses all available CPUs)
   - Run with specific workers: pytest -n 4 (uses 4 workers)
   - Distributes tests across workers for faster execution

2. HTML REPORTS (pytest-html):
   - Install: pip install pytest-html
   - Generate: pytest --html=report.html --self-contained-html
   - Creates visual HTML report with pass/fail details

3. JUNIT XML REPORTS:
   - Built into pytest: pytest --junitxml=results.xml
   - Compatible with CI/CD tools (Jenkins, GitLab, Azure DevOps)

4. TEST HISTORY & TRACKING:
   - Use pytest-history or allure-pytest for detailed tracking
   - Store results in JSON/database for trend analysis

5. SCALABILITY FEATURES:
   - Markers for test categorization (@pytest.mark.slow, @pytest.mark.smoke)
   - Fixtures with different scopes (function, class, module, session)
   - Parameterization for data-driven testing
   - Plugin architecture for extensibility

=== COMMANDS TO RUN ===

# Basic run
pytest q2.py -v

# Parallel execution (4 workers)
pytest q2.py -n 4 -v

# Generate HTML report
pytest q2.py --html=reports/report.html --self-contained-html

# Generate JUnit XML report
pytest q2.py --junitxml=reports/results.xml

# Combined parallel + reports
pytest q2.py -n auto --html=reports/report.html --junitxml=reports/results.xml -v

# Run specific test class
pytest q2.py::TestEndToEndScenarios -v

# Run with coverage
pytest q2.py --cov=. --cov-report=html
"""
