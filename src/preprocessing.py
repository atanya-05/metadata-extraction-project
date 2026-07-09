import re


class TextPreprocessor:

    @staticmethod
    def clean(text):

        text = text.replace("\n", " ")

        text = re.sub(r"\s+", " ", text)

        text = text.strip()

        return text