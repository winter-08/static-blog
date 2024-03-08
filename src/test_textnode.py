import unittest

from textnode import (
    TextNode,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_node_to_html_node,
)


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


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_bold(self):
        old_nodes = [TextNode("Hello **world**", "text")]
        split_nodes = split_nodes_delimiter(old_nodes, "**", "bold")
        expected_nodes = [TextNode("Hello ", "text"), TextNode("world", "bold")]
        self.assertEqual(split_nodes, expected_nodes)

    def test_split_nodes_delimiter_italic(self):
        old_nodes = [TextNode("Hello *world*", "text")]
        split_nodes = split_nodes_delimiter(old_nodes, "*", "italic")
        expected_nodes = [TextNode("Hello ", "text"), TextNode("world", "italic")]
        self.assertEqual(split_nodes, expected_nodes)

    def test_split_nodes_delimiter_code(self):
        old_nodes = [TextNode("Hello `world`", "text")]
        split_nodes = split_nodes_delimiter(old_nodes, "`", "code")
        expected_nodes = [TextNode("Hello ", "text"), TextNode("world", "code")]
        self.assertEqual(split_nodes, expected_nodes)

    def test_split_nodes_no_delimiter(self):
        old_nodes = [TextNode("Hello world", "text")]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(old_nodes, "**", "bold")

    def test_split_nodes_no_closing_delimiter(self):
        old_nodes = [TextNode("Hello **world", "text")]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(old_nodes, "**", "bold")


class TestExtractMarkdownImages(unittest.TestCase):
    def test_single_image(self):
        text = "This is a ![sample](image.jpg) image."
        expected_output = [("sample", "image.jpg")]
        self.assertEqual(extract_markdown_images(text), expected_output)

    def test_multiple_images(self):
        text = "Here are two images: ![image1](path/to/image1.jpg) and ![image2](path/to/image2.gif)."
        expected_output = [
            ("image1", "path/to/image1.jpg"),
            ("image2", "path/to/image2.gif"),
        ]
        self.assertEqual(extract_markdown_images(text), expected_output)

    def test_no_images(self):
        text = "This text does not contain any images."
        expected_output = []
        self.assertEqual(extract_markdown_images(text), expected_output)

    def test_empty_string(self):
        text = ""
        expected_output = []
        self.assertEqual(extract_markdown_images(text), expected_output)

    def test_image_without_link(self):
        text = "This is an image without a link: ![image]."
        expected_output = []
        self.assertEqual(extract_markdown_images(text), expected_output)

    def test_link_without_image(self):
        text = "This is a link without an image: [link](https://example.com)."
        expected_output = []
        self.assertEqual(extract_markdown_images(text), expected_output)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_multiple_links(self):
        text = "Visit [OpenAI](https://openai.com) and [GitHub](https://github.com)."
        expected_output = [
            ("OpenAI", "https://openai.com"),
            ("GitHub", "https://github.com"),
        ]
        self.assertEqual(extract_markdown_links(text), expected_output)

    def test_link_with_spaces(self):
        text = "This is a [link with spaces](https://example.com/link with spaces)."
        expected_output = [("link with spaces", "https://example.com/link with spaces")]
        self.assertEqual(extract_markdown_links(text), expected_output)

    def test_no_links(self):
        text = "No links in this text."
        expected_output = []
        self.assertEqual(extract_markdown_links(text), expected_output)


class TestSplitNodesImage(unittest.TestCase):
    def test_single_image(self):
        old_nodes = [TextNode("This is an ![image](image.jpg)", "text")]
        expected_output = [TextNode("image", "image", "image.jpg")]
        self.assertEqual(split_nodes_image(old_nodes), expected_output)

    def test_multiple_images(self):
        old_nodes = [
            TextNode("![image1](image1.png) and ![image2](image2.gif)", "text")
        ]
        expected_output = [
            TextNode("image1", "image", "image1.png"),
            TextNode("image2", "image", "image2.gif"),
        ]
        self.assertEqual(split_nodes_image(old_nodes), expected_output)

    def test_no_images(self):
        old_nodes = [TextNode("This text has no images", "text")]
        expected_output = [TextNode("This text has no images", "text")]
        self.assertEqual(split_nodes_image(old_nodes), expected_output)

    def test_empty_text(self):
        old_nodes = [TextNode("", "text")]
        expected_output = []
        self.assertEqual(split_nodes_image(old_nodes), expected_output)


class TestSplitNodesLink(unittest.TestCase):
    def test_single_link(self):
        old_nodes = [TextNode("Visit [OpenAI](https://openai.com)", "text")]
        expected_output = [TextNode("OpenAI", "link", "https://openai.com")]
        self.assertEqual(split_nodes_link(old_nodes), expected_output)

    def test_multiple_links(self):
        old_nodes = [
            TextNode(
                "Visit [OpenAI](https://openai.com) and [GitHub](https://github.com)",
                "text",
            )
        ]
        expected_output = [
            TextNode("OpenAI", "link", "https://openai.com"),
            TextNode("GitHub", "link", "https://github.com"),
        ]
        self.assertEqual(split_nodes_link(old_nodes), expected_output)

    def test_no_links(self):
        old_nodes = [TextNode("This text has no links", "text")]
        expected_output = [TextNode("This text has no links", "text")]
        self.assertEqual(split_nodes_link(old_nodes), expected_output)

    def test_empty_text(self):
        old_nodes = [TextNode("", "text")]
        expected_output = []
        self.assertEqual(split_nodes_link(old_nodes), expected_output)


if __name__ == "__main__":
    unittest.main()
