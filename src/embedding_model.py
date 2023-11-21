from langchain.embeddings.base import Embeddings
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings


class EmbeddingModel:
    _model: Embeddings = None

    @staticmethod
    def get_model() -> Embeddings:
        if not EmbeddingModel._model:
            print("Creating embedding model")
            
            EmbeddingModel._model = OpenAIEmbeddings()
            # EmbeddingModel._model = HuggingFaceInstructEmbeddings(
            #     model_name="/home/grey/code/models/instructor-xl",
            #     model_kwargs={"device": "cpu"},
            # )
        return EmbeddingModel._model
