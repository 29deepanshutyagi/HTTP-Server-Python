import requests

# Test for root endpoint
def test_root():
    response = requests.get("http://localhost:4221/")
    assert response.status_code == 200
    print("Root test passed.")

# Test for echo endpoint with gzip
def test_echo():
    response = requests.get("http://localhost:4221/echo/HelloWorld")
    assert response.status_code == 200
    assert response.text == "HelloWorld"
    print("Echo test passed.")

# Test for user-agent endpoint
def test_user_agent():
    headers = {'User-Agent': 'TestAgent/1.0'}
    response = requests.get("http://localhost:4221/user-agent", headers=headers)
    assert response.status_code == 200
    assert response.text == 'TestAgent/1.0'
    print("User-Agent test passed.")

# Test for file GET request
def test_file_get():
    with open('testfile.txt', 'w') as f:
        f.write("Test content for file")
    response = requests.get("http://localhost:4221/files/testfile.txt")
    assert response.status_code == 200
    assert response.text == "Test content for file"
    print("File GET test passed.")

# Test for file POST request
def test_file_post():
    response = requests.post("http://localhost:4221/files/testfile.txt", data="New file content")
    assert response.status_code == 201
    print("File POST test passed.")

# Run all tests
def run_tests():
    test_root()
    test_echo()
    test_user_agent()
    test_file_get()
    test_file_post()

if __name__ == "__main__":
    run_tests()
