from crewai import LLM

class MyLLM():
    
    # Definir o modelo LLM
    gpt_mini 				= LLM(model="gpt-4o-mini")
    gpt4o_mini 				= LLM(model="gpt-4o-mini")
    gpt4o_mini_2024_07_18 	= LLM(model="gpt-4o-mini-2024-07-18")
    gpt_4o_2024_08_06 		= LLM(model="gpt-4o-2024-08-06")
    gpt4o 					= LLM(model="gpt-4o")
    gpt_o1 					= LLM(model="o1-preview")
    gpt_o1_mini 			= LLM(model="o1-mini")
    Ollama_llama_3_1 		= LLM(model="ollama/llama3.1", base_url="http://localhost:1140/openai-8B")