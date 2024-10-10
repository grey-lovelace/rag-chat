from dotenv import load_dotenv
from operator import itemgetter
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableParallel
from langchain_community.chat_models import BedrockChat
from langchain.memory import PostgresChatMessageHistory
from langchain_community.chat_models import ChatOpenAI
from langchain.llms.base import LLM
from phoenix.trace.langchain import LangChainInstrumentor
from src.vector_store import VectorStore
import boto3


class LLM:
    _llm_chain = None

    @staticmethod
    def _get_llm() -> LLM:
        load_dotenv()

        # OPENAI
        # llm = ChatOpenAI(temperature=0.2)

        # BEDROCK
        BEDROCK_CLIENT = boto3.client("bedrock-runtime", "us-east-1")
        llm = BedrockChat(
            client=BEDROCK_CLIENT,
            model_id="anthropic.claude-3-sonnet-20240229-v1:0",
            model_kwargs={"max_tokens": 1000, "temperature": 0.2, "top_p": 0.9},
        )

        # Set up integration with Phoenix traces
        LangChainInstrumentor().instrument()

        return llm

    @staticmethod
    def get_history(session_id: str):
        return PostgresChatMessageHistory(
            connection_string="postgresql://postgres:postgres@localhost/postgres",
            session_id=session_id,
        )

    @staticmethod
    def get_chain():
        # SAI
        system_prompt = """
            You are a friendly and helpful assistant.
            You are an expert on underwriting rules and manual information for the insurance company Farm Bureau.
            Given a question from someone and documents/information pulled from the underwriting manuals, create a well thought out answer.
            Please only answer the last question asked. Answer the question only if you know the answer or can make a well-informed guess; otherwise tell me you don't know.
        """
        if not LLM._llm_chain:
            prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        f"""
                        Here are some documents for you to reference for your task:

                        <docs>
                        {{context}}
                        </docs>
                        
                        {system_prompt}
            """
                    ),
                    ("human", "{question}"),
                ]
            )
            retriever = VectorStore.get_store().as_retriever()

            LLM._llm_chain = (
                RunnableParallel({
                    "context": itemgetter("question") | retriever,
                    "question": itemgetter("question"),
                })
                | {
                    "answer": prompt | LLM._get_llm(),
                    "context": itemgetter("context")
                }
            )

        return LLM._llm_chain
