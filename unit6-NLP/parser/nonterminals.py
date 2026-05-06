# Ben's:

NONTERMINALS = """
S -> NP VP | S NP
NP -> N | Det NP | Adj NP | NP P | ConjP NP | NP V | Det Adj NP | NP P NP
VP -> V | VP P | ConjP VP | Adv VP | VP Adv | V NP | VP PP
PP -> P NP | P VP
ConjP -> Conj | NP Conj | VP Conj
"""

# Mine:

NONTERMINALS = """
S -> NP VP | S NP
NP -> N | Det N | Adj NP | NP P | ConjP NP | NP V | Det Adj NP | NP P NP
VP -> V | VP P | ConjP VP | Adv VP | VP Adv | V NP | VP PP
PP -> P NP | P VP
ConjP -> Conj | NP Conj | VP Conj
"""