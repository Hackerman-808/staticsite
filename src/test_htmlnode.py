import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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


    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


    def test_to_html_with_grandchildren_props(self):
        grandchild_node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            '<div><span><a href="https://www.google.com">Click me!</a></span></div>',
        )    


    def test_to_html_without_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()


    def test_to_html_with_empty_children(self):
        parent_node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            parent_node.to_html()


    def test_to_html_without_tag(self):
        child_node = LeafNode("b", "Hello, world!")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()


    def test_to_html_without_children_or_tag(self):
        child_node = LeafNode(None, None)
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()


    def test_to_html_many_children_props(self):
        child_node_1 = LeafNode("b", "Is this working?")
        child_node_2 = LeafNode("a", "No, it is not!")
        child_node_3 = LeafNode("c", "Hey Guys, this link does work.", {"href": "https://www.google.com"})
        parent_node = ParentNode("span", [child_node_1, child_node_2, child_node_3])
        self.assertEqual(
            parent_node.to_html(),
            '<span><b>Is this working?</b><a>No, it is not!</a><c href="https://www.google.com">Hey Guys, this link does work.</c></span>',
        )    


if __name__ == "__main__":
    unittest.main()
