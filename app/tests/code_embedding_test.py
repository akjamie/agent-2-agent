import unittest
from tree_sitter import Language, Parser
import os

class TestTreeSitterParsing(unittest.TestCase):
    def setUp(self):
        # Path to the manually built shared library
        self.python_so = os.path.join(os.path.dirname(__file__), 'build', 'my-languages.so')
        if not os.path.exists(self.python_so):
            self.skipTest(
                f"Shared library {self.python_so} not found. Please build it using the tree-sitter CLI or tree-sitter-languages.\n"
                "Example: tree-sitter build --languages python --output app/tests/build/my-languages.so"
            )
        self.PY_LANGUAGE = Language(self.python_so, 'python')
        self.parser = Parser()
        self.parser.set_language(self.PY_LANGUAGE)

    def test_parse_python(self):
        code = b"def foo(x):\n    return x + 1\n"
        tree = self.parser.parse(code)
        root_node = tree.root_node
        self.assertEqual(root_node.type, 'module')
        self.assertTrue(any(child.type == 'function_definition' for child in root_node.children))

    def test_parse_groovy_placeholder(self):
        # Tree-sitter Groovy grammar is not available on PyPI.
        # To use it, clone https://github.com/Moonside/tree-sitter-groovy and add its path when building the shared library.
        # Example:
        # tree-sitter build --languages python,groovy --output app/tests/build/my-languages.so
        pass  # Placeholder for Groovy parsing

if __name__ == "__main__":
    unittest.main()
