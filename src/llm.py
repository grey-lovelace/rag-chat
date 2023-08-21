from dotenv import load_dotenv
from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.chains import RetrievalQAWithSourcesChain
from src.vector_store import store

load_dotenv()

llm = OpenAI(temperature=0.1)
llm_chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=store.as_retriever())