from src.llm import llm_chain
from src.get_vector_sources import get_vector_sources
from datetime import datetime

print("Current sources")
print(get_vector_sources())
print(datetime.now())
resp = llm_chain({"question": "Who were the Source Allies blackbelts in 2023?"})
print(resp['answer'])
print(datetime.now())
