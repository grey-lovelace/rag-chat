from src.llm import llm_chain
from src.get_vector_sources import get_vector_sources
from datetime import datetime

print("Current sources")
print(get_vector_sources())
print(datetime.now())
print(llm_chain({"question": "Who were Source Allies's black belts this year?"}))
print(datetime.now())
