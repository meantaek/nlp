from collections import deque


class Token():
    """Represents a single token in a document.

    For example, a token "Pittsburgh" with tags "NNP" and "LOC" can be
    initialized with Token("Pittsburgh", ["NNP", "LOC"])
    """

    def __init__(self, word, tags):
        self.word = word
        self.tags = set(tags)

    def add_tag(self, tag):
        self.tags.add(tag)

    def remove_tag(self, tag):
        self.tags.remove(tag)


class Variable():
    """Represents a variable in a pattern.

    The const attribute determines whether or not it is a constant variable.
    """

    def __init__(self, token, const=False):
        self.token = token
        self.const = const

    def match(self, token):
        tags_match = all([tag in token.tags for tag in self.token.tags])
        if self.const:
            return tags_match and token.word == self.token.word
        return tags_match


class Pattern():
    """Represents a pattern.

    For example, simple pattern of "NN is NN" might be initialized with:

    p = Pattern('[NN] is [NN]')
    truck = Token('Truck', ['NN'])
    vehicle = Token('vehicle', ['NN'])
    print(p.format({0: truck, 1: vehicle}))

    >> 'Truck is vehicle'
    """

    def __init__(self, input):
        if isinstance(input, (str)):
            self.variables = [
                self._str_to_var(s)
                for s in input.strip().split()
            ]
        else:
            tokens, is_consts = input
            self.variables = [
                Variable(token, const=const)
                for token, const in zip(tokens, is_consts)
            ]

    def _str_to_var(self, string):
        """Parse string and return a Variable.

        If the string is of the format [X,Y], return Variable with tags=[X, Y]
        Otherwise, return a constant
        """
        if string[0] == '[' and string[-1] == ']':
            tags = string[1:-1].strip().split(',')
            token = Token('', tags)
            return Variable(token, const=False)
        else:
            token = Token(string, [])
            return Variable(token, const=True)

    def match(self, tokens):
        matches = True
        parameters = []
        for var, token in zip(self.variables, tokens):
            match = var.match(token)
            matches = matches and match
            if match and not var.const:
                parameters.append(token)
        return matches, parameters

    def search(self, tokens):

        def search_helper(m, n, params):
            if n == 0:
                return [params]
            if m == 0:
                return []

            if self.variables[n-1].match(tokens[m-1]):
                if not self.variables[n-1].const:
                    new_params = [tokens[m-1]] + params
                else:
                    new_params = params
                return search_helper(m-1, n-1, new_params) + \
                    search_helper(m-1, n, params)
            else:
                return search_helper(m-1, n, params)

        m = len(tokens)
        n = len(self.variables)
        matches = search_helper(m, n, [])
        return matches

    def format(self, tokens_map):
        words = []
        param_idx = 0
        for var in self.variables:
            if var.const:
                words.append(var.token.word)
            elif var.match(tokens_map[param_idx]):
                token = tokens_map.get(param_idx)
                if token and var.match(token):
                    words.append(token.word)
                param_idx += 1
        return " ".join(words)

    def constants(self):
        return [var for var in self.variables if var.const]

    def not_constants(self):
        return [var for var in self.variables if not var.const]


class ExtractionRule():
    """Represents an extraction rule that converts one pattern to another.

    input1 and input2 define two Patterns
    map determines how the outputs of a match on Pattern(input1) are fed
    into Pattern(input 2)

    For example, if we have the rule:

        rule = ExtractionRule('[NN] is [NN]', 'What is [NN] ?', {0: 0})

    Then only the first [NN] is mapped to the second rule.
    """

    def __init__(self, input1, input2, mapping):
        self.pattern1 = Pattern(input1)
        self.pattern2 = Pattern(input2)
        self.mapping = mapping
        # NOTE: add input validation later

    def extract(self, tokens):
        p1 = self.pattern1
        p2 = self.pattern2
        matches = p1.search(tokens)

        mapped_params = [
            {
                p2_idx: params[p1_idx]
                for p1_idx, p2_idx in self.mapping.items()
            } for params in matches
        ]
        return [p2.format(params) for params in mapped_params]
