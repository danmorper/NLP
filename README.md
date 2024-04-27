# data_loader.py

It divides the text from a pdf into chunks of a certain size and with some overlap.

## DocumentPart Class

- Purpose: Represents a segment (or chunk) of the text from the PDF.
- Attributes:
    - text: Stores the actual text content of the chunk.
    - metadata: Contains metadata about the chunk, such as the page number from which the text was extracted.
- Methods:
    - __str__: Overrides the default string representation method to provide a readable format of the chunk's content and its metadata. This method displays the first 100 characters of the text and the metadata information, facilitating easier debugging and output viewing.

## PDFReader Class

- Purpose: Manages the reading and chunking of the PDF document.
- Attributes:
    - pdf_path: The file path to the PDF document.
    - document_parts: A list that will store all the DocumentPart instances created from the PDF.
    - chunk_size: Specifies the size of each text chunk in characters.
    - overlap: Specifies the number of characters that should overlap between consecutive chunks.
- Initialization: During initialization, the __init__ method sets the attributes and calls the _read_pdf method to start processing the PDF.

## PDF Processing (_read_pdf Method)

- Text Extraction:
    - Opens the PDF file and iterates through each page using PyPDF2.
    - Extracts text from each page and aggregates it into a text_buffer.
- Chunking Logic:
    - As the text_buffer accumulates text from the pages, it checks if the buffer's size exceeds the specified chunk_size.
    - If so, it calculates an end_index for slicing the buffer, taking into account the overlap to ensure continuity in text analysis.
    - Slices the text_buffer to create a DocumentPart, which it adds to document_parts.
    - Adjusts the buffer by removing the processed part, preserving the overlap if specified.
- Handling the Last Chunk:
    - After all pages are processed, any remaining text in the text_buffer is also converted into a DocumentPart to ensure no text is left unprocessed.

## Utility Methods
- get_part: Allows retrieval of a specific chunk by its index, providing direct access to individual DocumentPart instances.
- str: Provides a concatenated string representation of all the document parts, showing each part's content when the PDFReader instance is printed.