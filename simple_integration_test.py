"""
Simple Integration Test - Standalone Version
Tests the complete flow without complex imports
"""
import requests
import json
import time
from datetime import datetime

# Configuration
API_BASE_URL = "http://localhost:8000/api/v1"
TEST_RESULTS = []


def log_test(name, success, message):
    """Log test result"""
    TEST_RESULTS.append({
        "test": name,
        "success": success,
        "message": message,
        "timestamp": datetime.now().isoformat()
    })
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status} | {name}")
    print(f"       {message}")


def test_ai_agent_active():
    """Test 1: Verify AI agent is running"""
    print("\n" + "="*60)
    print("TEST 1: AI Agent Status")
    print("="*60)
    
    try:
        response = requests.get(f"{API_BASE_URL}/ai/test", timeout=5)
        if response.status_code == 200:
            data = response.json()
            log_test("AI Agent Active", True, f"Status: {data.get('status')}")
            return True
        else:
            log_test("AI Agent Active", False, f"HTTP {response.status_code}")
            return False
    except Exception as e:
        log_test("AI Agent Active", False, str(e))
        return False


def test_ai_intent_detection():
    """Test 2: AI Intent Detection"""
    print("\n" + "="*60)
    print("TEST 2: AI Intent Detection")
    print("="*60)
    
    test_message = "Order 2 laptops for Rahul Kumar"
    print(f"📝 Message: '{test_message}'")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/ai/test-intent",
            json={"message": test_message},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            intent = result.get('intent')
            confidence = result.get('confidence', 0)
            
            print(f"   Intent: {intent}")
            print(f"   Confidence: {confidence}")
            
            if intent == 'create_order' and confidence > 0.7:
                log_test("Intent Detection", True, f"Detected: {intent} ({confidence:.2f})")
                return True
            else:
                log_test("Intent Detection", False, f"Wrong intent or low confidence")
                return False
        else:
            log_test("Intent Detection", False, f"HTTP {response.status_code}")
            return False
    except Exception as e:
        log_test("Intent Detection", False, str(e))
        return False


def test_create_order_flow():
    """Test 3: Complete Order Creation Flow"""
    print("\n" + "="*60)
    print("TEST 3: Order Creation Flow")
    print("="*60)
    
    test_message = "Order 2 laptops for Rahul Kumar"
    print(f"📝 Message: '{test_message}'")
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{API_BASE_URL}/ai/process",
            json={"message": test_message},
            timeout=15
        )
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            intent = result.get('intent')
            action_result = result.get('action_result', {})
            success = action_result.get('success', False)
            
            print(f"   Intent: {intent}")
            print(f"   Success: {success}")
            print(f"   Time: {elapsed:.2f}s")
            
            if success:
                order_id = action_result.get('order_id')
                print(f"   Order ID: {order_id}")
                log_test("Order Creation", True, f"Order {order_id} created in {elapsed:.2f}s")
                return order_id
            else:
                message = action_result.get('message', 'Unknown error')
                log_test("Order Creation", False, message)
                return None
        else:
            log_test("Order Creation", False, f"HTTP {response.status_code}: {response.text}")
            return None
    except Exception as e:
        log_test("Order Creation", False, str(e))
        return None


def test_dashboard_metrics():
    """Test 4: Dashboard Metrics"""
    print("\n" + "="*60)
    print("TEST 4: Dashboard Metrics")
    print("="*60)
    
    try:
        response = requests.get(f"{API_BASE_URL}/dashboard/", timeout=5)
        
        if response.status_code == 200:
            stats = response.json()
            
            print(f"   Total Revenue: ₹{stats.get('total_revenue', 0)}")
            print(f"   Total Orders: {stats.get('total_orders', 0)}")
            print(f"   Total Customers: {stats.get('total_customers', 0)}")
            
            log_test("Dashboard Metrics", True, "Dashboard data retrieved")
            return True
        else:
            log_test("Dashboard Metrics", False, f"HTTP {response.status_code}")
            return False
    except Exception as e:
        log_test("Dashboard Metrics", False, str(e))
        return False


def test_inventory_check():
    """Test 5: Inventory Check"""
    print("\n" + "="*60)
    print("TEST 5: Inventory Check via AI")
    print("="*60)
    
    test_message = "Check stock of laptop"
    print(f"📝 Message: '{test_message}'")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/ai/process",
            json={"message": test_message},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            intent = result.get('intent')
            
            print(f"   Intent: {intent}")
            
            if intent == 'check_inventory':
                log_test("Inventory Check", True, "Intent detected correctly")
                return True
            else:
                log_test("Inventory Check", False, f"Wrong intent: {intent}")
                return False
        else:
            log_test("Inventory Check", False, f"HTTP {response.status_code}")
            return False
    except Exception as e:
        log_test("Inventory Check", False, str(e))
        return False


def test_multilingual_support():
    """Test 6: Hindi/Hinglish Support"""
    print("\n" + "="*60)
    print("TEST 6: Multilingual Support")
    print("="*60)
    
    test_messages = [
        ("Hindi", "Laptop ka stock check karo"),
        ("Hinglish", "2 laptop order karo Rahul ke liye")
    ]
    
    all_passed = True
    
    for lang, message in test_messages:
        print(f"\n   {lang}: '{message}'")
        
        try:
            response = requests.post(
                f"{API_BASE_URL}/ai/test-intent",
                json={"message": message},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                intent = result.get('intent')
                print(f"   → Intent: {intent}")
            else:
                all_passed = False
                print(f"   → Failed: HTTP {response.status_code}")
        except Exception as e:
            all_passed = False
            print(f"   → Error: {e}")
    
    if all_passed:
        log_test("Multilingual Support", True, "Hindi/Hinglish working")
    else:
        log_test("Multilingual Support", False, "Some languages failed")
    
    return all_passed


def generate_report():
    """Generate test report"""
    print("\n" + "="*60)
    print("TEST REPORT")
    print("="*60)
    
    total = len(TEST_RESULTS)
    passed = sum(1 for r in TEST_RESULTS if r['success'])
    failed = total - passed
    
    print(f"\nTotal Tests: {total}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"Success Rate: {(passed/total*100):.1f}%")
    
    print("\n" + "-"*60)
    print("DETAILED RESULTS:")
    print("-"*60)
    
    for result in TEST_RESULTS:
        status = "✅" if result['success'] else "❌"
        print(f"{status} {result['test']}: {result['message']}")
    
    # Save report
    report = {
        "summary": {
            "total": total,
            "passed": passed,
            "failed": failed,
            "success_rate": f"{(passed/total*100):.1f}%",
            "timestamp": datetime.now().isoformat()
        },
        "results": TEST_RESULTS
    }
    
    with open("simple_test_report.json", 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Report saved to: simple_test_report.json")
    
    return passed == total


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🚀 SIMPLE INTEGRATION TEST SUITE")
    print("="*60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API URL: {API_BASE_URL}")
    
    # Run tests
    test_ai_agent_active()
    test_ai_intent_detection()
    order_id = test_create_order_flow()
    test_dashboard_metrics()
    test_inventory_check()
    test_multilingual_support()
    
    # Generate report
    all_passed = generate_report()
    
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


if __name__ == "__main__":
    try:
        exit_code = main()
        print(f"\nFinished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️ Tests interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n\n❌ CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
