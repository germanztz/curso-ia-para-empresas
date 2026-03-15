from odf import opendocument

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

        self.document.save(file_path)

    def get_indexed_elements(self) -> dict[int: opendocument.Element]:
        """
        Iterates through all child and sibling nodes of a tree and returns them 
        in an indexed dictionary {index: element}.
        
        Returns:
            dict: Dictionary with index as key and node as value
        """
        result = {}
        index = 0
        
        def traverse(node):
            nonlocal index
            if node is None:
                return
                
            # Add current node to result
            result[index] = node
            index += 1
            
            # Traverse children first (depth-first)
            current_child = node.firstChild
            while current_child is not None:
                traverse(current_child)
                current_child = current_child.nextSibling
        
        traverse(self.document.body)
        return result

    def get_indexed_text(self, markdown = True)-> dict[int:str]:
        """
        Extract text content from the ODT document.
        """
        content_dict = {}
        index = 0        
        # Get all text elements from the document
        for index, element in self.get_indexed_elements().items():
            try:
                # Check if element is a paragraph (P) or heading (H)
                if element.tagName  == 'text:p':
                    content_dict[index] = str(element)
                elif element.tagName  ==  'text:h':
                    level = 4 
                    try:
                        level = int(element.attributes.get(('urn:oasis:names:tc:opendocument:xmlns:text:1.0', 'outline-level'), '4'))
                    except:
                        pass
                    content_dict[index] = f"{'#'*level} {element}" if markdown else str(element)
            except Exception as e:
                print(f"{e} processing element {index}")

        return content_dict

    def get_text(self, markdown = True) -> str:
        return "\n".join(self.get_indexed_text(markdown = markdown).values())

    def replace(self, indexed_replacements: dict[int: str]):

        for index, element in self.get_indexed_elements().items():
            try:
                if index in indexed_replacements:
                    self.clear(element)
                    element.addText(indexed_replacements[index])

            except Exception as e:
                print(f"Error {e} processing element {index}")

    def clear(self, element: opendocument.Element ):
        try:
            while True:
                element.removeChild(element.firstChild)
        except:
            pass

    # def text_with_links(elem):
    #     """Genera texto incluyendo enlaces en formato Markdown [texto](href)."""
    #     result = []
    #     for child in elem:
    #         tag_local = child.tag.split("}")[-1]
    #         if tag_local == "a":
    #             href = child.attrib.get("{http://www.w3.org/1999/xlink}href", "")
    #             texto_link = "".join(child.itertext()).strip()
    #             result.append(f"[{texto_link}]({href})")
    #         else:
    #             result.append(text_with_links(child) if child is not None else child.text or "")
    #     if elem.text:
    #         result.insert(0, elem.text)
    #     return "".join(result)

if __name__ == "__main__":

    file_path = "/home/daimler/workspaces/curso-ia-para-empresas/workspace/cv_adapted.odt"
    document = OdtDocument(file_path)

    document.replace({16: "jhon.doe@replaced.com",})
    print(document.get_indexed_text()[16])
    document.save()
    # print("\n".join([f"{index}: {text}" for index, text in document.get_indexed_text().items()]))
