from src.llm import LLM
from src.vector_store import VectorStore
from time import time
import sys

print("-----------CURRENT AVAILABLE SOURCES----------")
print(VectorStore().get_sources())
question = (
    sys.argv[1]
    if len(sys.argv) > 1
    else "Who were the Source Allies blackbelts in 2023?"
)
print("-----------QUESTION----------")
print(question)
starttime = time()
sources = []
print("-----------ANSWER----------")
for resp in LLM.get_chain().stream({"question": question}):
    if("answer" in resp):
        print(resp["answer"].content, end="", flush=True)
    if("context" in resp):
        sources = resp["context"]

print("")
print("-----------USED SOURCES----------")
print(list({d.metadata["source"] for d in sources}))
print(f"Seconds Taken: {time() - starttime}")