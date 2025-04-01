from tools import get_subnet, get_reversed_mask

def test_get_subnet():
    print("Testing get_subnet...")
    assert get_subnet("192.168.2.1/8") == "192.0.0.0", "Test case 1 failed"
    assert get_subnet("10.0.0.1/16") == "10.0.0.0", "Test case 2 failed"
    assert get_subnet("172.16.5.4/24") == "172.16.5.0", "Test case 3 failed"
    print("get_subnet passed all test cases!")

def test_get_reversed_mask():
    print("Testing get_reversed_mask...")
    assert get_reversed_mask("192.168.2.1/8") == "0.255.255.255", "Test case 1 failed"
    assert get_reversed_mask("10.0.0.1/16") == "0.0.255.255", "Test case 2 failed"
    assert get_reversed_mask("172.16.5.4/24") == "0.0.0.255", "Test case 3 failed"
    print("get_reversed_mask passed all test cases!")

if __name__ == "__main__":
    test_get_subnet()
    test_get_reversed_mask()
    print("All tests completed successfully!")
