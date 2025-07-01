import warnings


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