import easyocr


class OCRReader:

    def __init__(self):

        self.reader = easyocr.Reader(
            ['en'],
            gpu=False
        )

    def read_image(self, image_path):

        result = self.reader.readtext(image_path)

        extracted_text = []

        for item in result:

            extracted_text.append(item[1])

        return "\n".join(extracted_text)