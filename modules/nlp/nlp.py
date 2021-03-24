import re
import spacy

from typing import List

nlp = spacy.load("en_core_web_sm")

TWITTER_LINK = r'https://t.co/.*'
WHITESPACE = " "
DOUBLE_WHITESPACE = "  "


def sanitize_with_exceptions(text, exceptions):
    """
    sanitize text orchestrator
    :param text: text to sanitize
    :param exceptions: list of words to except from sanitization
    :return: string of sanitized text excepting the indicated words
    """
    return join_words(
        sanitize_whitespaces(
          sanitize_punctuation_with_exceptions(text, exceptions)))


def sanitize_single_quote_for_sql(text):
    """
    substitutes a single quote into two single quotes (following SQL syntax)
    """
    if text:
        return text.replace("'", "''")
    return ""


def sanitize_punctuation_with_exceptions(text, exceptions):
    """
    removes unnecessary punctuation, splits text, returning a list of words
    """
    words = text.replace("\n", WHITESPACE)\
        .replace(",", WHITESPACE)\
        .replace(",.\"", WHITESPACE)\
        .split()

    return [(w.lower() if w not in exceptions else w) for w in words]


def sanitize_whitespaces(words: List[str]):
    """
    delete double whitespaces and other unnecessary whitespaces
    """
    clear_words = []
    for word in words:
        clear_word = word.replace(r"\s\s+", WHITESPACE)

        while DOUBLE_WHITESPACE in clear_word:
            clear_word = clear_word.replace(DOUBLE_WHITESPACE, WHITESPACE)
        clear_words.append(clear_word)
    return clear_words


def join_words(words):
    return WHITESPACE.join(words)


def extract_twitter_links(text):
    words = text.split()
    return [w for w in words if re.match(TWITTER_LINK, w)]


def extract_text_entities(text):
    entities = []
    if text:
        doc = nlp(text)
        for entity in doc.ents if doc.ents else []:
            if entity.text:
                entities.append({"text_entity_value": sanitize_single_quote_for_sql(
                    sanitize_with_exceptions(entity.text, exceptions=[])),
                                 "text_entity_label": entity.label_})
    return entities
