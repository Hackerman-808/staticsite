import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links

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


# KEEP IN MIND: Malformed Markdown images or links or other formatting errors are IGNORED -UNLESS- NO valid entries are present.
    def test_extract_image_empty_input(self):
        with self.assertRaises(Exception):
            extract_markdown_images("")


    def test_extract_image_mono_input(self):
        image_res = extract_markdown_images(
            "This is text with a ![thing](https://i.imgur.com/cambridge.gif)")
        self.assertEqual(image_res,
                         [("thing", "https://i.imgur.com/cambridge.gif")])


    def test_extract_image_dual_input(self):
        image_res = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertEqual(image_res,
                         [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])


    def test_extract_image_bad_format(self):
        with self.assertRaises(Exception):
            extract_markdown_images(
                "This is text with a ![rick roll(https://i.imgur.com/aKaOqIh.gif)")


    def test_extract_image_bad_and_valid_format(self):
    # As stated above, this is not ideal but the check can't see incorrect syntax on multiple entries when one is correct - 
    # too much work to fix, so leave for now as is.
        image_res = extract_markdown_images(
            "This is text with a ![rick roll(https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertEqual(image_res,
                         [("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])


    def test_extract_image_bad_and_bad_format(self):
        with self.assertRaises(Exception):
            extract_markdown_images(
                "This is text with a ![rick roll(https://i.imgur.com/aKaOqIh.gif) and ![obi wan]https://i.imgur.com/fJRm4Vk.jpeg)")


    def test_extract_image_empty_partial(self):
        with self.assertRaises(Exception):
            extract_markdown_images(
                "This is text with a ![](https://i.imgur.com/aKaOqIh.gif)")


    def test_extract_link_empty_input(self):
        with self.assertRaises(Exception):
            extract_markdown_links("")


    def test_extract_link_mono_input(self):
        link_res = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)")
        self.assertEqual(link_res,
                         [("to boot dev", "https://www.boot.dev")])


    def test_extract_link_dual_input(self):
        link_res = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertEqual(link_res,
                         [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_extract_link_bad_format(self):
        with self.assertRaises(Exception):
            extract_markdown_links(
                "This is text with a link to boot dev](https://www.boot.dev)")


    def test_extract_link_bad_and_valid_format(self):
    # As stated above, this is not ideal but the check can't see incorrect syntax on multiple entries when one is correct - 
    # too much work to fix, so leave for now as is.
        link_res = extract_markdown_links(
            "This is text with a link [to boot dev https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertEqual(link_res,
                         [("to youtube", "https://www.youtube.com/@bootdotdev")])


    def test_extract_link_bad_and_bad_format(self):
        with self.assertRaises(Exception):
            extract_markdown_links(
                "This is text with a link [to boot dev https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev")


    def test_extract_link_empty_partial(self):
        with self.assertRaises(Exception):
            extract_markdown_links(
                "This is a link [](https://www.youtube.com/@bootdotdev)")
            

if __name__ == "__main__":
    unittest.main()
