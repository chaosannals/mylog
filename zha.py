import re
import jieba
from whoosh.analysis import LowercaseFilter, StopFilter, StemFilter, Tokenizer, Token
from whoosh.lang.porter import stem

STOP_WORDS = frozenset([
    'a', 'an', 'are',
    '的', '了', '和', '我'
])

ACCEPTED_CHARS = re.compile(r"[\u4E00-\u9FD5]+")

jieba.load_userdict('conf/extdict.txt')

class ChineseTokenizer(Tokenizer):
    '''
    
    '''

    def __call__(self, text, 
        positions=False,
        chars=False,
        keeporiginal=False,
        removestops=True,
        start_pos=0,
        start_char=0,
        tokenize=True,
        mode='',
        **kwargs):
        '''
        '''

        words = jieba.tokenize(text, mode='search')
        token = Token(positions, chars, removestops=removestops, mode=mode, **kwargs)
        for (w, start_pos, stop_pos) in words:
            if not ACCEPTED_CHARS.match(w) and len(w) <= 1:
                continue
            token.original = w
            token.text = w
            token.pos = start_pos
            token.startchar = start_pos
            token.endchar = stop_pos
            yield token

def zh_analyzer(stoplist=STOP_WORDS, minsize=1, stemfn=stem, cachesize=50000):
    return (
        ChineseTokenizer() |
        LowercaseFilter() |
        StopFilter(stoplist=stoplist, minsize=minsize) |
        StemFilter(stemfn=stemfn, ignore=None, cachesize=cachesize)
    )