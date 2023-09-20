from dotenv import load_dotenv
from langchain import OpenAI, LLMChain, PromptTemplate, SagemakerEndpoint
from langchain.chains import RetrievalQAWithSourcesChain
from src.vector_store import store
from src.content_handler import ContentHandler

load_dotenv()

# llm = OpenAI(temperature=0.1)
llm = SagemakerEndpoint(
    endpoint_name="meta-textgeneration-llama-2-7b-f-2023-09-19-21-55-05-593",
    credentials_profile_name="AdministratorAccess-144406111952",
    region_name="us-east-1",
    model_kwargs={"max_new_tokens": 700, "top_p": 0.9, "temperature": 0.1},
    endpoint_kwargs={"CustomAttributes": 'accept_eula=true'},
    content_handler=ContentHandler()
)
llm_chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=store.as_retriever())
