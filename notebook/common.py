from yargy.interpretation import fact, attribute
from yargy.relations import gnc_relation
from yargy.tokenizer import MorphTokenizer
from yargy.utils import Record

Record.means = lambda self, *args, **kwargs: self.interpretation(*args, **kwargs)

TOKENIZER = MorphTokenizer()  # todo move to notebook
gnc = gnc_relation()

Array = fact('Array', [attribute('element').repeatable()])
