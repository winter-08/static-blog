import unittest

from html_markdown import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_single_block(self):
        self.assertEqual(markdown_to_blocks("Hello, world!"), ["Hello, world!"])

    def test_multiple_blocks(self):
        text = """Block 1
        Block 2
        Block 3"""
        expected_output = ["Block 1", "Block 2", "Block 3"]
        self.assertEqual(markdown_to_blocks(text), expected_output)

    def test_blocks_with_whitespace(self):
        text = """
            Block 1   
        Block 2    
            Block 3    
        """
        expected_output = ["Block 1", "Block 2", "Block 3"]
        self.assertEqual(markdown_to_blocks(text), expected_output)

    def test_blocks_with_empty_lines(self):
        text = """
        Block 1

        Block 2

        Block 3
        """
        expected_output = ["Block 1", "Block 2", "Block 3"]
        self.assertEqual(markdown_to_blocks(text), expected_output)

    def test_mixed_blocks(self):
        text = """
        Block 1
            Block 2   

        Block 3    
        """
        expected_output = ["Block 1", "Block 2", "Block 3"]
        self.assertEqual(markdown_to_blocks(text), expected_output)


if __name__ == "__main__":
    unittest.main()
