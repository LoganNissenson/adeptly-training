import os
import shutil
import sys

def cleanup_tests():
    """
    Clean up all test-related files and directories that might cause import issues.
    """
    # Base path for the adeptly app
    base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'adeptly')
    
    # Path to the tests directory
    tests_dir = os.path.join(base_path, 'tests')
    
    # Path to __pycache__ directories
    pycache_dirs = [
        os.path.join(base_path, '__pycache__'),
        os.path.join(tests_dir, '__pycache__') if os.path.exists(tests_dir) else None
    ]
    
    # Remove the tests directory if it exists
    if os.path.exists(tests_dir):
        print(f"Removing tests directory: {tests_dir}")
        shutil.rmtree(tests_dir)
    
    # Remove __pycache__ directories
    for cache_dir in pycache_dirs:
        if cache_dir and os.path.exists(cache_dir):
            print(f"Removing cache directory: {cache_dir}")
            shutil.rmtree(cache_dir)
    
    # Remove any .pyc files in the main directory that might be cached
    for file in os.listdir(base_path):
        if file.endswith('.pyc') and 'test' in file.lower():
            file_path = os.path.join(base_path, file)
            print(f"Removing cached file: {file_path}")
            os.remove(file_path)
    
    print("Cleanup complete!")

if __name__ == '__main__':
    cleanup_tests()
