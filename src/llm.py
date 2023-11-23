from dotenv import load_dotenv
from operator import itemgetter
from langchain import LLMChain, PromptTemplate
from langchain.llms import Bedrock, OpenAI, SagemakerEndpoint
from langchain.chains import RetrievalQAWithSourcesChain, RetrievalQA
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough, RunnableMap
from langchain.schema import format_document
from langchain.chat_models import ChatOpenAI
# from langchain import globals
from src.vector_store import VectorStore
from src.content_handler import ContentHandler
from langchain.schema.output_parser import StrOutputParser
import boto3

class LLM:
    _llm_chain = None

    @staticmethod
    def _get_llm() -> RetrievalQAWithSourcesChain:
            load_dotenv()

            llm = ChatOpenAI(temperature=0.2)
            # llm = SagemakerEndpoint(
            #     endpoint_name="meta-textgeneration-llama-2-7b-f-2023-10-09-15-17-41-081",
            #     credentials_profile_name="dev",
            #     region_name="us-east-1",
            #     model_kwargs={"max_new_tokens": 700, "top_p": 0.9, "temperature": 0.2},
            #     endpoint_kwargs={"CustomAttributes": "accept_eula=true"},
            #     content_handler=ContentHandler(),
            # )
            # boto3.setup_default_session(profile_name='dev')
            # BEDROCK_CLIENT = boto3.client("bedrock-runtime", 'us-east-1')
            # llm = Bedrock(
            #     credentials_profile_name="dev",
            #     model_id="anthropic.claude-instant-v1",
            #     client=BEDROCK_CLIENT
            # )
            return llm

    @staticmethod
    def get_chain():
        if not LLM._llm_chain:
            template = """    
                You are an expert about the Travel Insurance Agency Travelex. You are excellent at answering quesions based on snippets of data from websites.
                Given the following snippets of data and a question, create a final answer.
                You are a friendly and helpful assistant.
                If you don't know the answer, just say that you don't know. Don't try to make up an answer.
                
                QUESTION: {question}
                =========
                CONTENT: {context}
                =========
                FINAL ANSWER: Let me think a moment...
            """
            prompt = ChatPromptTemplate.from_template(template)
            retriever = VectorStore.get_store().as_retriever()
            LLM._llm_chain = (
                {
                    "context": itemgetter("question") | retriever,
                    "question": itemgetter("question")
                }
                | RunnablePassthrough()
                | {
                    "answer": prompt | LLM._get_llm(),
                    "context": itemgetter("context")
                }
            )
            
        return LLM._llm_chain