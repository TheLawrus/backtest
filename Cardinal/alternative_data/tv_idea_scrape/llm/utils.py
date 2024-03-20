from typing import Dict, List
from llama_index.node_parser.extractors import MetadataFeatureExtractor
from typing import Any, Dict, List, Optional, Sequence, cast

from llama_index.bridge.pydantic import Field
from llama_index.llm_predictor.base import BaseLLMPredictor, LLMPredictor
from llama_index.llms.base import LLM
from llama_index.prompts import PromptTemplate
from llama_index.schema import BaseNode, TextNode

class KeywordExtractor(MetadataFeatureExtractor):
    """Keyword extractor. Node-level extractor. Extracts
    `excerpt_keywords` metadata field.

    Args:
        llm_predictor (Optional[BaseLLMPredictor]): LLM predictor
        keywords (int): number of keywords to extract
    """

    llm_predictor: BaseLLMPredictor = Field(
        description="The LLMPredictor to use for generation."
    )
    keywords: int = Field(default=5, description="The number of keywords to extract.")

    def __init__(
        self,
        llm: Optional[LLM] = None,
        # TODO: llm_predictor arg is deprecated
        llm_predictor: Optional[BaseLLMPredictor] = None,
        keywords: int = 5,
        **kwargs: Any,
    ) -> None:
        """Init params."""
        if keywords < 1:
            raise ValueError("num_keywords must be >= 1")

        if llm is not None:
            llm_predictor = LLMPredictor(llm=llm)
        elif llm_predictor is None and llm is None:
            llm_predictor = LLMPredictor()

        super().__init__(llm_predictor=llm_predictor, keywords=keywords, **kwargs)

    @classmethod
    def class_name(cls) -> str:
        return "KeywordExtractor"

    def extract(self, nodes: Sequence[BaseNode]) -> List[Dict]:
        metadata_list: List[Dict] = []
        for node in nodes:
            if self.is_text_node_only and not isinstance(node, TextNode):
                metadata_list.append({})
                continue

            # TODO: figure out a good way to allow users to customize keyword template
            keywords = self.llm_predictor.predict(
                PromptTemplate(
                    template=f"""\
{{context_str}}. You are a tool for a stock market researcher. \
Give {self.keywords} unique keywords or phrases for this document. Format \
as json with keywords as keys and the sentiment as the value (positive, negative, or neutral). JSON: """
                ),
                context_str=cast(TextNode, node).text,
            )
            # node.metadata["excerpt_keywords"] = keywords
            metadata_list.append({"excerpt_keywords": keywords.strip()})
        return metadata_list