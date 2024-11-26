# Note: Precise formatting of spacing and indentation of the prompt template is important,
# as it is highly sensitive to whitespace changes. For example, it could have problems generating
# a summary from the pieces of context if the spacing is not done correctly

qa_template = """Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}
Question: {question}
Example:
Context: ```Company contracts (contract agreement between two companies)```
User: ```Extract the following key and value pairs and output in CSV format:
1. Name of the 1 st Party
2. Name of the 2 nd Party
3. Contract start date
4. Contract end date
5. Scope of work
6. Penalty amount```
Helpful answer: ```
Name of the 1 st Party,Name of the 2 nd Party,Contract start date,Contract end date,Scope of work,Penalty amount
value1, value2, value3, value4, value5, value6```
Only return the helpful answer below and nothing else. Your answer should be in csv format.
Helpful answer:
"""