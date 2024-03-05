import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", "bold", "example.com")
        node2 = TextNode("This is a text node", "bold", "example.com")
        self.assertEqual(node1, node2)

    def test_not_eq_text(self):
        node1 = TextNode("This is a text node", "bold", "example.com")
        node2 = TextNode("Different text", "bold", "example.com")
        self.assertNotEqual(node1, node2)

    def test_not_eq_text_type(self):
        node1 = TextNode("This is a text node", "bold", "example.com")
        node2 = TextNode("This is a text node", "italic", "example.com")
        self.assertNotEqual(node1, node2)

    def test_not_eq_url(self):
        node1 = TextNode("This is a text node", "bold", "example.com")
        node2 = TextNode("This is a text node", "bold", "different.com")
        self.assertNotEqual(node1, node2)

    def test_repr(self):
        node = TextNode("This is a text node", "bold", "example.com")
        expected_repr = "TextNode('This is a text node', 'bold', 'example.com')"
        self.assertEqual(repr(node), expected_repr)


if __name__ == "__main__":
    unittest.main()
