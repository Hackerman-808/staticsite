import unittest

from htmlnode import HTMLNode

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


if __name__ == "__main__":
    unittest.main()
