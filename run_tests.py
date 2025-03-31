import os
import subprocess
import sys
from cleanup_tests import cleanup_tests

def run_tests():
    """
    Clean up test files and then run Django tests
    """
    print("===== Cleaning up test files =====")
    cleanup_tests()
    
    print("\n===== Running Django tests =====")
    # Run Django tests using the manage.py command
    result = subprocess.run([sys.executable, 'manage.py', 'test', 'adeptly'], 
                            capture_output=True, 
                            text=True)
    
    # Print the output
    print(result.stdout)
    
    if result.stderr:
        print("Errors:")
        print(result.stderr)
    
    return result.returncode

if __name__ == '__main__':
    sys.exit(run_tests())
