from dotenv import load_dotenv
from langchain import OpenAI, LLMChain, PromptTemplate, SagemakerEndpoint
from langchain.chains import RetrievalQAWithSourcesChain, RetrievalQA
from src.vector_store import store
from src.content_handler import ContentHandler

load_dotenv()

# llm = OpenAI(temperature=0.1)
llm = SagemakerEndpoint(
    endpoint_name="meta-textgeneration-llama-2-7b-f-2023-09-20-13-35-02-360",
    credentials_profile_name="sandbox-dev",
    region_name="us-east-1",
    model_kwargs={"max_new_tokens": 700, "top_p": 0.9, "temperature": 0.2},
    endpoint_kwargs={"CustomAttributes": 'accept_eula=true'},
    content_handler=ContentHandler()
)
template = """
    You are a world class researcher, excellent at answering quesions based on snippets of data from websites and pdfs.
    Given the following snippets of data and a question, create a final answer.
    If you don't know the answer, just say that you don't know. Don't try to make up an answer.
    
    QUESTION: {question}
    =========
    CONTENT: {summaries}
    =========
    FINAL ANSWER:
"""
prompt = PromptTemplate(template=template, input_variables=['summaries', 'question'])
llm_chain = RetrievalQAWithSourcesChain.from_llm(
    llm=llm,
    retriever=store.as_retriever(search_kwargs={"k": 3}),
    combine_prompt=prompt,
    return_source_documents=True,
)