from dotenv import load_dotenv
from langchain import LLMChain, PromptTemplate
from langchain.llms import Bedrock, OpenAI, SagemakerEndpoint
from langchain.chains import RetrievalQAWithSourcesChain, RetrievalQA
# from langchain import globals
from src.vector_store import VectorStore
from src.content_handler import ContentHandler
import boto3

class LLM:
    _llm_chain = None

    @staticmethod
    def _get_llm() -> RetrievalQAWithSourcesChain:
            load_dotenv()

            llm = OpenAI(temperature=0.2)
            # llm = SagemakerEndpoint(0
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
    def get_chain() -> RetrievalQAWithSourcesChain:
        if not LLM._llm_chain:
            # other = "\n\nHuman: <paragraph> \n\"In 1758, the Swedish botanist and zoologist Carl Linnaeus published in his Systema Naturae, the two-word naming of species (binomial nomenclature). Canis is the Latin word meaning \"dog\", and under this genus, he listed the domestic dog, the wolf, and the golden jackal.\"\n</paragraph>\n\nAssistant:"
            # resp = LLM._get_llm().invoke(other)
            # print(resp)
            template = """    
                You are an expert about the Travel Insurance Agency Travelex. You are excellent at answering quesions based on snippets of data from websites.
                Given the following snippets of data and a question, create a final answer.
                You are a friendly and helpful assistant.
                If you don't know the answer, just say that you don't know. Don't try to make up an answer.
                
                QUESTION: {question}
                =========
                CONTENT: {summaries}
                =========
                FINAL ANSWER: Let me think a moment...
            """
            prompt = PromptTemplate(
                template=template, input_variables=["summaries", "question"]
            )

            LLM._llm_chain = RetrievalQAWithSourcesChain.from_llm(
                llm=LLM._get_llm(),
                retriever=VectorStore.get_store().as_retriever(search_kwargs={"k": 5}),
                combine_prompt=prompt,
                return_source_documents=True,
                verbose=True
            )
        return LLM._llm_chain
