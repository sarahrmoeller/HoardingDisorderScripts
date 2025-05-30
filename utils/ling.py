import warnings


def type_token_ratio(flat_tokens: list[str]) -> float:
    """
    Calculate the type-token ratio of a document.
    
    Args:
        doc (list[list[str]]): A list of sentences, each sentence is a list of tokens.
        
    Returns:
        float: The type-token ratio of the document.
    """
    if not flat_tokens:
        warnings.warn("Empty token list provided for type-token ratio "
                      "calculation.")
        return 0.0
    return len(set(token.lower() for token in flat_tokens)) / len(flat_tokens)


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