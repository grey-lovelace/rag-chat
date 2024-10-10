from langchain.embeddings.base import Embeddings
from langchain_community.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings, BedrockEmbeddings
import boto3

import nltk
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')
class EmbeddingModel:
    _model: Embeddings = None

    @staticmethod
    def get_model() -> Embeddings:
        if not EmbeddingModel._model:
            print("Creating embedding model")
            
            # EmbeddingModel._model = OpenAIEmbeddings()
            
            BEDROCK_CLIENT = boto3.client("bedrock-runtime", 'us-east-1')
            EmbeddingModel._model = BedrockEmbeddings(
                model_id="amazon.titan-embed-text-v2:0",
                client=BEDROCK_CLIENT
            )
        return EmbeddingModel._model
