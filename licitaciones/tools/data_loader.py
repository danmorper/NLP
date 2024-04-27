# Read pdf
import PyPDF2

class DocumentPart:
    def __init__(self, text, metadata):
        self.text = text
        self.metadata = metadata
    def __str__(self):
        # This will return the first 100 characters of text and the metadata page number.
        return f"Part({self.text}: {self.metadata})"
class PDFReader:
    def __init__(self, pdf_path, chunk_size, overlap):
        self.pdf_path = pdf_path
        self.document_parts = []
        self.chunk_size = chunk_size
        self.overlap = overlap
        self._read_pdf()

    def _read_pdf(self):
        with open(self.pdf_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)

            text_buffer = ""
            page_number = 0
            while page_number < num_pages:
                page = pdf_reader.pages[page_number]
                page_content = page.extract_text() or ""
                text_buffer += page_content
                while len(text_buffer) >= self.chunk_size:
                    end_index = self.chunk_size
                    if self.overlap:
                        end_index -= self.overlap
                    self.document_parts.append(DocumentPart(text=text_buffer[:end_index], metadata={"page": page_number + 1}))
                    text_buffer = text_buffer[end_index:] if not self.overlap else text_buffer[end_index - self.overlap:]
                page_number += 1
            
            # Handle the last chunk that might be smaller than chunk_size
            if text_buffer:
                self.document_parts.append(DocumentPart(text=text_buffer, metadata={"page": page_number}))

    def get_part(self, part_number):
        if 0 < part_number <= len(self.document_parts):
            return self.document_parts[part_number - 1]
        else:
            return None
        
    def __str__(self):
        # Create a string representation of all DocumentPart objects in the document
        printed_text = ""
        for part in self.document_parts:
            printed_text += str(part) + "\n"
        return printed_text