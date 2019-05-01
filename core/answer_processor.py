class AnswerProcessorService():
    """ """
    def __init__(self):
        pass

    def find_answer(self, sentence, question):
        """Find the answer within the sentence."""
        type = question.type.split(':')[0]
        NP = self.find_phrases(sentence, [])
        return ' '.join(NP)

    def find_phrases(self, sentence, phrases):
        def search_NP_VP(tree):
            if len(tree) == 0:
                return None
            if len(tree) == 2:
                if tree[0].label() == 'NP' and tree[1].label() == 'VP':
                    return tree[0]
            else:
                sub = [search_NP_VP(child) for child in tree]
                sub = [s for s in sub if s is not None]
                if sub:
                    return sub[0]
                else:
                    return None

        start = sentence.tree[0]
        return search_NP_VP(start)


AnswerProcessor = AnswerProcessorService()
