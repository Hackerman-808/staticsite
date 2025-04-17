import unittest

from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq_text_type_url_as_none(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)


    def test_eq_text_type_url(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.fudge.com")
        node2 = TextNode("This is a link node", TextType.LINK, "https://www.fudge.com")
        self.assertEqual(node, node2)


    def test_noteq_diff_type(self):
        node = TextNode("This is an image node", TextType.TEXT, "https://www.fudge.com/images/")
        node2 = TextNode("This is an image node", TextType.IMAGE, "https://www.fudge.com/images/")
        self.assertNotEqual(node, node2)
    

    def test_noteq_diff_url(self):
        node = TextNode("This is an image node", TextType.IMAGE, "https://www.fudge.com/pics/shucks.jpg")
        node2 = TextNode("This is an image node", TextType.IMAGE, "https://www.fudge.com/images/glob.jpg")
        self.assertNotEqual(node, node2)


    def test_noteq_diff_text_url(self):
        node = TextNode("`print('Jokes on YOU!')`", TextType.CODE, "https://www.fudge.com/snippets/joke.py")
        node2 = TextNode("`print('Jokes on ME!')`", TextType.CODE, "https://www.fudge.com/snippets/joke_me.py")
        self.assertNotEqual(node, node2)


    def test_noteq_diff_text_type_url(self):
        node = TextNode("Framble.", TextType.TEXT)
        node2 = TextNode("_HORBLE!_", TextType.ITALIC, "https://www.fudge.com/images/grmble.txt")
        self.assertNotEqual(node, node2)


    def test_text_to_html(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


    def test_bold_to_html(self):
        node = TextNode("This is bold text.", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text.")


    def test_italic_to_html(self):
        node = TextNode("This is italic text.", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text.")


    def test_code_to_html(self):
        node = TextNode("This is code.", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is code.")


    def test_link_to_html(self):
        node = TextNode("This is anchor text.", TextType.LINK, "https://www.dumbinfo.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is anchor text.")
        self.assertEqual(html_node.props, {"href": "https://www.dumbinfo.com"})

    def test_image_to_html(self):
        node = TextNode("This is an alt text node", TextType.IMAGE, "https://www.blandimage.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://www.blandimage.com", "alt": "This is an alt text node"})


    def test_invalid_to_html(self):
        node = TextNode("This is an invalid text type!", "Garbage.")
        with self.assertRaises(Exception):
            text_node_to_html_node(node)


if __name__ == "__main__":
    unittest.main()
