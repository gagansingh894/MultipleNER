import re
from nltk.corpus import stopwords

my_stopwords = list(stopwords.words('english'))


def process_text(inp: str, replace_whitespace: bool = False, to_lower: bool = False) -> str:
    """
    This function removes unwanted punctuation from the text and converts to proper text, lower text based on flag.
    :param to_lower: bool flag
    :param replace_whitespace: bool flag
    :param inp: input string
    :return: processed string
    """
    if replace_whitespace:
        return inp.strip().replace('"', "").title().replace(" ", "")
    elif to_lower:
        return inp.strip().replace('"', "").lower()
    else:
        return inp.strip().replace('"', "").title()


def check_for_digits(inp: str) -> bool:
    """
    This function checks if digits are present in string
    :param inp:
    :return:
    """
    inp.replace(" ", "")
    return any([char.isdigit() for char in inp])


def clean_text(inp: str) -> str:
    """
    Clean text by removing special symbols and stopwords
    :param inp: input string
    :return: cleaned string
    """
    inp = ' '.join([w.lower() for w in inp.split(" ") if w.lower() not in my_stopwords])
    inp = re.sub('[^A-Za-z0-9]+', '', inp)
    return inp


if __name__ == "__main__":
    pass