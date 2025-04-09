import unittest

from textnode import TextNode, TextType

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


if __name__ == "__main__":
    unittest.main()
