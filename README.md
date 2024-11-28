# Entity parsing and processing with Mistral LLM on local CPU
We download the Mistral Model locally for native computation, avoiding any API usage or data leaks.
## Quickstart

1. Download the Mistral model, check models/model_download.txt for the download link.
2. Install the requirements: 

`pip install -r requirements.txt`

3. Copy text PDF files to the `data` folder.
4. Run the script, to convert text to vector embeddings and save in FAISS index: 

`python ingest.py`

5. Run the script, to process data with Mistral LLM and return the answer: 

`python main.py "{Enter your Query Here}"`

Example Query Format: """Extract the following key and value pairs and output in CSV format:
1. Name of the 1 st Party
2. Name of the 2 nd Party
3. Contract start date
4. Contract end date
5. Scope of work
6. Penalty amount"""

## Future Improvements
1. Finally sending response to CSV file after data sanitization check
2. Improving runtime efficiency, better to adapt for gpu
3. Experiment with better LLM Models.
4. Add support for different modalities other than pdf.

