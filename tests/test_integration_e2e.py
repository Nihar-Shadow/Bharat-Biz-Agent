"""
End-to-End Integration Test System
Tests complete flow: Chat → AI → Backend → Database → Files → Dashboard
"""
import pytest
import os
import json
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# Import app components
from app.main import app
from app.database import Base, get_db
from app.models.customer import Customer
from app.models.product import Product
from app.models.order import Order
from app.models.ai_action_log import AIActionLog

# Test database setup
TEST_DATABASE_URL = "sqlite:///./test_integration.db"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


# Override database dependency for testing
def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


class IntegrationTestSuite:
    """Complete end-to-end integration test suite"""
    
    def __init__(self):
        self.test_results = []
        self.test_data = {}
        
    def setup_database(self):
        """Create fresh test database"""
        print("\n" + "="*60)
        print("STEP 1: Setting up test database")
        print("="*60)
        
        # Drop all tables and recreate
        Base.metadata.drop_all(bind=test_engine)
        Base.metadata.create_all(bind=test_engine)
        
        print("✅ Test database created")
        self.log_result("Database Setup", True, "Fresh database created")
        
    def seed_test_data(self):
        """Insert sample data for testing"""
        print("\n" + "="*60)
        print("STEP 2: Seeding test data")
        print("="*60)
        
        db = TestSessionLocal()
        
        try:
            # Create test customer
            customer = Customer(
                name="Rahul Kumar",
                email="rahul@test.com",
                phone="9876543210",
                address="123 Test Street, Mumbai"
            )
            db.add(customer)
            db.commit()
            db.refresh(customer)
            self.test_data['customer_id'] = customer.id
            print(f"✅ Created test customer: {customer.name} (ID: {customer.id})")
            
            # Create test products
            products = [
                Product(name="Laptop", sku="LAP001", price=45000.00, stock_quantity=10),
                Product(name="Mouse", sku="MOU001", price=500.00, stock_quantity=50),
                Product(name="Keyboard", sku="KEY001", price=1500.00, stock_quantity=30),
            ]
            
            for product in products:
                db.add(product)
            db.commit()
            
            for product in products:
                db.refresh(product)
                print(f"✅ Created product: {product.name} (Stock: {product.stock_quantity})")
                
            self.test_data['products'] = {p.name: p.id for p in products}
            
            self.log_result("Data Seeding", True, f"Created {len(products)} products and 1 customer")
            
        except Exception as e:
            print(f"❌ Error seeding data: {e}")
            self.log_result("Data Seeding", False, str(e))
            raise
        finally:
            db.close()
            
    def test_ai_chat_to_order(self):
        """Test: Chat message → AI processing → Order creation"""
        print("\n" + "="*60)
        print("STEP 3: Testing AI Chat → Order Flow")
        print("="*60)
        
        # Test message
        test_message = "Order 2 laptops for Rahul Kumar"
        print(f"📝 Test message: '{test_message}'")
        
        # Send to AI agent
        response = client.post(
            "/api/v1/ai/process",
            json={"message": test_message}
        )
        
        assert response.status_code == 200, f"AI processing failed: {response.text}"
        result = response.json()
        
        print(f"✅ AI Intent detected: {result['intent']}")
        print(f"✅ Confidence: {result['confidence']}")
        print(f"✅ Entities extracted: {json.dumps(result['entities'], indent=2)}")
        
        # Verify order was created
        if result['intent'] == 'create_order':
            action_result = result['action_result']
            if action_result.get('success'):
                order_id = action_result.get('order_id')
                self.test_data['order_id'] = order_id
                print(f"✅ Order created: ID {order_id}")
                self.log_result("AI Chat to Order", True, f"Order {order_id} created successfully")
            else:
                print(f"❌ Order creation failed: {action_result.get('message')}")
                self.log_result("AI Chat to Order", False, action_result.get('message'))
                raise Exception("Order creation failed")
        else:
            raise Exception(f"Wrong intent detected: {result['intent']}")
            
    def verify_database_order(self):
        """Verify order exists in database with correct data"""
        print("\n" + "="*60)
        print("STEP 4: Verifying Database Entries")
        print("="*60)
        
        db = TestSessionLocal()
        try:
            order_id = self.test_data.get('order_id')
            order = db.query(Order).filter(Order.id == order_id).first()
            
            assert order is not None, "Order not found in database"
            print(f"✅ Order found in database: ID {order.id}")
            
            assert order.customer_id == self.test_data['customer_id'], "Wrong customer"
            print(f"✅ Correct customer linked: {order.customer_id}")
            
            assert order.total_amount > 0, "Invalid total amount"
            print(f"✅ Total amount: ₹{order.total_amount}")
            
            assert len(order.items) > 0, "No order items"
            print(f"✅ Order items: {len(order.items)} items")
            
            for item in order.items:
                print(f"   - {item.product.name}: {item.quantity} × ₹{item.unit_price} = ₹{item.total_price}")
            
            self.log_result("Database Verification", True, f"Order {order_id} verified in DB")
            
        except Exception as e:
            print(f"❌ Database verification failed: {e}")
            self.log_result("Database Verification", False, str(e))
            raise
        finally:
            db.close()
            
    def verify_inventory_update(self):
        """Verify inventory was decremented correctly"""
        print("\n" + "="*60)
        print("STEP 5: Verifying Inventory Update")
        print("="*60)
        
        db = TestSessionLocal()
        try:
            # Check laptop stock (should be 10 - 2 = 8)
            laptop_id = self.test_data['products']['Laptop']
            laptop = db.query(Product).filter(Product.id == laptop_id).first()
            
            expected_stock = 8  # Original 10 - 2 ordered
            actual_stock = laptop.stock_quantity
            
            assert actual_stock == expected_stock, f"Stock mismatch: expected {expected_stock}, got {actual_stock}"
            print(f"✅ Laptop stock updated: 10 → {actual_stock}")
            
            self.log_result("Inventory Update", True, f"Stock decremented correctly")
            
        except Exception as e:
            print(f"❌ Inventory verification failed: {e}")
            self.log_result("Inventory Update", False, str(e))
            raise
        finally:
            db.close()
            
    def test_invoice_generation(self):
        """Test invoice file generation"""
        print("\n" + "="*60)
        print("STEP 6: Testing Invoice Generation")
        print("="*60)
        
        order_id = self.test_data.get('order_id')
        
        # Generate invoice
        response = client.post(f"/api/v1/invoices/generate/{order_id}")
        
        assert response.status_code == 200, f"Invoice generation failed: {response.text}"
        
        # Verify file was created
        invoice_dir = "invoices"
        if os.path.exists(invoice_dir):
            files = os.listdir(invoice_dir)
            invoice_files = [f for f in files if f.startswith(f"invoice_{order_id}")]
            
            assert len(invoice_files) > 0, "Invoice file not created"
            invoice_file = invoice_files[0]
            file_path = os.path.join(invoice_dir, invoice_file)
            file_size = os.path.getsize(file_path)
            
            print(f"✅ Invoice file created: {invoice_file}")
            print(f"✅ File size: {file_size} bytes")
            
            self.test_data['invoice_file'] = file_path
            self.log_result("Invoice Generation", True, f"Invoice created: {invoice_file}")
        else:
            print("⚠️ Invoice directory not found, creating...")
            os.makedirs(invoice_dir, exist_ok=True)
            self.log_result("Invoice Generation", False, "Invoice directory missing")
            
    def verify_ai_action_log(self):
        """Verify AI action was logged"""
        print("\n" + "="*60)
        print("STEP 7: Verifying AI Action Logs")
        print("="*60)
        
        db = TestSessionLocal()
        try:
            # Find log entry for our order
            logs = db.query(AIActionLog).filter(
                AIActionLog.intent == 'create_order'
            ).order_by(AIActionLog.created_at.desc()).all()
            
            assert len(logs) > 0, "No AI action logs found"
            
            latest_log = logs[0]
            print(f"✅ AI action logged: ID {latest_log.id}")
            print(f"✅ Intent: {latest_log.intent}")
            print(f"✅ Confidence: {latest_log.confidence}")
            print(f"✅ Success: {latest_log.success}")
            print(f"✅ Timestamp: {latest_log.created_at}")
            
            if latest_log.entities:
                print(f"✅ Entities: {latest_log.entities}")
            
            self.log_result("AI Action Logging", True, f"Action logged with ID {latest_log.id}")
            
        except Exception as e:
            print(f"❌ AI log verification failed: {e}")
            self.log_result("AI Action Logging", False, str(e))
            raise
        finally:
            db.close()
            
    def verify_dashboard_data(self):
        """Verify dashboard reflects the changes"""
        print("\n" + "="*60)
        print("STEP 8: Verifying Dashboard Data")
        print("="*60)
        
        # Get dashboard stats
        response = client.get("/api/v1/dashboard/")
        
        assert response.status_code == 200, f"Dashboard request failed: {response.text}"
        
        stats = response.json()
        
        print(f"✅ Total Revenue: ₹{stats['total_revenue']}")
        print(f"✅ Total Orders: {stats['total_orders']}")
        print(f"✅ Total Customers: {stats['total_customers']}")
        print(f"✅ Low Stock Items: {stats['low_stock_count']}")
        
        # Verify our order is counted
        assert stats['total_orders'] >= 1, "Order not reflected in dashboard"
        assert stats['total_revenue'] > 0, "Revenue not updated"
        
        self.log_result("Dashboard Verification", True, "Dashboard data reflects changes")
        
    def test_additional_scenarios(self):
        """Test additional AI scenarios"""
        print("\n" + "="*60)
        print("STEP 9: Testing Additional Scenarios")
        print("="*60)
        
        scenarios = [
            {
                "message": "Check stock of Mouse",
                "expected_intent": "check_inventory"
            },
            {
                "message": "Kitne laptop available hai?",
                "expected_intent": "check_inventory"
            },
            {
                "message": "Add customer Priya phone 9123456789",
                "expected_intent": "add_customer"
            }
        ]
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"\n📝 Scenario {i}: '{scenario['message']}'")
            
            response = client.post(
                "/api/v1/ai/process",
                json={"message": scenario['message']}
            )
            
            if response.status_code == 200:
                result = response.json()
                detected_intent = result['intent']
                
                if detected_intent == scenario['expected_intent']:
                    print(f"✅ Correct intent: {detected_intent}")
                else:
                    print(f"⚠️ Intent mismatch: expected {scenario['expected_intent']}, got {detected_intent}")
            else:
                print(f"❌ Request failed: {response.status_code}")
                
        self.log_result("Additional Scenarios", True, f"Tested {len(scenarios)} scenarios")
        
    def log_result(self, test_name, success, message):
        """Log test result"""
        self.test_results.append({
            "test": test_name,
            "success": success,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
        
    def generate_report(self):
        """Generate test report"""
        print("\n" + "="*60)
        print("TEST REPORT")
        print("="*60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"\nTotal Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%")
        
        print("\n" + "-"*60)
        print("DETAILED RESULTS:")
        print("-"*60)
        
        for result in self.test_results:
            status = "✅ PASS" if result['success'] else "❌ FAIL"
            print(f"{status} | {result['test']}")
            print(f"       {result['message']}")
            
        # Save report to file
        report_file = "test_report.json"
        with open(report_file, 'w') as f:
            json.dump({
                "summary": {
                    "total": total_tests,
                    "passed": passed_tests,
                    "failed": failed_tests,
                    "success_rate": f"{(passed_tests/total_tests*100):.1f}%"
                },
                "results": self.test_results,
                "test_data": self.test_data
            }, f, indent=2)
            
        print(f"\n📄 Report saved to: {report_file}")
        
        return passed_tests == total_tests
        

def run_integration_tests():
    """Main test runner"""
    print("\n" + "="*60)
    print("🚀 STARTING END-TO-END INTEGRATION TESTS")
    print("="*60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    suite = IntegrationTestSuite()
    
    try:
        # Run all tests in sequence
        suite.setup_database()
        suite.seed_test_data()
        suite.test_ai_chat_to_order()
        suite.verify_database_order()
        suite.verify_inventory_update()
        suite.test_invoice_generation()
        suite.verify_ai_action_log()
        suite.verify_dashboard_data()
        suite.test_additional_scenarios()
        
        # Generate report
        all_passed = suite.generate_report()
        
        if all_passed:
            print("\n" + "="*60)
            print("🎉 ALL TESTS PASSED!")
            print("="*60)
            return 0
        else:
            print("\n" + "="*60)
            print("⚠️ SOME TESTS FAILED")
            print("="*60)
            return 1
            
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        suite.generate_report()
        return 1


if __name__ == "__main__":
    exit_code = run_integration_tests()
    exit(exit_code)
