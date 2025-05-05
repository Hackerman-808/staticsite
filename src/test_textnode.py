import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter

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


    def test_split_nodes_delimiter_empty_delim(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "", TextType.CODE)


    def test_split_nodes_delimiter_no_delim_in_text(self):
        node = TextNode("This is text with no code block word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with no code block word", TextType.TEXT)])


    def test_split_nodes_delimiter_unclosed_delim(self):
        node = TextNode("This is text with an **unclosed delimiter!", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)


    def test_split_nodes_delimiter_non_text_node(self):
        node = TextNode("`This is code with no text block.`", TextType.CODE)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("`This is code with no text block.`", TextType.CODE)])


    def test_split_nodes_delimiter_incorrect_type_input(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "~", "FLUBBER")


    def test_split_nodes_delimiter_incorrect_node_type(self):
        with self.assertRaises(Exception):
            split_nodes_delimiter([TextNode("This is text with a `code block` word", "FLUBBER")],
                                  "`", TextType.CODE)


    def test_split_nodes_delimiter_empty_list(self):
        self.assertEqual(split_nodes_delimiter([], "`", TextType.CODE,), [])


    def test_split_nodes_delimiter_one_node(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT),
                                     TextNode("code block", TextType.CODE),
                                     TextNode(" word", TextType.TEXT),])


    def test_split_nodes_delimiter_multi_nodes(self):
        nodes = [TextNode("This is text with a `code block` word", TextType.TEXT), 
                TextNode("And this is text with a `code block` word", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT),
                                     TextNode("code block", TextType.CODE),
                                     TextNode(" word", TextType.TEXT), 
                                     TextNode("And this is text with a ", TextType.TEXT),
                                     TextNode("code block", TextType.CODE),
                                     TextNode(" word", TextType.TEXT)])
    

    def test_split_nodes_delimiter_multi_delims_in_node(self):
        node = TextNode("Text `code` more text `more code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("Text ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" more text ", TextType.TEXT),
            TextNode("more code", TextType.CODE)])


if __name__ == "__main__":
    unittest.main()
