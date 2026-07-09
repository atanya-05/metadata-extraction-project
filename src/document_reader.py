from pathlib import Path
from docx import Document


class DocumentReader:

    @staticmethod
    def read_docx(file_path):

        document = Document(file_path)

        paragraphs = []

        for paragraph in document.paragraphs:

            text = paragraph.text.strip()

            if text:
                paragraphs.append(text)

        return "\n".join(paragraphs)