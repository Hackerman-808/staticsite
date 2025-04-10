import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_1(self):
        node = HTMLNode("I", "Don't", "Know", {"<what>": "https://www.to.com",
                                                "put": "_here!"})
        self.assertEqual(node.props_to_html(), ' <what>="https://www.to.com" put="_here!"')
    

    def test_props_to_html_2(self):
        node = HTMLNode("Bug", "...", "grand", {"why": "for what", 
                                                "Please": "let it end?"})
        self.assertEqual(node.props_to_html(), ' why="for what" Please="let it end?"')
    

    def test_repr(self):
        node = HTMLNode(None, 5, "know", {"<what>": "https://www.to.com", 
                                          "put": "_here!"})
        self.assertEqual(node.__repr__(), "HTMLNode(None, 5, know, {'<what>': 'https://www.to.com', 'put': '_here!'})")


    def test_leaf_to_html_tag_as_none_value(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")


    def test_leaf_to_html_tag_value_as_none(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()


    def test_leaf_to_html_tag_value(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")


    def test_leaf_to_html_tag_value_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')


if __name__ == "__main__":
    unittest.main()
