# coding=utf-8
"""
Methods for Processing XML Documents
"""
import re


def extract_from_tag(text, tag_name):
    # Extract information between tags
    content = re.compile('<' + tag_name + '>' + '(.*)' + '</' + tag_name + '>', re.DOTALL).search(text)
    if content is not None:
        return content.group(1).strip()
    else:
        return ''


def prettify(text):
    # Process XML text

    # Remove XML tags
    text = re.sub(re.compile('<.*?>'), r'', text)

    # Remove hyperlink
    text = re.sub(r'https?:\/\/.*\/\w*', '', text)

    # Remove EOL characters
    text = re.sub(re.compile('\n'), ' ', text)

    # Remove punctuations
    text = re.sub(r'[\?\:\!\.\,\;]', '', text)

    # won't to will not
    text = re.sub(r'won\'t', 'will not', text)

    # n't to not
    text = re.sub(r'(\w+)n\'t', r'\1 not', text)

    # n’t to not
    text = re.sub(r'(\w+)n’t', r'\1 not', text)

    # Remove 's
    text = re.sub(r'\'s', r'', text)

    # Remove ’s
    text = re.sub(r'’s', r'', text)

    # Remove 'm
    text = re.sub(r'\'m', r'', text)

    # Remove ’m
    text = re.sub(r'’m', r'', text)

    # Remove 've
    text = re.sub(r'\'ve', r'', text)

    # Remove ’ve
    text = re.sub(r'’ve', r'', text)

    # Remove 'll
    text = re.sub(r'\'ll', r'', text)

    # Remove ’ll
    text = re.sub(r'’ll', r'', text)

    # Convert to lower case
    text = text.lower()

    # Only keep alphabet characters
    text = re.sub(r'[^a-z ]', r'', text)

    return text
