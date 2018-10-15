import logging
from ptm import get_reuters_token_list_by_sentence

logger = logging.getLogger('HMM_LDA')
logger.propagate=False
n_docs = 1000
voca, corpus = get_reuters_token_list_by_sentence(num_doc=n_docs)
