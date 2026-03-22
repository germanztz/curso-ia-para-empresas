import os
from odf import opendocument, teletype
from odf.text import P, Span
from odf.style import Style, TextProperties

class OdtDocument:

    def __init__(self, file_path):
        self.file_path = file_path
        self.document = self.load(file_path)
    
    def load(self, file_path):
        """
        Open an ODT file and return the loaded document object.
        """
        return opendocument.load(file_path)

    def save(self, file_path = None):
        """
        Save the document to a file.
        """
        if (file_path == None):
            file_path = self.file_path
        
        # Create the file if it doesn't exist
        if not os.path.exists(file_path):
            # Create parent directories if they don't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            # Create empty file
            with open(file_path, 'w') as f:
                pass
        
        self.document.save(file_path)
        print(f"Document saved to {file_path}")

    def _traverse(self, index, node, callback) -> int:
        """
        Iterates between the tree and calls the callback function on every node
        """
        if node is None:
            return -1
            
        # call the callback function passing the node
        if callback(index=index, node=node) == -1:
            return -1

        # Traverse children first (depth-first)
        current_child = node.firstChild
        while current_child is not None:
            index = self._traverse(index=index+1, node=current_child, callback=callback)
            if index == -1: break
            current_child = current_child.nextSibling
        return index

    def get_indexed_elements(self) -> dict[int: opendocument.Element]:
        """
        Iterates through all child and sibling nodes of a tree and returns them 
        in an indexed dictionary {index: element}.
        
        Returns:
            dict: Dictionary with index as key and node as value
        """
        result = {}
        
        def index_nodes(index, node) -> int:
            nonlocal result
            result[index] = node
            return index

        self._traverse(0, self.document.body, index_nodes)

        return result

    def get_indexed_text(self, markdown = True)-> dict[int:str]:
        """
        Extract text content from the ODT document.
        """
        content_dict = {}

        def get_text(index, node) -> int:

            nonlocal content_dict
            nonlocal markdown

            text = teletype.extractText(node)
            try:
                if node.tagName  == 'text:a':
                    link = node.attributes.get(('http://www.w3.org/1999/xlink', 'href'), 'unkown')
                    # If is a A then assume parent is a P and it's index is on -1
                    content_dict[index-1] = f"[{text}]({link})" if markdown and text  else text
                elif node.tagName == 'draw:line':
                    content_dict[index-1] = "---" if markdown else ''
                elif node.tagName  == 'text:p':
                    if node.parentNode.tagName  == 'text:list-item':
                        content_dict[index] = f"- {text}" 
                    else:
                        content_dict[index] = f"{text}" if markdown and text else text
                elif node.tagName  ==  'text:h':
                    level = int(node.attributes.get(('urn:oasis:names:tc:opendocument:xmlns:text:1.0', 'outline-level'), '4'))
                    content_dict[index] = f"{'#'*level} {text}" if markdown and text else text
            except Exception as ex:
                print(f"{ex} processing element {index}")

            return index

        self._traverse(0, self.document.body, get_text)

        return content_dict

    def get_text(self, markdown = True) -> str:
        return "\n".join(self.get_indexed_text(markdown = markdown).values())

    def replace(self, indexed_replacements: dict[int: str]):

        for index, element in reversed(list(self.get_indexed_elements().items())):
            try:
                if index in indexed_replacements:
                    self._set_text(element, indexed_replacements[index])
                    # print(f"Updated {index}: {indexed_replacements[index]}")

            except Exception as e:
                print(f"Error {e} processing element {index}")

    def _set_text(self, elem, replacement):
        """
        Parse a string with **bold** words and add Span elements to a P element
        
        Args:
            elem (P): The paragraph element to modify
            replacement (str): Text with **bold** words
        """
        # Create a style for bold text if it doesn't exist
        bold_style_exists = False
        for style in self.document.styles.getElementsByType(Style):
            if style.getAttribute("name") == "Bold":
                bold_style_exists = True
                break
        
        # Create bold style if it doesn't exist
        if not bold_style_exists:
            bold_style = Style(name="Bold", family="text")
            bold_props = TextProperties(fontweight="bold")
            bold_style.addElement(bold_props)
            self.document.styles.addElement(bold_style)
        
        new_elem = P(stylename=elem.getAttribute("stylename"))

        # Split the text by ** to identify bold sections
        parts = replacement.split('**')
        
        # Process parts - alternating between normal and bold text
        for i, part in enumerate(parts):
            if i % 2 == 0:
                # Normal text
                if part.strip():  # Only add non-empty text
                    new_elem.addElement(Span(text=part))
            else:
                # Bold text
                if part.strip():  # Only add non-empty text
                    new_elem.addElement(Span(stylename="Bold", text=part))

        elem.parentNode.insertBefore(new_elem,elem)
        elem.parentNode.removeChild(elem)
        
if __name__ == "__main__":

    import json
    file_path = os.path.dirname(os.path.abspath(__file__))+"/../workspace/cv_original.odt"
    document = OdtDocument(file_path)

    # print(document.get_indexed_text())
    # document.replace({215: "Autonomía y retroactividad",})
    # print(document.get_indexed_text()[215])

    print(json.dumps(document.get_indexed_text(), indent=2, ensure_ascii=True))

    # document.save("../workspace/cv_adapted.odt")

