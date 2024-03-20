from llama_index.node_parser import SimpleNodeParser
from llama_index.node_parser.extractors import (
    MetadataExtractor,
    SummaryExtractor,
)
import json
from llama_index import Document
import os

from llm.utils import KeywordExtractor
from config import JSON_OUTPUT, OPENAI_API_KEY, TEST_MODE

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

def main():
    metadata_extractor = MetadataExtractor(
        extractors=[
            SummaryExtractor(summaries=["self"]),
            KeywordExtractor(keywords=20),
        ],
    )

    node_parser = SimpleNodeParser.from_defaults(
        metadata_extractor=metadata_extractor,
    )

    with open(f"{JSON_OUTPUT}_step2.json", "r") as f:
        data = json.load(f)

    documents = []
    for d in data:
        if "text" in d:
            documents.append(Document(text=d["text"], metadata={
                            "link": d["link"], "publisher": d["publisher"], "date": d["date"]}))

    if TEST_MODE:
        documents = documents[:5]

    nodes = node_parser.get_nodes_from_documents(documents)
    res = []
    for node in nodes:
        
        node.metadata['excerpt_keywords'] = json.loads(node.metadata['excerpt_keywords'])
        res.append(node.metadata)

    with open(f"{JSON_OUTPUT}_step3.json", "w") as json_file:
            json.dump(res, json_file, default=str)