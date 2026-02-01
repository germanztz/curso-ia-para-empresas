# test/test_bash_operations.py
import unittest
import subprocess
from tools import bash_operations

class TestBashOperations(unittest.TestCase):
    
    def test_execute_bash_success(self):
        result = bash_operations.execute_bash.invoke(input={'command':"echo hello"})
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "hello\n")
        self.assertEqual(result.stderr, "")
    
    def test_execute_bash_error(self):
        result = bash_operations.execute_bash.invoke(input={'command':"ls /nonexistent"})
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, '')
        self.assertEqual(result.stderr, "ls: cannot access '/nonexistent': No such file or directory\n")
    
    def test_execute_bash_timeout(self):
        try:
            result = bash_operations.execute_bash.invoke(input={'command':"sleep 5", 'timeout':'1'})
        except Exception as e:
            self.assertEqual(str(e), "Command 'sleep 5' timed out after 1 seconds")
    
    
    def test_check_port_open_failure(self):
        result = bash_operations.check_port_open.invoke(input={'host':"localhost", 'port':9999})
        self.assertEqual(result.returncode, 1)

if __name__ == '__main__':
    unittest.main()