"""
Integration Test Runner with Detailed Validation
Run with: python run_integration_tests.py
"""
import sys
import os
import time
import json
from datetime import datetime
from pathlib import Path

# Ensure we can import from tests directory
if __name__ == "__main__":
    # Import test components directly
    from tests.test_integration_e2e import IntegrationTestSuite
    from tests.test_data_fixtures import (
        SAMPLE_CUSTOMERS,
        SAMPLE_PRODUCTS,
        ORDER_SCENARIOS,
        DB_VALIDATION_RULES,
        FILE_VALIDATION_RULES,
        PERFORMANCE_BENCHMARKS
    )


class DetailedTestRunner:
    """Enhanced test runner with detailed validation and reporting"""
    
    def __init__(self):
        self.suite = IntegrationTestSuite()
        self.performance_metrics = {}
        self.validation_results = []
        
    def measure_time(self, func, *args, **kwargs):
        """Measure execution time of a function"""
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed = end_time - start_time
        return result, elapsed
        
    def validate_database_schema(self):
        """Validate database schema matches expectations"""
        print("\n" + "="*60)
        print("VALIDATING DATABASE SCHEMA")
        print("="*60)
        
        from sqlalchemy import inspect
        from app.database import Base
        from tests.test_integration_e2e import test_engine
        
        inspector = inspect(test_engine)
        tables = inspector.get_table_names()
        
        expected_tables = ['customers', 'products', 'orders', 'order_items', 'ai_action_logs']
        
        for table in expected_tables:
            if table in tables:
                columns = [col['name'] for col in inspector.get_columns(table)]
                print(f"✅ Table '{table}' exists with {len(columns)} columns")
            else:
                print(f"❌ Table '{table}' missing")
                
    def validate_order_data(self, order_id):
        """Detailed validation of order data"""
        print("\n" + "="*60)
        print(f"DETAILED ORDER VALIDATION (ID: {order_id})")
        print("="*60)
        
        from tests.test_integration_e2e import TestSessionLocal
        from app.models.order import Order
        
        db = TestSessionLocal()
        try:
            order = db.query(Order).filter(Order.id == order_id).first()
            
            if not order:
                print(f"❌ Order {order_id} not found")
                return False
                
            # Validate required fields
            rules = DB_VALIDATION_RULES['order']
            for field in rules['required_fields']:
                value = getattr(order, field, None)
                if value is not None:
                    print(f"✅ {field}: {value}")
                else:
                    print(f"❌ {field}: MISSING")
                    
            # Validate status
            if order.status in rules['status_values']:
                print(f"✅ Status valid: {order.status}")
            else:
                print(f"❌ Invalid status: {order.status}")
                
            # Validate total amount
            if order.total_amount >= rules['min_total_amount']:
                print(f"✅ Total amount valid: ₹{order.total_amount}")
            else:
                print(f"❌ Invalid total: ₹{order.total_amount}")
                
            # Validate order items
            print(f"\n📦 Order Items ({len(order.items)}):")
            for item in order.items:
                print(f"   - {item.product.name}: {item.quantity} × ₹{item.unit_price} = ₹{item.total_price}")
                
                # Validate item data
                if item.quantity >= DB_VALIDATION_RULES['order_item']['min_quantity']:
                    print(f"     ✅ Quantity valid")
                else:
                    print(f"     ❌ Invalid quantity: {item.quantity}")
                    
            return True
            
        finally:
            db.close()
            
    def validate_invoice_file(self, invoice_path):
        """Validate invoice file"""
        print("\n" + "="*60)
        print("INVOICE FILE VALIDATION")
        print("="*60)
        
        if not os.path.exists(invoice_path):
            print(f"❌ Invoice file not found: {invoice_path}")
            return False
            
        file_size = os.path.getsize(invoice_path)
        rules = FILE_VALIDATION_RULES['invoice']
        
        print(f"✅ File exists: {invoice_path}")
        print(f"✅ File size: {file_size} bytes")
        
        if file_size >= rules['min_size_bytes']:
            print(f"✅ Size above minimum ({rules['min_size_bytes']} bytes)")
        else:
            print(f"❌ File too small")
            return False
            
        if file_size <= rules['max_size_bytes']:
            print(f"✅ Size below maximum ({rules['max_size_bytes']} bytes)")
        else:
            print(f"❌ File too large")
            return False
            
        return True
        
    def check_performance_benchmarks(self):
        """Check if performance meets benchmarks"""
        print("\n" + "="*60)
        print("PERFORMANCE BENCHMARK RESULTS")
        print("="*60)
        
        all_passed = True
        
        for metric_name, elapsed_time in self.performance_metrics.items():
            if metric_name in PERFORMANCE_BENCHMARKS:
                benchmark = PERFORMANCE_BENCHMARKS[metric_name]
                max_time = benchmark['max_time_seconds']
                
                if elapsed_time <= max_time:
                    print(f"✅ {metric_name}: {elapsed_time:.3f}s (max: {max_time}s)")
                else:
                    print(f"❌ {metric_name}: {elapsed_time:.3f}s (EXCEEDED max: {max_time}s)")
                    all_passed = False
            else:
                print(f"⚠️ {metric_name}: {elapsed_time:.3f}s (no benchmark)")
                
        return all_passed
        
    def run_comprehensive_tests(self):
        """Run all tests with detailed validation"""
        print("\n" + "="*70)
        print("🚀 COMPREHENSIVE INTEGRATION TEST SUITE")
        print("="*70)
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Python: {sys.version.split()[0]}")
        print(f"Working Directory: {os.getcwd()}")
        
        try:
            # Setup
            self.suite.setup_database()
            self.validate_database_schema()
            
            # Seed data
            self.suite.seed_test_data()
            
            # Test AI chat to order (with timing)
            _, elapsed = self.measure_time(self.suite.test_ai_chat_to_order)
            self.performance_metrics['ai_processing'] = elapsed
            
            # Validate order
            order_id = self.suite.test_data.get('order_id')
            if order_id:
                self.validate_order_data(order_id)
            
            # Verify database
            self.suite.verify_database_order()
            
            # Verify inventory
            self.suite.verify_inventory_update()
            
            # Test invoice generation (with timing)
            _, elapsed = self.measure_time(self.suite.test_invoice_generation)
            self.performance_metrics['invoice_generation'] = elapsed
            
            # Validate invoice file
            if 'invoice_file' in self.suite.test_data:
                self.validate_invoice_file(self.suite.test_data['invoice_file'])
            
            # Verify AI logs
            self.suite.verify_ai_action_log()
            
            # Verify dashboard (with timing)
            _, elapsed = self.measure_time(self.suite.verify_dashboard_data)
            self.performance_metrics['dashboard_query'] = elapsed
            
            # Additional scenarios
            self.suite.test_additional_scenarios()
            
            # Performance check
            perf_passed = self.check_performance_benchmarks()
            
            # Generate report
            all_passed = self.suite.generate_report()
            
            # Final summary
            print("\n" + "="*70)
            if all_passed and perf_passed:
                print("🎉 ALL TESTS PASSED - SYSTEM FULLY OPERATIONAL")
                print("="*70)
                return 0
            elif all_passed:
                print("⚠️ TESTS PASSED BUT PERFORMANCE ISSUES DETECTED")
                print("="*70)
                return 0
            else:
                print("❌ SOME TESTS FAILED - REVIEW REPORT")
                print("="*70)
                return 1
                
        except Exception as e:
            print(f"\n❌ CRITICAL ERROR: {e}")
            import traceback
            traceback.print_exc()
            self.suite.generate_report()
            return 1


def main():
    """Main entry point"""
    runner = DetailedTestRunner()
    exit_code = runner.run_comprehensive_tests()
    
    print(f"\nTest run completed with exit code: {exit_code}")
    print(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
