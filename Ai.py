# # # AI Chatbot for Johan's Anxiety & Panic Support System
# # # Modified to handle multiple PDFs using PyMuPDF and support Dutch/English memory

# # # import os
# # # import fitz  # PyMuPDF
# # # import json
# # # import langdetect
# # # import glob
# # # from dotenv import load_dotenv
# # # from langchain_community.vectorstores import FAISS
# # # from langchain_openai import OpenAIEmbeddings
# # # from langchain_text_splitters import RecursiveCharacterTextSplitter
# # # from langchain_openai import ChatOpenAI
# # # from langchain.schema import HumanMessage, SystemMessage, AIMessage
# # # from langchain_core.documents import Document

# # # # Load environment variables
# # # load_dotenv()
# # # os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

# # # # Function to extract text from all PDFs in a folder
# # # def extract_text_from_all_pdfs(folder_path):
# # #     combined_texts = []
# # #     pdf_files = glob.glob(os.path.join(folder_path, "*.pdf"))

# # #     for pdf_file in pdf_files:
# # #         try:
# # #             with fitz.open(pdf_file) as doc:
# # #                 text = ""
# # #                 for page in doc:
# # #                     text += page.get_text() + "\n"
# # #                 combined_texts.append(Document(page_content=text.strip()))
# # #                 print(f"✅ Loaded: {os.path.basename(pdf_file)}")
# # #         except Exception as e:
# # #             print(f"❌ Failed to process {pdf_file}: {e}")

# # #     return combined_texts

# # # # Load and prepare multiple PDF documents
# # # pdf_folder = "data"
# # # documents = extract_text_from_all_pdfs(pdf_folder)

# # # # Split documents into chunks
# # # text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# # # split_docs = text_splitter.split_documents(documents)

# # # # FAISS Vector Store
# # # faiss_path = "faiss_db_johan"
# # # if os.path.exists(faiss_path):
# # #     vectordb = FAISS.load_local(faiss_path, OpenAIEmbeddings(), allow_dangerous_deserialization=True)
# # # else:
# # #     vectordb = FAISS.from_documents(split_docs, OpenAIEmbeddings())
# # #     vectordb.save_local(faiss_path)

# # # retriever = vectordb.as_retriever(search_kwargs={"k": 3})

# # # # GPT-4 Chat Model
# # # llm = ChatOpenAI(model="gpt-4", temperature=0.6)

# # # # System prompts
# # # system_prompt_dutch = SystemMessage(content="""
# # # You are a compassionate, friendly, and insightful virtual psychologist specializing in helping people deal with anxiety and panic. 
# # # Your advice is based on Johan’s personal books and courses on mental health. You must respond in a supportive, empathetic, and easy-to-understand way in plain Dutch.
# # # Keep a calm, positive, and solution-focused tone. If you don’t have enough information, say so politely and suggest speaking to a professional.
# # # """)

# # # system_prompt_english = SystemMessage(content="""
# # # You are a compassionate, friendly, and insightful virtual psychologist specializing in helping people deal with anxiety and panic. 
# # # Your advice is based on Johan’s personal books and courses on mental health. You must respond in a supportive, empathetic, and easy-to-understand way in English.
# # # Keep a calm, positive, and solution-focused tone. If you don’t have enough information, say so politely and suggest speaking to a professional.
# # # """)

# # # # Detect language from input text
# # # def detect_language(text):
# # #     try:
# # #         lang = langdetect.detect(text)
# # #         return "nl" if lang == "nl" else "en"
# # #     except:
# # #         return "en"

# # # # Memory for current session
# # # chat_memory = []

# # # # Prompt Template for AI Chatbot
# # # def get_rag_response(user_input):
# # #     context = retriever.invoke(user_input)
# # #     info = "\n".join([doc.page_content for doc in context])
# # #     lang = detect_language(user_input)

# # #     if lang == "nl":
# # #         system_prompt = system_prompt_dutch
# # #         prompt = f'''
# # # Gebruik de volgende context uit Johan's boeken om een ondersteunend en duidelijk antwoord te geven in eenvoudig Nederlands.

# # # Kennisbank:
# # # {info}

# # # Vraag van gebruiker:
# # # {user_input}

# # # Antwoord:
# # # '''
# # #     else:
# # #         system_prompt = system_prompt_english
# # #         prompt = f'''
# # # Use the following context from Johan's books to provide a supportive and clear answer in simple English.

# # # Knowledge Base:
# # # {info}

# # # User's question:
# # # {user_input}

# # # Answer:
# # # '''

# # #     # Build full context from memory
# # #     messages = [system_prompt] + chat_memory + [HumanMessage(content=prompt)]
# # #     response = llm.invoke(messages)

# # #     # Update chat memory
# # #     chat_memory.append(HumanMessage(content=user_input))
# # #     chat_memory.append(AIMessage(content=response.content))

# # #     return response.content

# # # # Example Interaction
# # # def chat():
# # #     print("Welcome to Johan's Virtual Psychologist. Feel free to ask your question in Dutch or English.")
# # #     while True:
# # #         user_input = input("\nYou: ").strip()
# # #         if user_input.lower() in ["exit", "quit"]:
# # #             print("Goodbye! Take care of yourself.")
# # #             break
# # #         answer = get_rag_response(user_input)
# # #         print(f"\n🤖 Answer: {answer}")

# # # if __name__ == "__main__":
# # #     chat()







# # # AI Chatbot for Johan's Anxiety & Panic Support System
# # # Modified to handle multiple PDFs using PyMuPDF and support Dutch/English memory

# # import os
# # import fitz  # PyMuPDF
# # import json
# # import langdetect
# # import glob
# # from dotenv import load_dotenv
# # from langchain_community.vectorstores import FAISS
# # from langchain_openai import OpenAIEmbeddings
# # from langchain_text_splitters import RecursiveCharacterTextSplitter
# # from langchain_openai import ChatOpenAI
# # from langchain.schema import HumanMessage, SystemMessage, AIMessage
# # from langchain_core.documents import Document

# # # Load environment variables
# # load_dotenv()
# # os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

# # # Function to extract text from all PDFs in a folder
# # def extract_text_from_all_pdfs(folder_path):
# #     combined_texts = []
# #     pdf_files = glob.glob(os.path.join(folder_path, "*.pdf"))

# #     for pdf_file in pdf_files:
# #         try:
# #             with fitz.open(pdf_file) as doc:
# #                 text = ""
# #                 for page in doc:
# #                     text += page.get_text() + "\n"
# #                 combined_texts.append(Document(page_content=text.strip()))
# #                 print(f"✅ Loaded: {os.path.basename(pdf_file)}")
# #         except Exception as e:
# #             print(f"❌ Failed to process {pdf_file}: {e}")

# #     return combined_texts

# # # Load and prepare multiple PDF documents
# # pdf_folder = "data"
# # documents = extract_text_from_all_pdfs(pdf_folder)

# # # Split documents into chunks
# # text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# # split_docs = text_splitter.split_documents(documents)

# # # FAISS Vector Store
# # faiss_path = "faiss_db_johan"
# # if os.path.exists(faiss_path):
# #     print("📂 Existing FAISS database found. Loading it...")
# #     vectordb = FAISS.load_local(faiss_path, OpenAIEmbeddings(), allow_dangerous_deserialization=True)
# # else:
# #     print("📦 No FAISS found. Creating new one...")
# #     vectordb = FAISS.from_documents(split_docs, OpenAIEmbeddings())
# #     vectordb.save_local(faiss_path)
# #     print("✅ FAISS database saved.")

# # retriever = vectordb.as_retriever(search_kwargs={"k": 3})

# # # GPT-4 Chat Model
# # llm = ChatOpenAI(model="gpt-4", temperature=0.6)

# # # System prompts
# # system_prompt_dutch = SystemMessage(content="""
# # You are a compassionate, friendly, and insightful virtual psychologist specializing in helping people deal with anxiety and panic. 
# # Your advice is based on Johan’s personal books and courses on mental health. You must respond in a supportive, empathetic, and easy-to-understand way in plain Dutch.
# # Keep a calm, positive, and solution-focused tone. If you don’t have enough information, say so politely and suggest speaking to a professional.
# # """)

# # system_prompt_english = SystemMessage(content="""
# # You are a compassionate, friendly, and insightful virtual psychologist specializing in helping people deal with anxiety and panic. 
# # Your advice is based on Johan’s personal books and courses on mental health. You must respond in a supportive, empathetic, and easy-to-understand way in English.
# # Keep a calm, positive, and solution-focused tone. If you don’t have enough information, say so politely and suggest speaking to a professional.
# # """)

# # # Detect language from input text
# # def detect_language(text):
# #     try:
# #         lang = langdetect.detect(text)
# #         return "nl" if lang == "nl" else "en"
# #     except:
# #         return "en"

# # # Memory for current session
# # chat_memory = []

# # # Prompt Template for AI Chatbot
# # def get_rag_response(user_input):
# #     context = retriever.invoke(user_input)
# #     info = "\n".join([doc.page_content for doc in context])
# #     lang = detect_language(user_input)

# #     if lang == "nl":
# #         system_prompt = system_prompt_dutch
# #         prompt = f'''
# # Gebruik de volgende context uit Johan's boeken om een ondersteunend en duidelijk antwoord te geven in eenvoudig Nederlands.

# # Kennisbank:
# # {info}

# # Vraag van gebruiker:
# # {user_input}

# # Antwoord:
# # '''
# #     else:
# #         system_prompt = system_prompt_english
# #         prompt = f'''
# # Use the following context from Johan's books to provide a supportive and clear answer in simple English.

# # Knowledge Base:
# # {info}

# # User's question:
# # {user_input}

# # Answer:
# # '''

# #     # Build full context from memory
# #     messages = [system_prompt] + chat_memory + [HumanMessage(content=prompt)]
# #     response = llm.invoke(messages)

# #     # Update chat memory
# #     chat_memory.append(HumanMessage(content=user_input))
# #     chat_memory.append(AIMessage(content=response.content))

# #     return response.content

# # # Example Interaction
# # def chat():
# #     print("Welcome to Johan's Virtual Psychologist. Feel free to ask your question in Dutch or English.")
# #     while True:
# #         user_input = input("\nYou: ").strip()
# #         if user_input.lower() in ["exit", "quit"]:
# #             print("Goodbye! Take care of yourself.")
# #             break
# #         answer = get_rag_response(user_input)
# #         print(f"\n🤖 Answer: {answer}")

# # if __name__ == "__main__":
# #     chat()





# # import os
# # import fitz  # PyMuPDF
# # import json
# # import langdetect
# # import glob
# # from dotenv import load_dotenv
# # from langchain_community.vectorstores import FAISS
# # from langchain_openai import OpenAIEmbeddings
# # from langchain_text_splitters import RecursiveCharacterTextSplitter
# # from langchain_openai import ChatOpenAI
# # from langchain.schema import HumanMessage, SystemMessage, AIMessage
# # from langchain_core.documents import Document

# # # Load environment variables
# # load_dotenv()
# # os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

# # # Function to extract text from all PDFs in a folder
# # def extract_text_from_all_pdfs(folder_path):
# #     combined_texts = []
# #     pdf_files = glob.glob(os.path.join(folder_path, "*.pdf"))

# #     for pdf_file in pdf_files:
# #         try:
# #             with fitz.open(pdf_file) as doc:
# #                 text = ""
# #                 for page in doc:
# #                     text += page.get_text() + "\n"
# #                 combined_texts.append(Document(page_content=text.strip()))
# #                 print(f"✅ Loaded: {os.path.basename(pdf_file)}")
# #         except Exception as e:
# #             print(f"❌ Failed to process {pdf_file}: {e}")

# #     return combined_texts

# # # Load and prepare multiple PDF documents
# # pdf_folder = "data"
# # documents = extract_text_from_all_pdfs(pdf_folder)

# # # Split documents into chunks
# # text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# # split_docs = text_splitter.split_documents(documents)

# # # FAISS Vector Store
# # faiss_path = "faiss_db_johan"
# # if os.path.exists(faiss_path):
# #     print("📂 Existing FAISS database found. Loading it...")
# #     vectordb = FAISS.load_local(faiss_path, OpenAIEmbeddings(), allow_dangerous_deserialization=True)
# # else:
# #     print("📦 No FAISS found. Creating new one...")
# #     vectordb = FAISS.from_documents(split_docs, OpenAIEmbeddings())
# #     vectordb.save_local(faiss_path)
# #     print("✅ FAISS database saved.")

# # retriever = vectordb.as_retriever(search_kwargs={"k": 3})

# # # GPT-4 Chat Model
# # llm = ChatOpenAI(model="gpt-4", temperature=0.6)

# # # System prompts
# # system_prompt_english = SystemMessage(content="""
# # You are a compassionate, friendly, and insightful virtual psychologist, specializing in helping people deal with anxiety and mental discomfort. 
# # Your advice is based on Johan's "Mental Blueprint" and "Workbook" books and methods.
# # You must respond in a supportive, empathetic, and easy-to-understand way in English.

# # Instructions:
# # 1. When a user mentions anxiety or mental discomfort, identify it.
# #    - Ask the user: "Have you already created your 'Mental Blueprint'?"

# # 2. If the user has not created their 'Mental Blueprint', instruct them to create it first and stop the process there.

# # 3. If the user has already created their 'Mental Blueprint', only then proceed with addressing their anxiety issue. However, first validate the user's self-awareness before providing the proper assistance.

# # 4. Never give irrelevant or direct answers. The AI must first check the user's process of self-understanding before providing the correct support.

# # 5. Only use the resources from "Mental Blueprint" and "Workbook". Do not use any other books or methods (such as mindfulness or relaxation techniques), unless explicitly authorized.

# # Respond in a calm, positive, and solution-focused tone. If you don’t have enough information, say so politely and suggest speaking to a professional.
# # """)

# # system_prompt_dutch = SystemMessage(content="""
# # Je bent een compassievolle, vriendelijke en inzichtelijke virtuele psycholoog, gespecialiseerd in het helpen van mensen met angst en paniek. 
# # Je advies is gebaseerd op Johan's "Mental Blueprint" en "Workbook" boeken en methodes.
# # Je moet op een ondersteunende, empathische en makkelijk te begrijpen manier reageren in het Nederlands.

# # Instructies:
# # 1. Wanneer een gebruiker aangeeft angst of mentale ongemakken te ervaren, identificeer dit.
# #    - Vraag de gebruiker: "Heb je al een 'Mental Blueprint' gemaakt?"

# # 2. Als de gebruiker geen 'Mental Blueprint' heeft gemaakt, vraag hen dan om deze eerst te maken en stop het proces daar.

# # 3. Als de gebruiker al een 'Mental Blueprint' heeft gemaakt, ga dan pas verder met het aanpakken van hun angstprobleem. Valideer echter eerst het zelfbewustzijn van de gebruiker voordat je de juiste hulp biedt.

# # 4. Geef nooit irrelevante of directe antwoorden. De AI moet eerst het zelfbegrip van de gebruiker verifiëren voordat hij de juiste ondersteuning biedt.

# # 5. Gebruik alleen de bronnen van "Mental Blueprint" en "Workbook". Gebruik geen andere boeken of methodes (zoals mindfulness of ontspanningstechnieken), tenzij dit expliciet is toegestaan.

# # Reageer op een kalme, positieve en oplossingsgerichte manier. Als je niet genoeg informatie hebt, zeg dit dan beleefd en stel voor om met een professional te praten.
# # """)

# # # Detect language from input text
# # def detect_language(text):
# #     try:
# #         lang = langdetect.detect(text)
# #         return "nl" if lang == "nl" else "en"
# #     except:
# #         return "en"

# # # Memory for current session
# # chat_memory = []

# # # New function to detect if the user has created a mental blueprint
# # def ask_about_mental_blueprint(user_input):
# #     # Here we check if the user has already created their mental blueprint
# #     if "mental blueprint" in user_input.lower():
# #         return "Yes, it seems like you've started working on your mental blueprint. Well done!"
# #     else:
# #         return """It's an important first step in understanding your anxiety. Have you already created your mental blueprint? 
# # This process helps you understand the root cause of your anxiety and allows you to create a strategy to deal with it."""

# # # Prompt Template for AI Chatbot
# # def get_rag_response(user_input):
# #     # Ask about the mental blueprint first
# #     blueprint_response = ask_about_mental_blueprint(user_input)
    
# #     # Now, retrieve context from the FAISS database
# #     context = retriever.invoke(user_input)
# #     info = "\n".join([doc.page_content for doc in context])
# #     lang = detect_language(user_input)

# #     if lang == "nl":
# #         system_prompt = system_prompt_dutch
# #         prompt = f'''
# # Gebruik de volgende context uit Johan's boeken om een ondersteunend en duidelijk antwoord te geven in eenvoudig Nederlands.

# # Kennisbank:
# # {info}

# # Vraag van gebruiker:
# # {user_input}

# # Antwoord:
# # '''
# #     else:
# #         system_prompt = system_prompt_english
# #         prompt = f'''
# # Use the following context from Johan's books to provide a supportive and clear answer in simple English.

# # Knowledge Base:
# # {info}

# # User's question:
# # {user_input}

# # Answer:
# # '''

# #     # Build full context from memory
# #     messages = [system_prompt] + chat_memory + [HumanMessage(content=prompt)]
# #     response = llm.invoke(messages)

# #     # Update chat memory
# #     chat_memory.append(HumanMessage(content=user_input))
# #     chat_memory.append(AIMessage(content=response.content))

# #     # Return the response
# #     return blueprint_response + "\n" + response.content

# # # Example Interaction
# # def chat():
# #     print("Welcome to Johan's Virtual Psychologist. Feel free to ask your question in Dutch or English.")
# #     while True:
# #         user_input = input("\nYou: ").strip()
# #         if user_input.lower() in ["exit", "quit"]:
# #             print("Goodbye! Take care of yourself.")
# #             break
# #         answer = get_rag_response(user_input)
# #         print(f"\n🤖 Answer: {answer}")

# # if __name__ == "__main__":
# #     chat()





# import os
# import fitz  # PyMuPDF
# import json
# import langdetect
# import glob
# from dotenv import load_dotenv
# from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_openai import ChatOpenAI
# from langchain.schema import HumanMessage, SystemMessage, AIMessage
# from langchain_core.documents import Document

# # Load environment variables
# load_dotenv()
# os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

# # Function to extract text from all PDFs in a folder
# def extract_text_from_all_pdfs(folder_path):
#     combined_texts = []
#     pdf_files = glob.glob(os.path.join(folder_path, "*.pdf"))

#     for pdf_file in pdf_files:
#         try:
#             with fitz.open(pdf_file) as doc:
#                 text = ""
#                 for page in doc:
#                     text += page.get_text() + "\n"
#                 combined_texts.append(Document(page_content=text.strip()))
#                 print(f"✅ Loaded: {os.path.basename(pdf_file)}")
#         except Exception as e:
#             print(f"❌ Failed to process {pdf_file}: {e}")

#     return combined_texts

# # Load and prepare multiple PDF documents
# pdf_folder = "data"
# documents = extract_text_from_all_pdfs(pdf_folder)

# # Split documents into chunks
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# split_docs = text_splitter.split_documents(documents)

# # FAISS Vector Store
# faiss_path = "faiss_db_johan"
# if os.path.exists(faiss_path):
#     print("📂 Existing FAISS database found. Loading it...")
#     vectordb = FAISS.load_local(faiss_path, OpenAIEmbeddings(), allow_dangerous_deserialization=True)
# else:
#     print("📦 No FAISS found. Creating new one...")
#     vectordb = FAISS.from_documents(split_docs, OpenAIEmbeddings())
#     vectordb.save_local(faiss_path)
#     print("✅ FAISS database saved.")

# retriever = vectordb.as_retriever(search_kwargs={"k": 3})

# # GPT-4 Chat Model
# llm = ChatOpenAI(model="gpt-4", temperature=0.6)

# # System prompts based on client feedback:
# system_prompt_english = SystemMessage(content="""
# You are a compassionate, friendly, and insightful virtual psychologist, specializing in helping people deal with anxiety and mental discomfort. 
# Your advice is based on Johan's "Mental Blueprint" and "Workbook" books and methods.
# You must respond in a supportive, empathetic, and easy-to-understand way in English.

# Instructions:
# 1. When a user mentions anxiety or mental discomfort, identify it.
#    - Ask the user: "Do you already know WHY you have these thoughts of anxiety? Have you already created your 'Mental Blueprint'?"
  
# 2. If the user has not created their 'Mental Blueprint', instruct them to create it first and stop the process there.

# 3. If the user has already created their 'Mental Blueprint', only then proceed with addressing their anxiety issue. However, first validate the user's self-awareness before providing the proper assistance.

# 4. Never give irrelevant or direct answers. The AI must first check the user's process of self-understanding before providing the correct support.

# 5. Only use the resources from "Mental Blueprint" and "Workbook". Do not use any other books or methods (such as mindfulness or relaxation techniques), unless explicitly authorized.

# Respond in a calm, positive, and solution-focused tone. If you don’t have enough information, say so politely and suggest speaking to a professional.
# """)

# system_prompt_dutch = SystemMessage(content="""
# Je bent een compassievolle, vriendelijke en inzichtelijke virtuele psycholoog, gespecialiseerd in het helpen van mensen met angst en paniek. 
# Je advies is gebaseerd op Johan's "Mental Blueprint" en "Workbook" boeken en methodes.
# Je moet op een ondersteunende, empathische en makkelijk te begrijpen manier reageren in het Nederlands.

# Instructies:
# 1. Wanneer een gebruiker aangeeft angst of mentale ongemakken te ervaren, identificeer dit.
#    - Vraag de gebruiker: "Weet je al WAAROM je deze gedachten van angst hebt? Heb je al je 'Mental Blueprint' gemaakt?"
  
# 2. Als de gebruiker geen 'Mental Blueprint' heeft gemaakt, vraag hen dan om deze eerst te maken en stop het proces daar.

# 3. Als de gebruiker al een 'Mental Blueprint' heeft gemaakt, ga dan pas verder met het aanpakken van hun angstprobleem. Valideer echter eerst het zelfbewustzijn van de gebruiker voordat je de juiste hulp biedt.

# 4. Geef nooit irrelevante of directe antwoorden. De AI moet eerst het zelfbegrip van de gebruiker verifiëren voordat hij de juiste ondersteuning biedt.

# 5. Gebruik alleen de bronnen van "Mental Blueprint" en "Workbook". Gebruik geen andere boeken of methodes (zoals mindfulness of ontspanningstechnieken), tenzij dit expliciet is toegestaan.

# Reageer op een kalme, positieve en oplossingsgerichte manier. Als je niet genoeg informatie hebt, zeg dit dan beleefd en stel voor om met een professional te praten.
# """)

# # Detect language from input text
# def detect_language(text):
#     try:
#         lang = langdetect.detect(text)
#         return "nl" if lang == "nl" else "en"
#     except:
#         return "en"

# # Memory for current session
# chat_memory = []

# # New function to detect if the user has created a mental blueprint
# def ask_about_mental_blueprint(user_input):
#     # Here we check if the user has already created their mental blueprint
#     if "mental blueprint" in user_input.lower():
#         return "Yes, it seems like you've started working on your mental blueprint. Well done!"
#     else:
#         return """It's an important first step in understanding your anxiety. Have you already created your mental blueprint? 
# This process helps you understand the root cause of your anxiety and allows you to create a strategy to deal with it."""

# # Prompt Template for AI Chatbot
# def get_rag_response(user_input):
#     # Ask about the mental blueprint first
#     blueprint_response = ask_about_mental_blueprint(user_input)
    
#     # Now, retrieve context from the FAISS database
#     context = retriever.invoke(user_input)
#     info = "\n".join([doc.page_content for doc in context])
#     lang = detect_language(user_input)

#     if lang == "nl":
#         system_prompt = system_prompt_dutch
#         prompt = f'''
# Gebruik de volgende context uit Johan's boeken om een ondersteunend en duidelijk antwoord te geven in eenvoudig Nederlands.

# Kennisbank:
# {info}

# Vraag van gebruiker:
# {user_input}

# Antwoord:
# '''
#     else:
#         system_prompt = system_prompt_english
#         prompt = f'''
# Use the following context from Johan's books to provide a supportive and clear answer in simple English.

# Knowledge Base:
# {info}

# User's question:
# {user_input}

# Answer:
# '''

#     # Build full context from memory
#     messages = [system_prompt] + chat_memory + [HumanMessage(content=prompt)]
#     response = llm.invoke(messages)

#     # Update chat memory
#     chat_memory.append(HumanMessage(content=user_input))
#     chat_memory.append(AIMessage(content=response.content))

#     # Return the response
#     return blueprint_response + "\n" + response.content

# # Example Interaction
# def chat():
#     print("Welcome to Johan's Virtual Psychologist. Feel free to ask your question in Dutch or English.")
#     while True:
#         user_input = input("\nYou: ").strip()
#         if user_input.lower() in ["exit", "quit"]:
#             print("Goodbye! Take care of yourself.")
#             break
#         answer = get_rag_response(user_input)
#         print(f"\n🤖 Answer: {answer}")

# if __name__ == "__main__":
#     chat()








# import os
# import fitz  # PyMuPDF
# import json
# import langdetect
# import glob
# from dotenv import load_dotenv
# from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_openai import ChatOpenAI
# from langchain.schema import HumanMessage, SystemMessage, AIMessage
# from langchain_core.documents import Document

# # Load environment variables
# load_dotenv()
# os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

# # Keyword list for anxiety or mental blueprint-related input
# ANXIETY_KEYWORDS = [
#     "anxiety", "anxious", "stress", "nervous", "panic", "worried", "fearful",
#     "mental blueprint", "blueprint", "mental discomfort", "overwhelmed"
# ]

# # Function to extract text from all PDFs in a folder/
# def extract_text_from_all_pdfs(folder_path):
#     combined_texts = []
#     pdf_files = glob.glob(os.path.join(folder_path, "*.pdf"))

#     for pdf_file in pdf_files:
#         try:
#             with fitz.open(pdf_file) as doc:
#                 text = ""
#                 for page in doc:
#                     text += page.get_text() + "\n"
#                 combined_texts.append(Document(page_content=text.strip()))
#                 print(f"✅ Loaded: {os.path.basename(pdf_file)}")
#         except Exception as e:
#             print(f"❌ Failed to process {pdf_file}: {e}")

#     return combined_texts

# # Load and prepare multiple PDF documents
# pdf_folder = "data"
# documents = extract_text_from_all_pdfs(pdf_folder)

# # Split documents into chunks
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# split_docs = text_splitter.split_documents(documents)

# # FAISS Vector Store
# faiss_path = "faiss_db_johan"
# if os.path.exists(faiss_path):
#     print("📂 Existing FAISS database found. Loading it...")
#     vectordb = FAISS.load_local(faiss_path, OpenAIEmbeddings(), allow_dangerous_deserialization=True)
# else:
#     print("📦 No FAISS found. Creating new one...")
#     vectordb = FAISS.from_documents(split_docs, OpenAIEmbeddings())
#     vectordb.save_local(faiss_path)
#     print("✅ FAISS database saved.")

# retriever = vectordb.as_retriever(search_kwargs={"k": 3})

# # GPT-4 Chat Model
# llm = ChatOpenAI(model="gpt-4", temperature=0.6)

# # System prompts based on client feedback
# system_prompt_english = SystemMessage(content="""
# You are a compassionate, friendly, and insightful virtual psychologist, specializing in helping people deal with anxiety and mental discomfort. 
# Your advice is based on Johan's "Mental Blueprint" and "Workbook" books and methods.
# You must respond in a supportive, empathetic, and easy-to-understand way in English.

# Instructions:
# 1. When a user mentions anxiety or mental discomfort, identify it.
#    - Ask the user: "Do you already know WHY you have these thoughts of anxiety? Have you already created your 'Mental Blueprint'?"
  
# 2. If the user has not created their 'Mental Blueprint', instruct them to create it first and stop the process there.

# 3. If the user has already created their 'Mental Blueprint', only then proceed with addressing their anxiety issue. However, first validate the user's self-awareness before providing the proper assistance.

# 4. Never give irrelevant or direct answers. The AI must first check the user's process of self-understanding before providing the correct support.

# 5. Only use the resources from "Mental Blueprint" and "Workbook". Do not use any other books or methods (such as mindfulness or relaxation techniques), unless explicitly authorized.

# Respond in a calm, positive, and solution-focused tone. If you don’t have enough information, say so politely and suggest speaking to a professional.
# """)

# system_prompt_dutch = SystemMessage(content="""
# Je bent een compassievolle, vriendelijke en inzichtelijke virtuele psycholoog, gespecialiseerd in het helpen van mensen met angst en paniek. 
# Je advies is gebaseerd op Johan's "Mental Blueprint" en "Workbook" boeken en methodes.
# Je moet op een ondersteunende, empathische en makkelijk te begrijpen manier reageren in het Nederlands.

# Instructies:
# 1. Wanneer een gebruiker aangeeft angst of mentale ongemakken te ervaren, identificeer dit.
#    - Vraag de gebruiker: "Weet je al WAAROM je deze gedachten van angst hebt? Heb je al je 'Mental Blueprint' gemaakt?"
  
# 2. Als de gebruiker geen 'Mental Blueprint' heeft gemaakt, vraag hen dan om deze eerst te maken en stop het proces daar.

# 3. Als de gebruiker al een 'Mental Blueprint' heeft gemaakt, ga dan pas verder met het aanpakken van hun angstprobleem. Valideer echter eerst het zelfbewustzijn van de gebruiker voordat je de juiste hulp biedt.

# 4. Geef nooit irrelevante of directe antwoorden. De AI moet eerst het zelfbegrip van de gebruiker verifiëren voordat hij de juiste ondersteuning biedt.

# 5. Gebruik alleen de bronnen van "Mental Blueprint" en "Workbook". Gebruik geen andere boeken of methodes (zoals mindfulness of ontspanningstechnieken), tenzij dit expliciet is toegestaan.

# Reageer op een kalme, positieve en oplossingsgerichte manier. Als je niet genoeg informatie hebt, zeg dit dan beleefd en stel voor om met een professional te praten.
# """)

# # Detect language from input text
# def detect_language(text):
#     try:
#         lang = langdetect.detect(text)
#         return "nl" if lang == "nl" else "en"
#     except:
#         return "en"

# # Memory for current session
# chat_memory = []

# # Modified function to detect if the user has created a mental blueprint
# def ask_about_mental_blueprint(user_input):
#     user_input_lower = user_input.lower()
    
#     # Check if input contains anxiety-related or blueprint-related keywords
#     is_anxiety_related = any(keyword in user_input_lower for keyword in ANXIETY_KEYWORDS)
    
#     if not is_anxiety_related:
#         # Return empty string if input is not anxiety-related
#         return ""
    
#     # If mental blueprint is mentioned, provide positive feedback
#     if "mental blueprint" in user_input_lower or "blueprint" in user_input_lower:
#         return "Yes, it seems like you've started working on your mental blueprint. Well done!"
    
#     # If anxiety-related but no blueprint mentioned, suggest creating one
#     return """It's an important first step in understanding your anxiety. Have you already created your mental blueprint? 
# This process helps you understand the root cause of your anxiety and allows you to create a strategy to deal with it."""

# # Modified function to get RAG response
# def get_rag_response(user_input):
#     # Check for mental blueprint
#     blueprint_response = ask_about_mental_blueprint(user_input)
    
#     # Retrieve context from FAISS database
#     context = retriever.invoke(user_input)
#     info = "\n".join([doc.page_content for doc in context])
#     lang = detect_language(user_input)

#     if lang == "nl":
#         system_prompt = system_prompt_dutch
#         prompt = f'''
# Gebruik de volgende context uit Johan's boeken om een ondersteunend en duidelijk antwoord te geven in eenvoudig Nederlands.

# Kennisbank:
# {info}

# Vraag van gebruiker:
# {user_input}

# Antwoord:
# '''
#     else:
#         system_prompt = system_prompt_english
#         prompt = f'''
# Use the following context from Johan's books to provide a supportive and clear answer in simple English.

# Knowledge Base:
# {info}

# User's question:
# {user_input}

# Answer:
# '''

#     # Build full context from memory
#     messages = [system_prompt] + chat_memory + [HumanMessage(content=prompt)]
#     response = llm.invoke(messages)

#     # Update chat memory
#     chat_memory.append(HumanMessage(content=user_input))
#     chat_memory.append(AIMessage(content=response.content))

#     # Return blueprint response (if any) combined with GPT-4 response
#     if blueprint_response:
#         return blueprint_response + "\n" + response.content
#     return response.content

# # Example Interaction
# def chat():
#     print("Welcome to Johan's Virtual Psychologist. Feel free to ask your question in Dutch or English.")
#     while True:
#         user_input = input("\nYou: ").strip()
#         if user_input.lower() in ["exit", "quit"]:
#             print("Goodbye! Take care of yourself.")
#             break
#         answer = get_rag_response(user_input)
#         print(f"\n🤖 Answer: {answer}")

# if __name__ == "__main__":
#     chat()





# import os
# import fitz  # PyMuPDF
# import json
# import langdetect
# import glob
# from dotenv import load_dotenv
# from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_openai import ChatOpenAI
# from langchain.schema import HumanMessage, SystemMessage, AIMessage
# from langchain_core.documents import Document

# # Load environment variables
# load_dotenv()
# os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

# # Keyword list for anxiety or mental blueprint-related input
# ANXIETY_KEYWORDS = [
#     "anxiety", "anxious", "stress", "nervous", "panic", "worried", "fearful",
#     "mental blueprint", "blueprint", "mental discomfort", "overwhelmed"
# ]

# # Global memory
# chat_memory = []
# user_blueprint = None
# blueprint_questions = {
#     "en": [
#         "What are you struggling with emotionally or mentally?",
#         "When do you most often experience this?",
#         "What thoughts usually accompany those feelings?",
#         "What past events might be related to these emotions?",
#         "Do you notice any current habits or routines that affect how you feel?"
#     ],
#     "nl": [
#         "Waarmee worstelt u emotioneel of mentaal?",
#         "Wanneer ervaart u dit het vaakst?",
#         "Welke gedachten gaan meestal gepaard met die gevoelens?",
#         "Welke gebeurtenissen uit het verleden kunnen verband houden met deze emoties?",
#         "Merkt u huidige gewoonten of routines op die invloed hebben op hoe u zich voelt?"
#     ]
# }
# blueprint_responses = []
# current_question_index = 0

# # Function to extract text from all PDFs in a folder
# def extract_text_from_all_pdfs(folder_path):
#     combined_texts = []
#     pdf_files = glob.glob(os.path.join(folder_path, "*.pdf"))

#     for pdf_file in pdf_files:
#         try:
#             with fitz.open(pdf_file) as doc:
#                 text = ""
#                 for page in doc:
#                     text += page.get_text() + "\n"
#                 combined_texts.append(Document(page_content=text.strip()))
#                 print(f"✅ Loaded: {os.path.basename(pdf_file)}")
#         except Exception as e:
#             print(f"❌ Failed to process {pdf_file}: {e}")

#     return combined_texts

# # Load and prepare multiple PDF documents
# pdf_folder = "data"
# documents = extract_text_from_all_pdfs(pdf_folder)

# # Split documents into chunks
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=200)
# split_docs = text_splitter.split_documents(documents)

# # FAISS Vector Store
# faiss_path = "faiss_db_johan"
# if os.path.exists(faiss_path):
#     print("📂 Existing FAISS database found. Loading it...")
#     vectordb = FAISS.load_local(faiss_path, OpenAIEmbeddings(), allow_dangerous_deserialization=True)
# else:
#     print("📦 No FAISS found. Creating new one...")
#     vectordb = FAISS.from_documents(split_docs, OpenAIEmbeddings())
#     vectordb.save_local(faiss_path)
#     print("✅ FAISS database saved.")

# retriever = vectordb.as_retriever(search_kwargs={"k": 3})

# # GPT-4 Chat Model
# llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.6)

# # System Prompts
# system_prompt_english = SystemMessage(content="""
# You are an AI chatbot designed to assist users with mental health issues based on the content of two specific books: the Main Book (001 Workbook) and the accompanying Workbook. Your primary goal is to guide users through a structured flow to identify their mental health issues and provide personalized solutions. Follow these steps for every user interaction:

# 1. **Initial Question**: Regardless of the user's question, always start by asking, "Have you created your mental blueprint yet?" This is a critical step to understand the user's mental health profile.

# 2. **If the User Has a Mental Blueprint**:
#    - Ask the user to provide details of their mental blueprint (e.g., specific mental health issues identified, triggers, or patterns).
#    - Use the provided blueprint to reference relevant sections from the Main Book and Workbook.
#    - Suggest specific exercises, techniques, or solutions from the Workbook that address the user's mental health issues.
#    - If the blueprint requires a chapter with a YouTube video, recommend watching that video before proceeding (e.g., "Please watch this video to understand more: [Insert Video Link]"). Ensure the video is relevant to the user's blueprint.
#    - If the blueprint requires visual representation, describe a diagram to illustrate the mental blueprint or suggest how it could be visualized.

# 3. **If the User Does Not Have a Mental Blueprint**:
#    - Guide the user to create a mental blueprint by asking the following series of questions, one at a time, based on Chapter 1 of the Main Book:
#      - "What are you struggling with emotionally or mentally?"
#      - "When do you most often experience this?"
#      - "What thoughts usually accompany those feelings?"
#      - "What past events might be related to these emotions?"
#      - "Do you notice any current habits or routines that affect how you feel?"
#    - Ask each question sequentially, waiting for the user's response before proceeding to the next. Store each response to build the mental blueprint.
#    - After collecting all responses, summarize the mental blueprint for the user (e.g., "Based on your answers, your mental blueprint indicates [specific issues, triggers, thoughts, past events, and habits].").
#    - If the Main Book references a YouTube video for creating the blueprint, instruct the user to watch it (e.g., "Please watch this introductory video on mental blueprints: [Insert Video Link]").
#    - Proceed to suggest exercises or solutions from the Workbook tailored to the newly created blueprint.
#    - If visuals are required, describe a diagram to represent the mental blueprint.

# 4. **Maintaining the Flow**:
#    - Never provide direct answers to the user's questions without following the mental blueprint process.
#    - Ensure responses are conversational, empathetic, and clear, guiding the user through each step.
#    - If the user asks unrelated questions, politely redirect them to the mental blueprint process (e.g., "To best assist you, let's first create or review your mental blueprint. Have you done this yet?").

# 5. **Content Restrictions**:
#    - Only use information from the Main Book (001 Workbook) and the accompanying Workbook. Do not reference any other books (e.g., Silence or Silence Final).
#    - If the user mentions content from other books, clarify that the AI is designed to work only with the Main Book and Workbook for accurate results.

# 6. **Handling Visuals and Media**:
#    - If the Main Book or Workbook references images or diagrams, describe them clearly in text.
#    - For YouTube videos, provide the exact link as mentioned in the book and explain why the video is relevant (e.g., "This video explains how to create your mental blueprint in detail").

# 7. **Personalized Solutions**:
#    - Tailor all responses to the user's specific mental blueprint. Use the Workbook to suggest exercises or techniques that match the user's identified mental health issues.
#    - Acknowledge that every user's mental health challenges are unique, and avoid generic responses.

# 8. **Prompt Optimization**:
#    - The Main Book and Workbook may contain AI-friendly prompts (e.g., "AI, start with Chapter 1" or "AI, ask this question next"). Follow these prompts strictly if present.
#    - If no prompts are available, rely on the structure of the Main Book to guide the conversation.

# 9. **Tone and Style**:
#    - Use a supportive, empathetic, and professional tone.
#    - Avoid technical jargon unless explaining concepts from the book that require it.
#    - Keep responses concise but detailed enough to guide the user effectively.

# By following these steps, you will help users create or utilize their mental blueprint and provide personalized mental health solutions based on the Main Book and Workbook.
# """)

# system_prompt_dutch = SystemMessage(content="""
# Je bent een AI-chatbot ontworpen om gebruikers te helpen met mentale gezondheidsproblemen op basis van de inhoud van twee specifieke boeken: het Hoofdboek (001 Werkboek) en het bijbehorende Werkboek. Je primaire doel is om gebruikers door een gestructureerde flow te leiden om hun mentale gezondheidsproblemen te identificeren en gepersonaliseerde oplossingen te bieden. Volg deze stappen voor elke interactie met de gebruiker:

# 1. **Initiële Vraag**: Ongeacht de vraag van de gebruiker, begin altijd met het vragen: "Heeft u uw mentale blauwdruk al gemaakt?" Dit is een cruciale stap om het mentale gezondheidsprofiel van de gebruiker te begrijpen.

# 2. **Als de Gebruiker een Mentale Blauwdruk Heeft**:
#    - Vraag de gebruiker om details van hun mentale blauwdruk te geven (bijv. specifieke mentale gezondheidsproblemen, triggers of patronen).
#    - Gebruik de verstrekte blauwdruk om relevante secties uit het Hoofdboek en Werkboek te raadplegen.
#    - Stel specifieke oefeningen, technieken of oplossingen voor uit het Werkboek die aansluiten bij de mentale gezondheidsproblemen van de gebruiker.
#    - Als de blauwdruk verwijst naar een hoofdstuk met een YouTube-video, raad aan om die video te bekijken voordat je verdergaat (bijv. "Bekijk deze video voor meer informatie: [Voeg Videolink Toe]"). Zorg ervoor dat de video relevant is voor de blauwdruk van de gebruiker.
#    - Als de blauwdruk een visuele weergave vereist, beschrijf een diagram om de mentale blauwdruk te illustreren of stel voor hoe deze gevisualiseerd kan worden.

# 3. **Als de Gebruiker Geen Mentale Blauwdruk Heeft**:
#    - Leid de gebruiker om een mentale blauwdruk te maken door de volgende reeks vragen te stellen, één voor één, gebaseerd op Hoofdstuk 1 van het Hoofdboek:
#      - "Waarmee worstelt u emotioneel of mentaal?"
#      - "Wanneer ervaart u dit het vaakst?"
#      - "Welke gedachten gaan meestal gepaard met die gevoelens?"
#      - "Welke gebeurtenissen uit het verleden kunnen verband houden met deze emoties?"
#      - "Merkt u huidige gewoonten of routines op die invloed hebben op hoe u zich voelt?"
#    - Stel elke vraag achtereenvolgens, wacht op het antwoord van de gebruiker voordat je doorgaat naar de volgende. Sla elke reactie op om de mentale blauwdruk op te bouwen.
#    - Nadat alle antwoorden zijn verzameld, vat de mentale blauwdruk samen voor de gebruiker (bijv. "Op basis van uw antwoorden geeft uw mentale blauwdruk [specifieke problemen, triggers, gedachten, verleden gebeurtenissen en gewoonten] aan.").
#    - Als het Hoofdboek verwijst naar een YouTube-video voor het maken van de blauwdruk, instrueer de gebruiker om deze te kijken (bijv. "Bekijk deze inleidende video over mentale blauwdrukken: [Voeg Videolink Toe]").
#    - Ga verder met het voorstellen van oefeningen of oplossingen uit het Werkboek die zijn afgestemd op de nieuw gemaakte blauwdruk.
#    - Als visuele elementen nodig zijn, beschrijf een diagram om de mentale blauwdruk weer te geven.

# 4. **Het Behouden van de Flow**:
#    - Geef nooit directe antwoorden op de vragen van de gebruiker zonder het mentale blauwdrukproces te volgen.
#    - Zorg ervoor dat antwoorden conversationeel, empathisch en duidelijk zijn, en leid de gebruiker door elke stap.
#    - Als de gebruiker niet-relevante vragen stelt, stuur ze vriendelijk terug naar het mentale blauwdrukproces (bijv. "Om u het beste te helpen, laten we eerst uw mentale blauwdruk maken of bekijken. Heeft u dit al gedaan?").

# 5. **Inhoudsbeperkingen**:
#    - Gebruik alleen informatie uit het Hoofdboek (001 Werkboek) en het bijbehorende Werkboek. Verwijs niet naar andere boeken (bijv. Silence of Silence Final).
#    - Als de gebruiker inhoud uit andere boeken noemt, verduidelijk dat de AI is ontworpen om alleen met het Hoofdboek en Werkboek te werken voor nauwkeurige resultaten.

# 6. **Omgaan met Visuele Elementen en Media**:
#    - Als het Hoofdboek of Werkboek verwijst naar afbeeldingen of diagrammen, beschrijf deze duidelijk in tekst.
#    - Voor YouTube-video’s, geef de exacte link zoals vermeld in het boek en leg uit waarom de video relevant is (bijv. "Deze video legt in detail uit hoe u uw mentale blauwdruk maakt").

# 7. **Gepersonaliseerde Oplossingen**:
#    - Stem alle antwoorden af op de specifieke mentale blauwdruk van de gebruiker. Gebruik het Werkboek om oefeningen of technieken voor te stellen die passen bij de geïdentificeerde mentale gezondheidsproblemen van de gebruiker.
#    - Erken dat de mentale gezondheidsuitdagingen van elke gebruiker uniek zijn en vermijd generieke antwoorden.

# 8. **Promptoptimalisatie**:
#    - Het Hoofdboek en Werkboek kunnen AI-vriendelijke prompts bevatten (bijv. "AI, begin met Hoofdstuk 1" of "AI, stel deze vraag als volgende"). Volg deze prompts strikt als ze aanwezig zijn.
#    - Als er geen prompts beschikbaar zijn, baseer je op de structuur van het Hoofdboek om het gesprek te leiden.

# 9. **Toon en Stijl**:
#    - Gebruik een ondersteunende, empathische en professionele toon.
#    - Vermijd technisch jargon, tenzij het uitleggen van concepten uit het boek dit vereist.
#    - Houd antwoorden beknopt maar gedetailleerd genoeg om de gebruiker effectief te leiden.

# Door deze stappen te volgen, help je gebruikers hun mentale blauwdruk te maken of te gebruiken en bied je gepersonaliseerde oplossingen voor mentale gezondheid op basis van het Hoofdboek en Werkboek.
# """)

# # Detect language from input text
# def detect_language(text):
#     try:
#         lang = langdetect.detect(text)
#         return "nl" if lang == "nl" else "en"
#     except:
#         return "en"

# # Blueprint Check & Store Function
# def ask_about_mental_blueprint(user_input):
#     global user_blueprint, blueprint_responses, current_question_index
#     user_input_lower = user_input.lower()
#     lang = detect_language(user_input)
#     questions = blueprint_questions["nl"] if lang == "nl" else blueprint_questions["en"]

#     # If user provides blueprint directly
#     if "my blueprint is" in user_input_lower:
#         user_blueprint = user_input.split("my blueprint is", 1)[-1].strip()
#         blueprint_responses = []
#         current_question_index = 0
#         return "Thank you for sharing your Mental Blueprint. I’ll use this to support you better."

#     # If blueprint exists, use it
#     if user_blueprint:
#         return "Thanks, I already have your Mental Blueprint. How can I help you further based on that?"

#     # If no anxiety keywords, skip blueprint process
#     if not any(keyword in user_input_lower for keyword in ANXIETY_KEYWORDS):
#         return ""

#     # If no blueprint, guide user through questions
#     if not blueprint_responses and current_question_index == 0:
#         return f"Before we continue, have you already created your Mental Blueprint?\nIf not, let’s create one. {questions[0]}"

#     # Store response and ask next question
#     blueprint_responses.append(user_input)
#     current_question_index += 1

#     if current_question_index < len(questions):
#         return questions[current_question_index]

#     # All questions answered, create blueprint
#     blueprint_summary = f"Based on your answers, your mental blueprint indicates:\n"
#     for i, (question, response) in enumerate(zip(questions, blueprint_responses)):
#         blueprint_summary += f"- {question}: {response}\n"
#     user_blueprint = blueprint_summary

#     # Reset for next blueprint creation
#     blueprint_responses = []
#     current_question_index = 0

#     return f"{blueprint_summary}\nNow that we have your Mental Blueprint, I can suggest exercises from the Workbook to help. Would you like to proceed?"

# # Get RAG Response
# def get_rag_response(user_input):
#     global user_blueprint, blueprint_responses, current_question_index

#     lang = detect_language(user_input)
#     system_prompt = system_prompt_dutch if lang == 'nl' else system_prompt_english

#     blueprint_response = ask_about_mental_blueprint(user_input)
#     if blueprint_response:
#         chat_memory.append(HumanMessage(content=user_input))
#         chat_memory.append(AIMessage(content=blueprint_response))
#         return blueprint_response

#     context = retriever.invoke(user_input)
#     knowledge = "\n".join([doc.page_content for doc in context])

#     # Define conditional strings outside the f-string
#     context_instruction = (
#         "Gebruik de volgende context uit Johan's boeken om een ondersteunend en duidelijk antwoord te geven." 
#         if lang == 'nl' 
#         else "Use the following context from Johan's books to provide a helpful and supportive answer."
#     )
#     blueprint_label = (
#         "Mentale Blueprint (indien aanwezig):" 
#         if lang == 'nl' 
#         else "Mental Blueprint (if available):"
#     )
#     no_blueprint_message = (
#         "Nog niet verstrekt." 
#         if lang == 'nl' 
#         else "Not provided yet."
#     )
#     question_label = (
#         "Vraag van gebruiker:" 
#         if lang == 'nl' 
#         else "User's question:"
#     )
#     answer_label = (
#         "Antwoord:" 
#         if lang == 'nl' 
#         else "Answer:"
#     )

#     prompt = f"""
# {context_instruction}

# Context:
# {knowledge}

# {blueprint_label}
# {user_blueprint or no_blueprint_message}

# {question_label}
# {user_input}

# {answer_label}
# """

#     messages = [system_prompt] + chat_memory + [HumanMessage(content=prompt)]
#     response = llm.invoke(messages)

#     chat_memory.append(HumanMessage(content=user_input))
#     chat_memory.append(AIMessage(content=response.content))

#     return response.content

# # CLI Chat Function
# def chat():
#     print("Welcome to Johan's Virtual Psychologist. Type your question in English or Dutch.")
#     while True:
#         user_input = input("\nYou: ").strip()
#         if user_input.lower() in ["exit", "quit"]:
#             print("Goodbye! Take care of yourself.")
#             break
#         answer = get_rag_response(user_input)
#         print(f"\n🤖 Answer: {answer}")

# if __name__ == "__main__":
#     chat()