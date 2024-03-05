import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_init(self):
        node = HTMLNode(tag='div', value='Hello', children=[], props={'class': 'test'})
        self.assertEqual(node.tag, 'div')
        self.assertEqual(node.value, 'Hello')
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {'class': 'test'})

        node_default = HTMLNode()
        self.assertIsNone(node_default.tag)
        self.assertIsNone(node_default.value)
        self.assertEqual(node_default.children, [])
        self.assertEqual(node_default.props, {})

    def test_props_to_html(self):
        node = HTMLNode(tag='div', props={'class': 'test', 'id': 'my-div'})
        expected_output = ' class="test" id="my-div"'
        self.assertEqual(node.props_to_html(), expected_output)

    def test_repr(self):
        child1 = HTMLNode(tag='p', value='Child 1')
        child2 = HTMLNode(tag='p', value='Child 2')
        parent = HTMLNode(tag='div', children=[child1, child2], props={'class': 'parent'})
        expected_output = 'this is a html node: div | None | p, p |  class="parent"'
        self.assertEqual(repr(parent), expected_output)

        node_no_children = HTMLNode(tag='p', value='No children')
        expected_output_no_children = 'this is a html node: p | No children |  | '
        self.assertEqual(repr(node_no_children), expected_output_no_children)

    def test_to_html_not_implemented(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

class TestLeafNode(unittest.TestCase):
    def test_init_valid(self):
        node = LeafNode(tag='p', value='Hello', props={'class': 'text'})
        self.assertEqual(node.tag, 'p')
        self.assertEqual(node.value, 'Hello')
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {'class': 'text'})

    def test_init_missing_value(self):
        node = LeafNode(tag='p', value=None, props={'class': 'text'})
        self.assertIsNone(node.value)

    def test_props_to_html_with_tag(self):
        node = LeafNode(tag='p', value='Hello', props={'class': 'text'})
        expected_output = ' class="text"'
        self.assertEqual(node.props_to_html(), expected_output)

    def test_props_to_html_without_tag(self):
        node = LeafNode(value='Hello')
        expected_output = 'Hello'
        self.assertEqual(node.props_to_html(), expected_output)

    def test_to_html_with_tag(self):
        node = LeafNode(tag='p', value='Hello', props={'class': 'text'})
        expected_output = '<p class="text">Hello</p>'
        self.assertEqual(node.to_html(), expected_output)

    def test_to_html_without_tag(self):
        node = LeafNode(value='Hello')
        expected_output = 'Hello'
        self.assertEqual(node.to_html(), expected_output)

    def test_to_html_missing_value(self):
        node = LeafNode(tag='p', value=None, props={'class': 'text'})
        with self.assertRaises(ValueError):
            node.to_html()

    def test_repr(self):
        node = LeafNode(tag='p', value='Hello', props={'class': 'text'})
        expected_output = "LeafNode(tag=p, value=Hello, props= class=\"text\")"
        self.assertEqual(repr(node), expected_output)

class TestParentNode(unittest.TestCase):
    def test_init_valid(self):
        child1 = LeafNode(tag='p', value='Child 1')
        child2 = LeafNode(tag='p', value='Child 2')
        node = ParentNode(tag='div', children=[child1, child2], props={'class': 'parent'})
        self.assertEqual(node.tag, 'div')
        self.assertIsNone(node.value)
        self.assertEqual(node.children, [child1, child2])
        self.assertEqual(node.props, {'class': 'parent'})

    def test_init_missing_tag(self):
        child = LeafNode(tag='p', value='Child')
        node = ParentNode(children=[child], props={'class': 'parent'})
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertEqual(node.children, [child])
        self.assertEqual(node.props, {'class': 'parent'})

    def test_init_missing_children(self):
        node = ParentNode(tag='div', props={'class': 'parent'})
        self.assertEqual(node.tag, 'div')
        self.assertIsNone(node.value)
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {'class': 'parent'})

    def test_to_html_with_tag_and_children(self):
        child1 = LeafNode(tag='p', value='Child 1')
        child2 = LeafNode(tag='p', value='Child 2')
        parent = ParentNode(tag='div', children=[child1, child2], props={'class': 'parent'})
        expected_output = '<div class="parent"><p>Child 1</p><p>Child 2</p></div>'
        self.assertEqual(parent.to_html(), expected_output)

    def test_to_html_missing_tag(self):
        child = LeafNode(tag='p', value='Child')
        parent = ParentNode(children=[child], props={'class': 'parent'})
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_to_html_missing_children(self):
        parent = ParentNode(tag='div', props={'class': 'parent'})
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_to_html_nested_nodes(self):
        leaf1 = LeafNode(tag='p', value='Leaf 1')
        leaf2 = LeafNode(tag='p', value='Leaf 2')
        parent1 = ParentNode(tag='div', children=[leaf1], props={'class': 'child'})
        parent2 = ParentNode(tag='div', children=[parent1, leaf2], props={'class': 'parent'})
        expected_output = '<div class="parent"><div class="child"><p>Leaf 1</p></div><p>Leaf 2</p></div>'
        self.assertEqual(parent2.to_html(), expected_output)


if __name__ == '__main__':
    unittest.main()
