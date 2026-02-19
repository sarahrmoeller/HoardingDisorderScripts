import warnings
import stanza
import stanza.models.constituency.parse_tree as pt
import statistics as stats


nlp = stanza.Pipeline(lang='en', processors='tokenize,pos,constituency')


def type_token_ratio(tokens: list[str] | list[list[str]],
                     per_sent=True) -> float:
    """
    Calculate the type-token ratio of a document.
    
    :param tokens: : Either a flat list of tokens (`list[str]`), 
                     or a list of tokenized sentences 
                     (`list[list[str]]`).
    :type tokens: list[str] or list[list[str]]
    :param per_sent: If `True`, the function expects an input in the form 
                     of `list[list[str]]`, which is a list of tokenized 
                     sentences. The TTR of each sentence is calculated and
                     their average is returned. 
                     If `False`, the function expects a flat list of 
                     tokens, and the TTR of that list is calculated.
    :type per_sent: bool
    :return: The type-token ratio of the document.
    :rtype: float
    """
    if not tokens:
        warnings.warn("Empty token list provided for type-token ratio "
                      "calculation.")
        return 0.0
    if per_sent:
        return sum([len(set(token.lower() for token in sent)) / len(sent) 
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


def count_nps(tree: pt.Tree) -> int:
    """
    Recursively count the number of noun phrases (NPs) in a constituency parse 
    tree.

    Args:
        tree (Tree): A constituency parse tree for a sentence.

    Returns:
        int: Total number of NP (noun phrase) nodes in the tree.
    """
    # Theoretically, this will count only the lowest node
    # If this node is an NP and contains no NP children, it's a lowest NP
    if tree.label == 'NP' and \
        all(child.label != 'NP' for child in tree.children 
            if isinstance(child, pt.Tree)):
        return 1
    # Recurse into children
    return sum(count_nps(child) for child in tree.children 
               if isinstance(child, pt.Tree)) # type: ignore


def count_non_NP_phrases(tree: pt.Tree) -> int:
    """
    Recursively counts the total number of phrase nodes in a Stanza 
    constituency tree. We define a "phrase" to be any node that is not 
    preterminal---since all terminal nodes are words, we assume preterminal
    nodes are POS tags for the words.

    Args:
        tree (stanza.models.common.constituent.Tree): The constituency tree or 
        a sub-tree.

    Returns:
        int: The total count of phrase nodes in the tree.
    """
    # Base case    
    if tree.is_preterminal():
        return 0

    # Recursive step: Count this node as 1 phrase, then add the counts
    # from all of its children that are also sub-trees.
    # Exclude the ROOT and S nodes from the count
    return int(tree.label not in {'ROOT', 'S', 'NP'}) + \
            sum(count_non_NP_phrases(child) for child in tree.children)


def NP_ratio(tree: pt.Tree) -> float:
    """
    Calculate the noun phrase (NP) ratio for a given constituency tree.

    The NP ratio is defined as:
        number of noun phrases (NPs) / number of phrases in the sentence

    Args:
        tree (stanza.models.common.constituent.Tree): The constituency tree 
        for a sentence.

    Returns:
        float: The NP ratio
    """
    if not tree:
        return 0.0
    np_count = count_nps(tree)
    other_phrases_count = count_non_NP_phrases(tree)
    if np_count + other_phrases_count == 0:
        return 0.0
    return np_count / (np_count + other_phrases_count)


def count_nps_in_sd(stanza_doc) -> int:
    if not stanza_doc:
        return 0
    return sum(count_nps(sent.constituency) for sent in stanza_doc.sentences)


def NP_ratio_in_sd(stanza_doc) -> float:
    if not stanza_doc or len(stanza_doc.sentences) < 1:
        return 0.0
    return stats.mean(NP_ratio(sent.constituency) 
                      for sent in stanza_doc.sentences
                      if sent)