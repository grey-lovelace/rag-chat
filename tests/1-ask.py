from src.llm import LLM
from src.vector_store import VectorStore
from time import time
import sys

print("-----------CURRENT AVAIALBLE SOURCES----------")
print(VectorStore().get_sources())
question = (
    sys.argv[1]
    if len(sys.argv) > 1
    else "Who were the Source Allies blackbelts in 2023?"
)
print("-----------QUESTION----------")
print(question)
starttime = time()
resp = LLM.get_chain().invoke({"question": question})
print("-----------ANSWER----------")
print(resp["answer"].content)
print("-----------USED SOURCES----------")
print(list({d.metadata["source"] for d in resp["context"]}))
print(f"Seconds Taken: {time() - starttime}")
