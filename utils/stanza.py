# unusable for now

import stanza.models.common.doc as stnzdoc
    
    @cached_property
    def _stanza_docs(self) -> dict:
        """
        Cache stanza Document objects for each speaker.
        """
        from . import ling
        return {speaker: ling.nlp(self.content_by_speaker(speaker))
                for speaker in self.default_speaker_pair}

    def stanza_doc(self, speaker: str) -> stnzdoc.Document:
        """
        Returns a stanza Document object for the content spoken by the
        specified speaker. Uses a cached dictionary to avoid recomputation.
        """
        return self._stanza_docs[speaker]

    def tokens_by_speaker(self, speaker: str, per_sent: bool=True) -> list[list[str]]:
        """
        Returns a list of tokens (as strings) in the content spoken by the 
        specified speaker. 
        `per_sent` controls whether a list of lists is returned, where each
        inner list contains the tokens in a single sentence, or whether a 
        flattened list of all tokens is returned.
        """
        sd = self.stanza_doc(speaker)
        if per_sent:
            return [[token.text for token in sent.tokens] 
                    for sent in sd.sentences]
        return [token.text for token in sd.iter_tokens()]