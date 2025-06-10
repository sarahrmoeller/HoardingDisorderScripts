import warnings
import stanza

stanza.download('en')
nlp = stanza.Pipeline()


def type_token_ratio(tokens: list[str] | list[list[str]],
                     per_sent=False) -> float:
    """
    Calculate the type-token ratio of a document.
    
    Args:
        tokens (list[list[str]]): Either a flat list of tokens (`list[str]`), 
                                  or a list of tokenized sentences 
                                  (`list[list[str]]`).
        per_sent (bool): If `True`, the function expects an input in the form 
                         of `list[list[str]]`, which is a list of tokenized 
                         sentences. The TTR of each sentence is calculated and
                         their average is returned. 
                         If `False`, the function expects a flat list of 
                         tokens, and the TTR of that list is calculated.
        
    Returns:
        float: The type-token ratio of the document.
    """
    if not tokens:
        warnings.warn("Empty token list provided for type-token ratio "
                      "calculation.")
        return 0.0
    if per_sent:
        return sum([len(set(token.lower() for token in sent)) 
                    for sent in tokens]) / len(tokens)
    # Otherwise tokens are flat
    return len(set(token.lower() for token in tokens)) / len(tokens) # type: ignore


def average_sentence_length(sentences: list[list[str]]) -> float:
    """
    Calculate the average sentence length of a document.
    
    Args:
        sentences (list[list[str]]): A list of sentences, each sentence is a list of tokens.
        
    Returns:
        float: The average number of tokens in each sentence in the document.
    """
    if not sentences:
        warnings.warn("Empty sentences list provided for average sentence "
                      "length calculation.")
        return 0.0
    return sum(len(sent) for sent in sentences) / len(sentences)


def count_nps(tree):
    """
    Recursively count the number of noun phrases (NPs) in a constituency parse tree.

    Args:
        tree (Tree): A constituency parse tree for a sentence.

    Returns:
        int: Total number of NP (noun phrase) nodes in the tree.
    """
    count = 0
    if tree.label == 'NP':
        count += 1
    for child in tree.children:
        if not isinstance(child, str): #not sure if this is correct
            count += count_nps(child)
    return count


def get_np_counts(text):
    """ 
    Compute the number of noun phrases (NPs) in each sentence of a given text.

    Args:
        text (str): A block of text containing one or more sentences.

    Returns:
        List[int]: A list of NP counts, one per sentence.
    """
    doc = nlp(text)
    return [count_nps(sentence.constituency) for sentence in doc.sentences]


def get_np_ratios(text):
    """ 
    MAIN FUNCTION: Calculate the noun phrase (NP) ratio for each sentence in a given text.

    The NP ratio is defined as:
        number of noun phrases (NPs) / number of words in the sentence

    Args:
        text (str): A block of text containing one or more sentences.

    Returns:
        List[float]: A list of NP ratios (rounded to 2 decimal places),
                     one for each sentence in the text.
    """
    doc = nlp(text)
    ratios = []
    for sentence in doc.sentences:
        np_count = count_nps(sentence.constituency)
        word_count = len(sentence.words)
        ratios.append(round(np_count / word_count, 2) if word_count > 0 else 0)
    return ratios