import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):

    def test_initialization(self):
        node = HTMLNode(tag='div', value='Hello, World!', children=None, props={'class': 'my-class'})
        self.assertEqual(node.tag, 'div')
        self.assertEqual(node.value, 'Hello, World!')
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {'class': 'my-class'})

    def test_props_to_html(self):
        node = HTMLNode(props={'class': 'test', 'id': 'unique'})
        self.assertEqual(node.props_to_html(), ' class="test" id="unique"')

    def test_repr(self):
        node = HTMLNode('span', 'Example', None, {'style': 'color: red;'})
        expected_repr = "HTMLNode(span, Example, children: None, {'style': 'color: red;'})"
        self.assertEqual(repr(node), expected_repr)


class TestLeafNode(unittest.TestCase):

    def test_initialization_and_repr(self):
        leaf = LeafNode(tag='p', value='This is a paragraph.', props={'class': 'text'})
        expected_repr = "LeafNode(p, This is a paragraph., {'class': 'text'})"
        self.assertEqual(repr(leaf), expected_repr)

    def test_to_html_with_tag_and_props(self):
        leaf = LeafNode('p', 'This is a paragraph.', {'class': 'text'})
        self.assertEqual(leaf.to_html(), '<p class="text">This is a paragraph.</p>')

    def test_to_html_without_props(self):
        leaf = LeafNode('span', 'A span element')
        self.assertEqual(leaf.to_html(), '<span>A span element</span>')

    def test_to_html_with_none_tag_raises_error(self):
        leaf = LeafNode(tag=None, value='Just some text.')
        self.assertEqual(leaf.to_html(), 'Just some text.')

    def test_to_html_with_none_value_raises_error(self):
        leaf = LeafNode(tag='p', value=None, props={'class': 'text'})
        with self.assertRaises(ValueError):
            leaf.to_html()


class TestParentNode(unittest.TestCase):
    
    def test_initialization_and_repr(self):
        parent = ParentNode(tag='div', children=[], props={'class': 'container'})
        self.assertEqual(repr(parent), "ParentNode(div, children: [], {'class': 'container'})")

    def test_to_html_single_child(self):
        child = LeafNode(tag='p', value='Paragraph inside div')
        parent = ParentNode(tag='div', children=[child], props={'class': 'container'})
        self.assertEqual(parent.to_html(), '<div class="container"><p>Paragraph inside div</p></div>')

    def test_to_html_multiple_children(self):
        children = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ]
        parent = ParentNode(tag='p', children=children)
        expected_html = '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
        self.assertEqual(parent.to_html(), expected_html)

    def test_to_html_nested_structure(self):
        grandchild = LeafNode(tag='span', value='A span inside a paragraph.')
        child = ParentNode(tag='p', children=[grandchild])
        parent = ParentNode(tag='div', children=[child], props={'class': 'nested'})
        expected_html = '<div class="nested"><p><span>A span inside a paragraph.</span></p></div>'
        self.assertEqual(parent.to_html(), expected_html)

    def test_to_html_with_empty_children_list(self):
        parent = ParentNode(tag='div', children=[])
        self.assertEqual(parent.to_html(), '<div></div>')

    def test_to_html_with_none_tag_raises_error(self):
        parent = ParentNode(tag=None, children=[LeafNode(tag='p', value='This should fail')])
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_to_html_with_none_children_raises_error(self):
        parent = ParentNode(tag='div', children=None)
        with self.assertRaises(ValueError):
            parent.to_html()


if __name__ == '__main__':
    unittest.main()
