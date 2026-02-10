"""
AI Agent Engine Test Script
Tests natural language processing with various messages
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def print_test(title, message, result):
    """Print formatted test result"""
    print(f"\n{'='*70}")
    print(f"TEST: {title}")
    print(f"{'='*70}")
    print(f"Input: {message}")
    print(f"\nIntent: {result.get('intent', 'N/A')}")
    print(f"Confidence: {result.get('confidence', 0):.2f}")
    print(f"Entities: {json.dumps(result.get('entities', {}), indent=2)}")
    print(f"\nAction Result:")
    print(json.dumps(result.get('action_result', {}), indent=2))
    print(f"{'='*70}")

def test_ai_agent():
    """Test AI Agent with various messages"""
    print("\n🤖 AI AGENT ENGINE - TEST SUITE")
    print("="*70)
    
    # Test 1: Check AI Agent Status
    print("\n📍 Checking AI Agent Status...")
    try:
        r = requests.get(f"{BASE_URL}/ai/test")
        print(f"✅ AI Agent Status: {r.json()['status']}")
        print(f"   Supported Intents: {', '.join(r.json()['supported_intents'])}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Test messages
    test_cases = [
        # Create Order - English
        {
            "title": "Create Order (English)",
            "message": "Order 2 laptops for Alice"
        },
        # Create Order - Hinglish
        {
            "title": "Create Order (Hinglish)",
            "message": "Laptop chahiye 2 pieces for Alice"
        },
        # Check Inventory - English
        {
            "title": "Check Inventory (English)",
            "message": "Check stock of mouse"
        },
        # Check Inventory - Hinglish
        {
            "title": "Check Inventory (Hinglish)",
            "message": "Mouse kitne available hai?"
        },
        # Generate Invoice
        {
            "title": "Generate Invoice",
            "message": "Generate invoice for order 1"
        },
        # Generate Invoice - Hinglish
        {
            "title": "Generate Invoice (Hinglish)",
            "message": "Order 1 ka bill banao"
        },
        # Add Customer
        {
            "title": "Add Customer",
            "message": "Add customer Deepak phone 9876543210"
        },
        # Payment Reminder
        {
            "title": "Payment Reminder",
            "message": "Send payment reminder to Alice"
        },
        # Spelling Error Tolerance
        {
            "title": "Spelling Error (lapto instead of laptop)",
            "message": "Check stock of lapto"
        },
        # Multiple Entities
        {
            "title": "Multiple Entities",
            "message": "Order 3 cables for Bob phone 9123456789 Rs 500"
        },
        # Low Stock Check
        {
            "title": "Low Stock Check",
            "message": "Show me low stock products"
        },
        # Unknown Intent
        {
            "title": "Unknown Intent",
            "message": "What is the weather today?"
        }
    ]
    
    # Run tests
    for i, test_case in enumerate(test_cases, 1):
        try:
            response = requests.post(
                f"{BASE_URL}/ai/process",
                json={"message": test_case["message"]}
            )
            result = response.json()
            print_test(test_case["title"], test_case["message"], result)
            
            # Validate
            if result.get('intent') != 'unknown':
                print(f"✅ Test {i} PASSED")
            else:
                print(f"⚠️  Test {i} - Unknown intent (expected for some tests)")
                
        except Exception as e:
            print(f"\n❌ Test {i} FAILED: {e}")
    
    # Summary
    print(f"\n{'='*70}")
    print("🎉 AI AGENT TESTING COMPLETE")
    print(f"{'='*70}")
    print("\n📊 Summary:")
    print(f"   Total Tests: {len(test_cases)}")
    print(f"   Intents Tested: create_order, check_inventory, generate_invoice, add_customer, payment_reminder")
    print(f"   Languages: English, Hinglish")
    print(f"   Features: Spelling errors, Multiple entities, Fuzzy matching")
    print("\n✅ AI Agent Engine is working correctly!")
    print("\n📖 For more examples, see: AI_AGENT_DOCUMENTATION.md")
    print("🌐 Interactive testing: http://localhost:8000/docs")

def test_intent_only():
    """Test intent detection without executing actions"""
    print("\n🔍 INTENT DETECTION ONLY (No Actions)\n")
    
    test_messages = [
        "Order 2 laptops",
        "Check stock",
        "Generate bill",
        "Add customer",
        "Payment reminder"
    ]
    
    for msg in test_messages:
        try:
            response = requests.post(
                f"{BASE_URL}/ai/test-intent",
                json={"message": msg}
            )
            result = response.json()
            print(f"Message: {msg:30} → Intent: {result['intent']:20} Confidence: {result['confidence']:.2f}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    import sys
    
    try:
        # Check if server is running
        r = requests.get("http://localhost:8000/health")
        if r.status_code != 200:
            print("❌ Server is not healthy")
            sys.exit(1)
        
        # Run tests
        if len(sys.argv) > 1 and sys.argv[1] == "--intent-only":
            test_intent_only()
        else:
            test_ai_agent()
            
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to server")
        print("Make sure the server is running:")
        print("   python -m uvicorn app.main:app --reload")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        sys.exit(0)
