from enum import Enum
from htmlnode import LeafNode
import re

class TextType(Enum):
	TEXT = "text"
	BOLD = "bold"
	ITALIC = "italic"
	CODE = "code"
	LINK = "link"
	IMAGE = "image"


class TextNode:
	def __init__(self, text, text_type, url=None):
		self.text = text
		self.text_type = text_type
		self.url = url


	def __eq__(self, other):
		return (self.text == other.text 
		  and self.text_type == other.text_type 
		  and self.url == other.url)


	def __repr__(self):
		url_part = f', "{self.url}"' if self.url is not None else ""
		return f'TextNode("{self.text}", {self.text_type}{url_part})'


def text_node_to_html_node(text_node):
	if not isinstance(text_node.text_type, TextType):
		raise Exception("No valid text type provided.")
	else:
		match text_node.text_type:
			case TextType.TEXT:
				return LeafNode(None, text_node.text)
			case TextType.BOLD:
				return LeafNode("b", text_node.text)
			case TextType.ITALIC:
				return LeafNode("i", text_node.text)
			case TextType.CODE:
				return LeafNode("code", text_node.text)
			case TextType.LINK:
				return LeafNode("a", text_node.text, {"href": text_node.url})
			case TextType.IMAGE:
				return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})


def split_nodes_delimiter(old_nodes, delimiter, text_type):
# Note: This function assumes that appropriate delimiters are used for the given text_type.
# It doesn't validate the semantic correctness of delimiter/text_type pairs.
	if not delimiter:
		raise Exception("No delimiter provided.")
	if not isinstance(text_type, TextType):
		raise Exception("No valid text type provided.")
	new_nodes = []
	
	for node in old_nodes:
		if not isinstance(node.text_type, TextType):
			raise Exception("No valid text type provided.")
		elif node.text_type != TextType.TEXT:
			new_nodes.append(node) 
		elif delimiter not in node.text:
			new_nodes.append(node)
		elif node.text.count(delimiter) % 2 != 0:
			raise Exception("There are unclosed delimiters present. Please verify correct format.")
		else:
			split_node = node.text.split(delimiter)

			for entry in split_node:
				if entry[0].isspace() or entry[-1].isspace():
					new_nodes.append(TextNode(entry, TextType.TEXT))
				elif not entry[0].isspace() and entry[-1].isspace():
					new_nodes.append(TextNode(entry, text_type))
	return new_nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if not delimiter:
        raise Exception("No delimiter provided.")
    if not isinstance(text_type, TextType):
        raise Exception("No valid text type provided.")
    new_nodes = []
    
    for node in old_nodes:
        if not isinstance(node.text_type, TextType):
            raise Exception("No valid text type provided.")
        elif node.text_type != TextType.TEXT:
            new_nodes.append(node)
        elif delimiter not in node.text:
            new_nodes.append(node)
        elif node.text.count(delimiter) % 2 != 0:
            raise Exception("There are unclosed delimiters present. Please verify correct format.")
        else:
            # Only reach here if it's a TEXT node with properly paired delimiters
            split_node = node.text.split(delimiter)
            
            for i, entry in enumerate(split_node):
                # Handle empty strings that can occur from splitting
                if not entry:
                    continue
                # Even indexes are normal text, odd indexes are special text (between delimiters)
                if i % 2 == 0:
                    new_nodes.append(TextNode(entry, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(entry, text_type))
                
    return new_nodes


def extract_markdown_images(text):
	pass
