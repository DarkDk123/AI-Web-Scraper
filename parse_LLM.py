# _____Imports__________
import logging
import os
from typing import Generator

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint

# _____Load Environment Variables_____
load_dotenv()

# Build logger
logger: logging.Logger = logging.getLogger("parser")
logging.basicConfig(level=logging.INFO)


template = """
You are tasked with extracting specific information from the following text content: {dom_content}. 
    Please follow these instructions carefully:


    1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. 

    2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. 

    3. **Empty Response:** If no information matches the description, return an empty string ('').

    4. "**Beautiful Markdown:** Format your response mostly in tables and Lists

    5. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text.

    Please return only extracted data, nothing else, no description!
"""

prompt = PromptTemplate.from_template(template)


LLM: HuggingFaceEndpoint = HuggingFaceEndpoint(
    repo_id=os.environ["HUGGINGFACE_MODEL_ID"],
    task="text-generation",
    repetition_penalty=1.03,
    temperature=0.8,
    streaming=True,
)  # type: ignore


chain = prompt | LLM


def parse_chunks_with_HF_LLM(
    dom_chunks: Generator[str, None, None], parse_description: str
):
    """
    Parse a generator of HTML DOM chunks with a given parse description.

    This function takes a generator of HTML DOM chunks and a parse description, and
    uses the `chain` to extract the relevant information from the chunks.

    Args:
        dom_chunks: A generator of HTML chunks.
        parse_description: A description of the information to extract from the
            chunks.

    Yields:
        str: The extracted information from each chunk.

    """


    for i, chunk in enumerate(dom_chunks, start=1):
        response = chain.stream(
            {"dom_content": chunk, "parse_description": parse_description}
        )

        logger.info(f"Parsed batch: {i}")

        yield response

