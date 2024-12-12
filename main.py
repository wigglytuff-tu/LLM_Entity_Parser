# main.py

import timeit
import box
import yaml
import faiss
import numpy as np
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from llm.wrapper import setup_qa_chain, query_embeddings

# Import config vars
with open('config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = box.Box(yaml.safe_load(ymlfile))


def get_answer(query_text, semantic_search=False):
    """
    Retrieves an answer for the given query using either semantic search or a QA chain.

    Args:
        query_text (str): The user's query.
        semantic_search (bool): If True, perform semantic search; else, use QA chain.

    Returns:
        str: The answer to the query.
    """
    start = timeit.default_timer()

    if semantic_search:
        # Perform semantic search
        semantic_search_result = query_embeddings(query_text)
        answer = f"Semantic search result: {semantic_search_result}"
    else:
        # Perform QA using the QA chain
        qa_chain = setup_qa_chain()
        response = qa_chain({'query': query_text})
        answer = response.get("result", "No answer found.")

    end = timeit.default_timer()
    time_taken = end - start

    return answer, time_taken

# import timeit
# import argparse
# from llm.wrapper import setup_qa_chain
# from llm.wrapper import query_embeddings
# 
# 
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument('input',
#                         type=str,
#                         default='What is the invoice number value?',
#                         help='Enter the query to pass into the LLM')
#     parser.add_argument('--semantic_search',
#                         type=bool,
#                         default=False,
#                         help='Enter True if you want to run semantic search, else False')
#     args = parser.parse_args()
# 
#     start = timeit.default_timer()
#     if args.semantic_search:
#         semantic_search = query_embeddings(args.input)
#         print(f'Semantic search: {semantic_search}')
#         print('='*50)
#     else:
#         qa_chain = setup_qa_chain()
#         response = qa_chain({'query': args.input})
#         print(f'\nAnswer: {response["result"]}')
#         print('=' * 50)
#     end = timeit.default_timer()
# 
#     print(f"Time to retrieve answer: {end - start}")
