# # import fitz  # PyMuPDF
# # import os
# # import glob

# # def extract_images_from_pdf(pdf_file):
# #     doc = fitz.open(pdf_file)
# #     image_list = []
    
# #     # Loop through all pages in the PDF
# #     for page_num in range(len(doc)):
# #         page = doc.load_page(page_num)
# #         # Get images on the page
# #         image_list += page.get_images(full=True)
    
# #     # List to store the paths of extracted images
# #     image_paths = []
# #     for img_index, img in enumerate(image_list):
# #         xref = img[0]
# #         base_image = doc.extract_image(xref)
# #         image_bytes = base_image["image"]  # Extract image bytes
# #         image_path = f"image_{os.path.basename(pdf_file)}_{img_index}.png"  # Save the image as a PNG
# #         with open(image_path, "wb") as img_file:
# #             img_file.write(image_bytes)
# #         image_paths.append(image_path)
    
# #     return image_paths

# # # Define the folder path where PDFs are stored
# # pdf_folder = "data"

# # # Get a list of all PDF files in the folder
# # pdf_files = glob.glob(os.path.join(pdf_folder, "*.pdf"))

# # # Extract images from each PDF file
# # for pdf_file in pdf_files:
# #     print(f"Extracting images from: {pdf_file}")
# #     image_paths = extract_images_from_pdf(pdf_file)
# #     for path in image_paths:
# #         print(f"Image saved at: {path}")









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

# # # Function to extract images from PDFs
# # def extract_images_from_pdf(pdf_file):
# #     doc = fitz.open(pdf_file)
# #     image_list = []
    
# #     # Loop through all pages in the PDF
# #     for page_num in range(len(doc)):
# #         page = doc.load_page(page_num)
# #         # Get images on the page
# #         image_list += page.get_images(full=True)
    
# #     # List to store the paths of extracted images
# #     image_paths = []
# #     for img_index, img in enumerate(image_list):
# #         xref = img[0]
# #         base_image = doc.extract_image(xref)
# #         image_bytes = base_image["image"]  # Extract image bytes
# #         image_path = f"image_{os.path.basename(pdf_file)}_{img_index}.png"  # Save the image as a PNG
# #         with open(image_path, "wb") as img_file:
# #             img_file.write(image_bytes)
# #         image_paths.append(image_path)
    
# #     return image_paths

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
# # system_prompt_dutch = SystemMessage(content="""You are a compassionate, friendly, and insightful virtual psychologist specializing in helping people deal with anxiety and panic. Your advice is based on Johan’s personal books and courses on mental health. You must respond in a supportive, empathetic, and easy-to-understand way in plain Dutch. Keep a calm, positive, and solution-focused tone. If you don’t have enough information, say so politely and suggest speaking to a professional.""")
# # system_prompt_english = SystemMessage(content="""You are a compassionate, friendly, and insightful virtual psychologist specializing in helping people deal with anxiety and panic. Your advice is based on Johan’s personal books and courses on mental health. You must respond in a supportive, empathetic, and easy-to-understand way in English. Keep a calm, positive, and solution-focused tone. If you don’t have enough information, say so politely and suggest speaking to a professional.""")

# # # Detect language from input text
# # def detect_language(text):
# #     try:
# #         lang = langdetect.detect(text)
# #         return "nl" if lang == "nl" else "en"
# #     except:
# #         return "en"

# # # Memory for current session
# # chat_memory = []

# # # Function to fetch response from RAG model
# # def get_rag_response(user_input):
# #     context = retriever.invoke(user_input)
# #     info = "\n".join([doc.page_content for doc in context])
# #     lang = detect_language(user_input)

# #     if lang == "nl":
# #         system_prompt = system_prompt_dutch
# #         prompt = f'''Gebruik de volgende context uit Johan's boeken om een ondersteunend en duidelijk antwoord te geven in eenvoudig Nederlands.

# # Kennisbank:
# # {info}

# # Vraag van gebruiker:
# # {user_input}

# # Antwoord:
# # '''
# #     else:
# #         system_prompt = system_prompt_english
# #         prompt = f'''Use the following context from Johan's books to provide a supportive and clear answer in simple English.

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

# # # Show images related to the PDFs
# # def show_images(pdf_folder):
# #     pdf_files = glob.glob(os.path.join(pdf_folder, "*.pdf"))
# #     for pdf_file in pdf_files:
# #         image_paths = extract_images_from_pdf(pdf_file)
# #         for path in image_paths:
# #             display(Image(filename=path))  # Display image in Colab or Jupyter

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
        
# #         # Check for images related to the PDFs
# #         if "image" in user_input.lower():
# #             show_images(pdf_folder)

# # if __name__ == "__main__":
# #     chat()






# import os
# import fitz  # PyMuPDF
# import glob
# import langdetect
# from dotenv import load_dotenv
# from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings, ChatOpenAI
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain.schema import HumanMessage, SystemMessage, AIMessage
# from langchain_core.documents import Document

# # Load environment variables
# load_dotenv()
# os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

# # Global memory and blueprint
# chat_memory = []
# user_blueprint = None
# blueprint_responses = []
# current_question_index = 0

# # Keywords
# ANXIETY_KEYWORDS = [
#     "anxiety", "anxious", "stress", "nervous", "panic", "worried", "fearful",
#     "mental blueprint", "blueprint", "mental discomfort", "overwhelmed", "can't relax", "overthinking"
# ]

# # System prompts
# system_prompt_english = SystemMessage(content="""
# You are an AI chatbot designed to assist users with mental health issues based on the content of two specific books: the Main Book (001 Workbook) and the accompanying Workbook. Your primary goal is to guide users through a structured, empathetic, and conversational flow to identify their mental health issues and provide personalized solutions. Follow these steps for every user interaction:

# 1. **Casual Interaction**: If the user greets you casually (e.g., "hi", "hello", "hey"), respond warmly and conversationally, inviting them to share how you can assist without immediately mentioning a mental blueprint. Keep the response short and human-like.

# 2. **General Help Request**: If the user asks for help vaguely (e.g., "I need help"), respond empathetically and ask for more details about their situation to understand their needs better. Avoid suggesting exercises immediately.

# 3. **Intent Detection**: Analyze the user's input to determine their intent:
#    - If the user requests solutions (e.g., "what can I do?", "how to fix"), check if they have a mental blueprint. If they do, provide solutions based on their blueprint. If not, ask if they’d like to create one or provide solutions based on their stated issue.
#    - If the user mentions a mental health issue (e.g., "I have panic attacks") without requesting solutions, express empathy and ask if they have created a mental blueprint. Follow the blueprint flow if they agree, or provide solutions if they decline.
#    - If the user wants to create a mental blueprint, follow the blueprint creation steps below.
#    - If the user’s intent is unclear or unrelated, guide them empathetically toward sharing their mental health concerns.

# 4. **Mental Blueprint Creation**: If the user agrees to create a mental blueprint, guide them through these questions one at a time:
#    - Step 1: "What are you struggling with emotionally or mentally?"
#    - Step 2: "When do you most often experience this?"
#    - Step 3: "What thoughts usually accompany those feelings?"
#    - Step 4: "What past events might be related to these emotions?"
#    - Step 5: "Do you notice any current habits or routines that affect how you feel?"
#    Store each response. After collecting all responses, summarize the blueprint and provide tailored Workbook exercises with specific Worksheet and Assignment numbers (e.g., "Assignment 3.2 from Worksheet 10").

# 5. **If User Has a Mental Blueprint or Requests Solutions**: Use their blueprint or stated issues to fetch relevant exercises from the Main Book and Workbook. Include specific Worksheet and Assignment numbers.

# 6. **Maintaining the Flow**: Keep responses conversational, empathetic, and concise. If the user asks unrelated questions, gently redirect to their mental health concerns. Do not ask all blueprint questions at once.

# 7. **Content Restrictions**: Use only the Main Book (001 Workbook) and Workbook. Clarify this if other books are mentioned.

# 8. **Personalized Solutions**: Tailor responses to the user’s issues or blueprint with specific Workbook exercises. Acknowledge their unique challenges.

# 9. **Tone and Style**: Use a supportive, empathetic, and professional tone. Keep responses human-like and avoid overly technical jargon.
# """)
# system_prompt_dutch = SystemMessage(content="""
# Je bent een AI-chatbot ontworpen om gebruikers te helpen met mentale gezondheidsproblemen op basis van de inhoud van twee specifieke boeken: het Hoofdboek (001 Werkboek) en het bijbehorende Werkboek. Je primaire doel is om gebruikers door een gestructureerde, empathische en conversationele flow te leiden om hun mentale gezondheidsproblemen te identificeren en gepersonaliseerde oplossingen te bieden. Volg deze stappen voor elke interactie:

# 1. **Casuele Interactie**: Als de gebruiker je informeel begroet (bijv. "hallo", "hey"), reageer warm en conversationeel, en nodig hen uit om te delen hoe je kunt helpen zonder meteen naar een mentale blauwdruk te vragen. Houd de reactie kort en menselijk.

# 2. **Algemene Hulpvraag**: Als de gebruiker vaag om hulp vraagt (bijv. "Ik heb hulp nodig"), reageer empathisch en vraag om meer details over hun situatie om hun behoeften beter te begrijpen. Vermijd het direct voorstellen van oefeningen.

# 3. **Intentie Detectie**: Analyseer de input van de gebruiker om hun intentie te bepalen:
#    - Als de gebruiker om oplossingen vraagt (bijv. "Wat kan ik doen?", "Hoe los ik dit op?"), controleer of ze een mentale blauwdruk hebben. Als ze die hebben, bied oplossingen gebaseerd op hun blauwdruk. Zo niet, vraag of ze er een willen maken of bied oplossingen gebaseerd op hun genoemde probleem.
#    - Als de gebruiker een mentaal gezondheidsprobleem noemt (bijv. "Ik heb paniekaanvallen") zonder om oplossingen te vragen, toon empathie en vraag of ze een mentale blauwdruk hebben gemaakt. Volg de blauwdrukstroom als ze instemmen, of bied oplossingen als ze weigeren.
#    - Als de gebruiker een mentale blauwdruk wil maken, volg de onderstaande stappen voor het maken van de blauwdruk.
#    - Als de intentie onduidelijk of niet gerelateerd is, leid hen empathisch naar het delen van hun mentale gezondheidsproblemen.

# 4. **Mentale Blauwdruk Creatie**: Als de gebruiker instemt met het maken van een mentale blauwdruk, leid hen door de volgende vragen één voor één:
#    - Stap 1: "Waarmee worstelt u emotioneel of mentaal?"
#    - Stap 2: "Wanneer ervaart u dit het vaakst?"
#    - Stap 3: "Welke gedachten gaan meestal gepaard met die gevoelens?"
#    - Stap 4: "Welke gebeurtenissen uit het verleden kunnen verband houden met deze emoties?"
#    - Stap 5: "Merkt u huidige gewoonten of routines op die invloed hebben op hoe u zich voelt?"
#    Sla elke reactie op. Vat na alle antwoorden de blauwdruk samen en beveel Werkboek-oefeningen aan met specifieke Worksheet- en Assignment-nummers (bijv. "Assignment 3.2 van Worksheet 10").

# 5. **Als de Gebruiker een Mentale Blauwdruk Heeft of Oplossingen Vraagt**: Gebruik hun blauwdruk of genoemde problemen om relevante oefeningen uit het Hoofdboek en Werkboek te halen. Voeg specifieke Worksheet- en Assignment-nummers toe.

# 6. **Het Behouden van de Flow**: Houd antwoorden conversationeel, empathisch en beknopt. Als de gebruiker niet-relevante vragen stelt, stuur vriendelijk terug naar hun mentale gezondheidsproblemen.

# 7. **Inhoudsbeperkingen**: Gebruik alleen het Hoofdboek (001 Werkboek) en Werkboek. Verduidelijk dit als andere boeken worden genoemd.

# 8. **Gepersonaliseerde Oplossingen**: Stem antwoorden af op de blauwdruk of genoemde problemen met specifieke Werkboek-oefeningen. Erken de uniciteit van de uitdagingen van de gebruiker.

# 9. **Toon en Stijl**: Gebruik een ondersteunende, empathische en professionele toon. Houd reacties menselijk en vermijd overdreven technisch jargon.
# """)

# # Language detection
# def detect_language(text):
#     try:
#         lang = langdetect.detect(text)
#         return "nl" if lang == "nl" else "en"
#     except:
#         return "en"

# # PDF reader
# def extract_text_from_all_pdfs(folder_path):
#     combined_texts = []
#     pdf_files = glob.glob(os.path.join(folder_path, "*.pdf"))
#     for pdf_file in pdf_files:
#         try:
#             with fitz.open(pdf_file) as doc:
#                 text = "".join(page.get_text() + "\n" for page in doc)
#                 combined_texts.append(Document(page_content=text.strip()))
#                 print(f"✅ Loaded: {os.path.basename(pdf_file)}")
#         except Exception as e:
#             print(f"❌ Failed to process {pdf_file}: {e}")
#     return combined_texts

# # PDF -> FAISS
# pdf_folder = "data"
# documents = extract_text_from_all_pdfs(pdf_folder)
# splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=200)
# split_docs = splitter.split_documents(documents)

# faiss_path = "faiss_db_johan"
# if os.path.exists(faiss_path):
#     vectordb = FAISS.load_local(faiss_path, OpenAIEmbeddings(), allow_dangerous_deserialization=True)
# else:
#     vectordb = FAISS.from_documents(split_docs, OpenAIEmbeddings())
#     vectordb.save_local(faiss_path)

# retriever = vectordb.as_retriever(search_kwargs={"k": 3})
# llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.6)

# # Blueprint conversation
# def ask_about_mental_blueprint(user_input):
#     global user_blueprint, blueprint_responses, current_question_index
#     user_input_lower = user_input.lower()
#     lang = detect_language(user_input)

#     # Define blueprint questions
#     questions = [
#         "What are you struggling with emotionally or mentally?",
#         "When do you most often experience this?",
#         "What thoughts usually accompany those feelings?",
#         "What past events might be related to these emotions?",
#         "Do you notice any current habits or routines that affect how you feel?"
#     ] if lang == "en" else [
#         "Waarmee worstelt u emotioneel of mentaal?",
#         "Wanneer ervaart u dit het vaakst?",
#         "Welke gedachten gaan meestal gepaard met die gevoelens?",
#         "Welke gebeurtenissen uit het verleden kunnen verband houden met deze emoties?",
#         "Merkt u huidige gewoonten of routines op die invloed hebben op hoe u zich voelt?"
#     ]

#     # Handle blueprint creation process if already in progress
#     if current_question_index > 0:
#         blueprint_responses.append(user_input)
#         current_question_index += 1

#         if current_question_index < len(questions):
#             return questions[current_question_index]

#         # Summarize blueprint and suggest solutions
#         summary = "Based on your answers, your mental blueprint indicates:\n" if lang == "en" else "Op basis van uw antwoorden geeft uw mentale blauwdruk aan:\n"
#         for q, r in zip(questions, blueprint_responses):
#             summary += f"- {q}: {r}\n"
#         user_blueprint = summary
#         context = retriever.invoke(user_blueprint)
#         knowledge = "\n".join([doc.page_content for doc in context])
#         prompt = f"""
# Based on the user's mental blueprint and the content from the Main Book and Workbook, suggest specific exercises or techniques to address their mental health issues.

# User's blueprint: {user_blueprint}
# Context from books: {knowledge}

# Provide an empathetic response with tailored suggestions, focusing on actionable exercises or techniques from the Workbook. For each suggestion, include specific Worksheet and Assignment numbers (e.g., "Assignment 3.2 from Worksheet 10"). Ensure suggestions are personalized to the user's blueprint.
# """
#         response = llm.invoke([system_prompt_english if lang == "en" else system_prompt_dutch, HumanMessage(content=prompt)])
#         blueprint_responses.clear()
#         current_question_index = 0
#         return f"Your mental blueprint has been created!\n{summary}\n{response.content}"

#     # Detect user intent using AI
#     intent_prompt = f"""
# Analyze the user's input to determine their intent: '{user_input}'.
# - If the user is greeting you casually (e.g., "hi", "hello", "hey", "yo", "hiya", "good morning", "good day"), respond with 'GREETING'.
# - If the user is requesting general help (e.g., "I need help", "help me"), respond with 'GENERAL_HELP'.
# - If the user is requesting solutions (e.g., "what can I do?", "suggest something", "how to fix"), respond with 'SOLUTION'.
# - If the user is mentioning a mental health issue without explicitly requesting solutions (e.g., "I feel anxious", "I have panic attacks"), respond with 'ISSUE'.
# - If the user expresses a desire to create a mental blueprint (e.g., "guide me", "I want to create a blueprint", "let's make one"), respond with 'BLUEPRINT'.
# - If the user’s intent is unclear or unrelated, respond with 'UNRELATED'.
# """
#     intent_response = llm.invoke([system_prompt_english if lang == "en" else system_prompt_dutch, HumanMessage(content=intent_prompt)])
#     intent = intent_response.content.strip()

#     # Handle casual greetings
#     if intent == "GREETING":
#         prompt = f"Respond warmly and conversationally to the user's greeting: '{user_input}'. Invite them to share how you can assist without mentioning a mental blueprint. Keep it short and human-like."
#         response = llm.invoke([system_prompt_english if lang == "en" else system_prompt_dutch, HumanMessage(content=prompt)])
#         return response.content

#     # Handle general help requests
#     if intent == "GENERAL_HELP":
#         prompt = f"The user said: '{user_input}'. Respond empathetically and ask for more details about what they’re going through to better understand their needs. Keep the response short and human-like, avoiding immediate suggestions of exercises or blueprints."
#         response = llm.invoke([system_prompt_english if lang == "en" else system_prompt_dutch, HumanMessage(content=prompt)])
#         return response.content

#     # Handle blueprint creation initiation
#     if intent == "BLUEPRINT":
#         blueprint_responses = []
#         current_question_index = 0
#         blueprint_responses.append(user_input)
#         current_question_index += 1
#         return questions[0]

#     # Handle mental health issues (prioritize ISSUE even if SOLUTION is present)
#     if intent == "ISSUE" and current_question_index == 0:
#         prompt = f"""
# The user mentioned a mental health issue: '{user_input}'. Respond empathetically, acknowledging their struggle. Then ask if they have created a mental blueprint to understand their feelings better. Keep the response concise and human-like.
# """
#         response = llm.invoke([system_prompt_english if lang == "en" else system_prompt_dutch, HumanMessage(content=prompt)])
#         return response.content

#     # Handle solution requests when no issue is mentioned or blueprint exists
#     if intent == "SOLUTION" and intent != "ISSUE" and current_question_index == 0:
#         if user_blueprint:
#             context_input = user_blueprint
#             context = retriever.invoke(context_input)
#             knowledge = "\n".join([doc.page_content for doc in context])
#             prompt = f"""
# Based on the user's input and the content from the Main Book and Workbook, suggest specific exercises or techniques to address their mental health issues.

# User's blueprint: {context_input}
# Context from books: {knowledge}

# Provide an empathetic response with tailored suggestions, focusing on actionable exercises or techniques from the Workbook. For each suggestion, include specific Worksheet and Assignment numbers (e.g., "Assignment 3.2 from Worksheet 10"). Ensure suggestions are personalized to the user's blueprint.
# """
#             response = llm.invoke([system_prompt_english if lang == "en" else system_prompt_dutch, HumanMessage(content=prompt)])
#             return response.content
#         else:
#             prompt = f"""
# The user requested solutions without a mental blueprint: '{user_input}'. Respond empathetically, suggesting that creating a blueprint could help. Ask if they’d like to start creating one now. If they’ve mentioned a specific issue, offer to provide solutions based on that issue if they prefer not to create a blueprint. Keep the response concise and human-like.
# """
#             response = llm.invoke([system_prompt_english if lang == "en" else system_prompt_dutch, HumanMessage(content=prompt)])
#             return response.content

#     # User provides or confirms having a blueprint
#     if "my blueprint is" in user_input_lower or user_input_lower in ["i have mental blue print", "i have a mental blueprint"]:
#         if "my blueprint is" in user_input_lower:
#             user_blueprint = user_input.split("my blueprint is", 1)[-1].strip()
#         else:
#             user_blueprint = user_input
#         blueprint_responses = []
#         current_question_index = 0
#         context = retriever.invoke(user_blueprint)
#         knowledge = "\n".join([doc.page_content for doc in context])
#         prompt = f"""
# Based on the user's mental blueprint and the content from the Main Book and Workbook, suggest specific exercises or techniques to address their mental health issues.

# User's blueprint: {user_blueprint}
# Context from books: {knowledge}

# Provide an empathetic response with tailored suggestions, focusing on actionable exercises or techniques from the Workbook. For each suggestion, include specific Worksheet and Assignment numbers (e.g., "Assignment 3.2 from Worksheet 10"). Ensure suggestions are personalized to the user's blueprint.
# """
#         response = llm.invoke([system_prompt_english if lang == "en" else system_prompt_dutch, HumanMessage(content=prompt)])
#         return response.content

#     # User explicitly says they don't have a blueprint
#     if "i don't have a mental blueprint" in user_input_lower or "no blueprint" in user_input_lower:
#         prompt = f"""
# The user said they don't have a mental blueprint: '{user_input}'. Respond empathetically, suggesting that creating a blueprint could help. Ask if they’d like to start creating one now. If they’ve mentioned a specific issue (e.g., "panic attacks"), offer to provide solutions based on that issue if they prefer not to create a blueprint. Keep the response concise and human-like.
# """
#         response = llm.invoke([system_prompt_english if lang == "en" else system_prompt_dutch, HumanMessage(content=prompt)])
#         return response.content

#     # Handle blueprint creation agreement
#     if any(word in user_input_lower for word in ["yes", "sure", "okay", "start", "let's do it"]) and current_question_index == 0:
#         blueprint_responses = []
#         current_question_index = 0
#         blueprint_responses.append(user_input)
#         current_question_index += 1
#         return questions[0]

#     # Handle blueprint creation declination
#     if any(word in user_input_lower for word in ["no", "not now", "don't want"]) and current_question_index == 0:
#         context = retriever.invoke(user_input)
#         knowledge = "\n".join([doc.page_content for doc in context])
#         prompt = f"""
# The user declined to create a mental blueprint and mentioned: '{user_input}'. Provide an empathetic response with tailored suggestions based on their stated issue, focusing on actionable exercises or techniques from the Workbook. For each suggestion, include specific Worksheet and Assignment numbers (e.g., "Assignment 3.2 from Worksheet 10"). Ensure suggestions are personalized to the user's input.
# """
#         response = llm.invoke([system_prompt_english if lang == "en" else system_prompt_dutch, HumanMessage(content=prompt)])
#         return response.content

#     # Default response for unrelated input
#     prompt = f"The user said: '{user_input}'. Respond empathetically and guide them toward sharing their mental health concerns or starting a mental blueprint. Keep the response concise and human-like."
#     response = llm.invoke([system_prompt_english if lang == "en" else system_prompt_dutch, HumanMessage(content=prompt)])
#     return response.content

# # Main response function
# def get_rag_response(user_input):                                                                                                                                                                                            
#     lang = detect_language(user_input)
#     system_prompt = system_prompt_dutch if lang == 'nl' else system_prompt_english

#     blueprint_response = ask_about_mental_blueprint(user_input)
#     if blueprint_response:
#         chat_memory.append(HumanMessage(content=user_input))
#         chat_memory.append(AIMessage(content=blueprint_response))
#         return blueprint_response

#     # Fallback for general queries
#     context = retriever.invoke(user_input)
#     knowledge = "\n".join([doc.page_content for doc in context])
#     blueprint_info = user_blueprint if user_blueprint else "Not provided yet."
#     prompt = f"""
# Use the following context from Johan's books to provide a helpful and supportive answer.

# Context:
# {knowledge}

# Mental Blueprint (if available):
# {blueprint_info}

# User's question:
# {user_input}

# Provide an empathetic response, and if relevant, guide the user toward creating a mental blueprint. For each suggestion, include specific Worksheet and Assignment numbers (e.g., "Assignment 3.2 from Worksheet 10").
# """
#     messages = [system_prompt] + chat_memory + [HumanMessage(content=prompt)]
#     response = llm.invoke(messages)

#     chat_memory.append(HumanMessage(content=user_input))
#     chat_memory.append(AIMessage(content=response.content))
#     return response.content

# # Entry point
# def chat():
#     print("🧠 Welcome to Johan's Virtual Psychologist. Type your question in English or Dutch.")
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
# import glob
# import langdetect
# from dotenv import load_dotenv
# from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings, ChatOpenAI
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain.schema import HumanMessage, SystemMessage, AIMessage
# from langchain_core.documents import Document

# # Load environment variables
# load_dotenv()
# os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

# # Global memory and blueprint
# chat_memory = []
# user_blueprint = None
# blueprint_responses = []
# current_question_index = 0

# # Keywords
# ANXIETY_KEYWORDS = [
#     "anxiety", "anxious", "stress", "nervous", "panic", "worried", "fearful",
#     "mental blueprint", "blueprint", "mental discomfort", "overwhelmed", "can't relax", "overthinking", "presure", "pressure"
# ]

# # System prompts
# system_prompt_english = SystemMessage(content="""
# You are an AI chatbot designed to assist users with mental health issues based on the content of two specific books: the Main Book (001 Workbook) and the accompanying Workbook. Your primary goal is to guide users through a structured, empathetic, and conversational flow to identify their mental health issues and provide personalized solutions. Follow these steps for every user interaction:

# 1. **Casual Interaction**: If the user greets you casually (e.g., "hi", "hello", "hey"), respond warmly and conversationally, inviting them to share how you can assist without immediately mentioning a mental blueprint. Keep the response short and human-like.

# 2. **General Help Request**: If the user asks for help vaguely (e.g., "I need help"), respond empathetically and ask for more details about their situation to understand their needs better. Avoid suggesting exercises immediately.

# 3. **Intent Detection**: Analyze the user's input to determine their intent:
#    - If the user requests solutions (e.g., "what can I do?", "how to fix"), check if they have a mental blueprint. If they do, provide solutions based on their blueprint. If not, ask if they’d like to create one or provide solutions based on their stated issue.
#    - If the user mentions a mental health issue (e.g., "I have panic attacks") without requesting solutions, express empathy and ask if they have created a mental blueprint. Follow the blueprint flow if they agree, or provide solutions if they decline.
#    - If the user wants to create a mental blueprint, follow the blueprint creation steps below.
#    - If the user confirms they have a blueprint, ask if they want to create a new one or proceed with solutions.
#    - If the user’s intent is unclear or unrelated, guide them empathetically toward sharing their mental health concerns.

# 4. **Mental Blueprint Creation**: If the user agrees to create a mental blueprint, guide them through these questions one at a time:
#    - Step 1: "What are you struggling with emotionally or mentally?"
#    - Step 2: "When do you most often experience this?"
#    - Step 3: "What thoughts usually accompany those feelings?"
#    - Step 4: "What past events might be related to these emotions?"
#    - Step 5: "Do you notice any current habits or routines that affect how you feel?"
#    Store each response. After collecting all responses, summarize the blueprint and provide tailored Workbook exercises with specific Worksheet and Assignment numbers (e.g., "Assignment 3.2 from Worksheet 10").

# 5. **If User Has a Mental Blueprint or Requests Solutions**: Use their blueprint or stated issues to fetch relevant exercises from the Main Book and Workbook. Include specific Worksheet and Assignment numbers.

# 6. **Maintaining the Flow**: Keep responses conversational, empathetic, and concise. If the user asks unrelated questions, gently redirect to their mental health concerns. Do not ask all blueprint questions at once.

# 7. **Content Restrictions**: Use only the Main Book (001 Workbook) and Workbook. Clarify this if other books are mentioned.

# 8. **Personalized Solutions**: Tailor responses to the user’s issues or blueprint with specific Workbook exercises. Acknowledge their unique challenges.

# 9. **Tone and Style**: Use a supportive, empathetic, and professional tone. Keep responses human-like and avoid overly technical jargon.
# """)
# system_prompt_dutch = SystemMessage(content="""
# Je bent een AI-chatbot ontworpen om gebruikers te helpen met mentale gezondheidsproblemen op basis van de inhoud van twee specifieke boeken: het Hoofdboek (001 Werkboek) en het bijbehorende Werkboek. Je primaire doel is om gebruikers door een gestructureerde, empathische en conversationele flow te leiden om hun mentale gezondheidsproblemen te identificeren en gepersonaliseerde oplossingen te bieden. Volg deze stappen voor elke interactie:

# 1. **Casuele Interactie**: Als de gebruiker je informeel begroet (bijv. "hallo", "hey"), reageer warm en conversationeel, en nodig hen uit om te delen hoe je kunt helpen zonder meteen naar een mentale blauwdruk te vragen. Houd de reactie kort en menselijk.

# 2. **Algemene Hulpvraag**: Als de gebruiker vaag om hulp vraagt (bijv. "Ik heb hulp nodig"), reageer empathisch en vraag om meer details over hun situatie om hun behoeften beter te begrijpen. Vermijd het direct voorstellen van oefeningen.

# 3. **Intentie Detectie**: Analyseer de input van de gebruiker om hun intentie te bepalen:
#    - Als de gebruiker om oplossingen vraagt (bijv. "Wat kan ik doen?", "Hoe los ik dit op?"), controleer of ze een mentale blauwdruk hebben. Als ze die hebben, bied oplossingen gebaseerd op hun blauwdruk. Zo niet, vraag of ze er een willen maken of bied oplossingen gebaseerd op hun genoemde probleem.
#    - Als de gebruiker een mentaal gezondheidsprobleem noemt (bijv. "Ik heb paniekaanvallen") zonder om oplossingen te vragen, toon empathie en vraag of ze een mentale blauwdruk hebben gemaakt. Volg de blauwdrukstroom als ze instemmen, of bied oplossingen als ze weigeren.
#    - Als de gebruiker een mentale blauwdruk wil maken, volg de onderstaande stappen voor het maken van de blauwdruk.
#    - Als de gebruiker bevestigt dat ze een blauwdruk hebben, vraag of ze een nieuwe willen maken of oplossingen willen op basis van de bestaande blauwdruk.
#    - Als de intentie onduidelijk of niet gerelateerd is, leid hen empathisch naar het delen van hun mentale gezondheidsproblemen.

# 4. **Mentale Blauwdruk Creatie**: Als de gebruiker instemt met het maken van een mentale blauwdruk, leid hen door de volgende vragen één voor één:
#    - Stap 1: "Waarmee worstelt u emotioneel of mentaal?"
#    - Stap 2: "Wanneer ervaart u dit het vaakst?"
#    - Stap 3: "Welke gedachten gaan meestal gepaard met die gevoelens?"
#    - Stap 4: "Welke gebeurtenissen uit het verleden kunnen verband houden met deze emoties?"
#    - Stap 5: "Merkt u huidige gewoonten of routines op die invloed hebben op hoe u zich voelt?"
#    Sla elke reactie op. Vat na alle antwoorden de blauwdruk samen en beveel Werkboek-oefeningen aan met specifieke Worksheet- en Assignment-nummers (bijv. "Assignment 3.2 van Worksheet 10").

# 5. **Als de Gebruiker een Mentale Blauwdruk Heeft of Oplossingen Vraagt**: Gebruik hun blauwdruk of genoemde problemen om relevante oefeningen uit het Hoofdboek en Werkboek te halen. Voeg specifieke Worksheet- en Assignment-nummers toe.

# 6. **Het Behouden van de Flow**: Houd antwoorden conversationeel, empathisch en beknopt. Als de gebruiker niet-relevante vragen stelt, stuur vriendelijk terug naar hun mentale gezondheidsproblemen.

# 7. **Inhoudsbeperkingen**: Gebruik alleen het Hoofdboek (001 Werkboek) en Werkboek. Verduidelijk dit als andere boeken worden genoemd.

# 8. **Gepersonaliseerde Oplossingen**: Stem antwoorden af op de blauwdruk of genoemde problemen met specifieke Werkboek-oefeningen. Erken de uniciteit van de uitdagingen van de gebruiker.

# 9. **Toon en Stijl**: Gebruik een ondersteunende, empathische en professionele toon. Houd reacties menselijk en vermijd overdreven technisch jargon.
# """)

# # Language detection
# def detect_language(text):
#     try:
#         lang = langdetect.detect(text)
#         return "nl" if lang == "nl" else "en"
#     except:
#         return "en"

# # PDF reader
# def extract_text_from_all_pdfs(folder_path):
#     combined_texts = []
#     pdf_files = glob.glob(os.path.join(folder_path, "*.pdf"))
#     for pdf_file in pdf_files:
#         try:
#             with fitz.open(pdf_file) as doc:
#                 text = "".join(page.get_text() + "\n" for page in doc)
#                 combined_texts.append(Document(page_content=text.strip()))
#                 print(f"✅ Loaded: {os.path.basename(pdf_file)}")
#         except Exception as e:
#             print(f"❌ Failed to process {pdf_file}: {e}")
#     return combined_texts

# # PDF -> FAISS
# pdf_folder = "data"
# documents = extract_text_from_all_pdfs(pdf_folder)
# splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=200)
# split_docs = splitter.split_documents(documents)

# faiss_path = "faiss_db_johan"
# if os.path.exists(faiss_path):
#     vectordb = FAISS.load_local(faiss_path, OpenAIEmbeddings(), allow_dangerous_deserialization=True)
# else:
#     vectordb = FAISS.from_documents(split_docs, OpenAIEmbeddings())
#     vectordb.save_local(faiss_path)

# retriever = vectordb.as_retriever(search_kwargs={"k": 3})
# llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.6)

# # Blueprint conversation
# def ask_about_mental_blueprint(user_input):
#     global user_blueprint, blueprint_responses, current_question_index
#     user_input_lower = user_input.lower()
#     lang = detect_language(user_input)

#     # Define blueprint questions
#     questions = [
#         "What are you struggling with emotionally or mentally?",
#         "When do you most often experience this?",
#         "What thoughts usually accompany those feelings?",
#         "What past events might be related to these emotions?",
#         "Do you notice any current habits or routines that affect how you feel?"
#     ] if lang == "en" else [
#         "Waarmee worstelt u emotioneel of mentaal?",
#         "Wanneer ervaart u dit het vaakst?",
#         "Welke gedachten gaan meestal gepaard met die gevoelens?",
#         "Welke gebeurtenissen uit het verleden kunnen verband houden met deze emoties?",
#         "Merkt u huidige gewoonten of routines op die invloed hebben op hoe u zich voelt?"
#     ]

#     # Handle blueprint creation process if already in progress
#     if current_question_index > 0:
#         blueprint_responses.append(user_input)
#         current_question_index += 1

#         if current_question_index < len(questions):
#             return questions[current_question_index]

#         # Summarize blueprint and suggest solutions
#         summary = "Your mental blueprint has been created!\n" if lang == "en" else "Uw mentale blauwdruk is gemaakt!\n"
#         for q, r in zip(questions, blueprint_responses):
#             summary += f"- {q}: {r}\n"
#         user_blueprint = summary
#         context = retriever.invoke(user_blueprint)
#         knowledge = "\n".join([doc.page_content for doc in context])
#         prompt = f"""
# Based on the user's mental blueprint and the content from the Main Book and Workbook, suggest specific exercises or techniques to address their mental health issues.

# User's blueprint: {user_blueprint}
# Context from books: {knowledge}

# Provide an empathetic response with tailored suggestions, focusing on actionable exercises or techniques from the Workbook. For each suggestion, include specific Worksheet and Assignment numbers (e.g., "Assignment 3.2 from Worksheet 10"). Ensure suggestions are personalized to the user's blueprint.
# """
#         response = llm.invoke([system_prompt_english if lang == "en" else system_prompt_dutch, HumanMessage(content=prompt)])
#         blueprint_responses.clear()
#         current_question_index = 0
#         return f"{summary}\n{response.content}"

#     # Check conversation history for previous blueprint confirmation
#     has_blueprint = any("i have a mental blueprint" in msg.content.lower() or "my blueprint is" in msg.content.lower() for msg in chat_memory if isinstance(msg, HumanMessage))

#     # Detect user intent using AI
#     intent_prompt = f"""
# Analyze the user's input to determine their intent: '{user_input}'.
# - If the user is greeting you casually (e.g., "hi", "hello", "hey", "yo", "hiya", "good morning", "good day"), respond with 'GREETING'.
# - If the user is requesting general help (e.g., "I need help", "help me"), respond with 'GENERAL_HELP'.
# - If the user is requesting solutions (e.g., "what can I do?", "suggest something", "how to fix", "give me solutions", "what should i do?", "not now. give me the solution"), respond with 'SOLUTION'.
# - If the user is mentioning a mental health issue without explicitly requesting solutions (e.g., "I feel anxious", "I have panic attacks", "I have a mental presure"), respond with 'ISSUE'.
# - If the user expresses a desire to create a mental blueprint (e.g., "guide me", "I want to create a blueprint", "let's make one", "let's start"), respond with 'BLUEPRINT'.
# - If the user confirms they have a blueprint (e.g., "I have a mental blueprint", "my blueprint is"), respond with 'HAS_BLUEPRINT'.
# - If the user explicitly says they don’t have a blueprint (e.g., "I don’t have a mental blueprint", "no blueprint"), respond with 'NO_BLUEPRINT'.
# - If the user’s intent is unclear or unrelated, respond with 'UNRELATED'.
# Examples:
# - Input: "i have a mental presure in office time . so now tell me what should i do?" -> Intent: SOLUTION
# - Input: "I feel stressed at work" -> Intent: ISSUE
# - Input: "hii" -> Intent: GREETING
# - Input: "I want to create a blueprint" -> Intent: BLUEPRINT
# - Input: "i have mental blueprint" -> Intent: HAS_BLUEPRINT
# - Input: "not now. give me the solution" -> Intent: SOLUTION
# - Input: "i don't have any mental blueprint" -> Intent: NO_BLUEPRINT
# """
#     intent_response = llm.invoke([system_prompt_english if lang == "en" else system_prompt_dutch, HumanMessage(content=intent_prompt)])
#     intent = intent_response.content.strip()

#     # Handle casual greetings
#     if intent == "GREETING":
#         prompt = f"Respond warmly and conversationally to the user's greeting: '{user_input}'. Invite them to share how you can assist without mentioning a mental blueprint. Keep it short and human-like."
#         response = llm.invoke([system_prompt_english if lang == "en" else system_prompt_dutch, HumanMessage(content=prompt)])
#         return response.content

#     # Handle general help requests
#     if intent == "GENERAL_HELP":
#         prompt = f"The user said: '{user_input}'. Respond empathetically and ask for more details about what they’re going through to better understand their needs. Keep the response short and human-like, avoiding immediate suggestions of exercises or blueprints."
#         response = llm.invoke([system_prompt_english if lang == "en" else system_prompt_dutch, HumanMessage(content=prompt)])
#         return response.content

#     # Handle blueprint creation initiation
#     if intent == "BLUEPRINT" or any(word in user_input_lower for word in ["yes", "sure", "okay", "start", "let's do it", "let's start"]) and current_question_index == 0:
#         blueprint_responses = []
#         current_question_index = 1
#         return questions[0]

#     # Handle mental health issues or solution requests
#     if intent in ["ISSUE", "SOLUTION"]:
#         if has_blueprint and user_blueprint:
#             context = retriever.invoke(user_blueprint)
#             knowledge = "\n".join([doc.page_content for doc in context])
#             prompt = f"""
# The user mentioned a mental health issue or requested solutions: '{user_input}' and has an existing mental blueprint. Provide an empathetic response with tailored suggestions based on their existing blueprint, focusing on actionable exercises or techniques from the Workbook. For each suggestion, include specific Worksheet and Assignment numbers (e.g., "Assignment 3.2 from Worksheet 10"). Ensure suggestions are personalized to the user's blueprint.

# User's blueprint: {user_blueprint}
# Context from books: {knowledge}
# Conversation history: {chat_memory}
# """
#             response = llm.invoke([system_prompt_english if lang == "en" else system_prompt_dutch, HumanMessage(content=prompt)])
#             return response.content
#         elif has_blueprint and not user_blueprint:
#             prompt = f"""
# The user confirmed they have a mental blueprint but hasn’t shared its details: '{user_input}'. Respond empathetically and ask them to share some details from their mental blueprint to provide tailored solutions. If they decline, provide general solutions based on their stated issue, including specific Worksheet and Assignment numbers from the Workbook.

# Conversation history: {chat_memory}
# Keep the response concise and human-like.
# """
#             response = llm.invoke([system_prompt_english if lang == "en" else system_prompt_dutch, HumanMessage(content=prompt)])
#             return response.content
#         else:
#             prompt = f"""
# The user mentioned a mental health issue or requested solutions: '{user_input}'. Respond empathetically, acknowledging their struggle, and explain that creating a mental blueprint can help understand their feelings better. Then ask if they have already created a mental blueprint. Keep the response concise and human-like.
# """
#             response = llm.invoke([system_prompt_english if lang == "en" else system_prompt_dutch, HumanMessage(content=prompt)])
#             return response.content

#     # User confirms they have a blueprint
#     if intent == "HAS_BLUEPRINT":
#         if "my blueprint is" in user_input_lower:
#             user_blueprint = user_input.split("my blueprint is", 1)[-1].strip()
#         elif user_blueprint:  # Use existing blueprint if available
#             prompt = f"""
# The user confirmed they have a mental blueprint: '{user_input}'. Respond empathetically and ask if they would like to proceed with solutions based on their existing blueprint or create a new one to address any recent changes.

# User's existing blueprint: {user_blueprint}
# Conversation history: {chat_memory}
# Keep the response concise and human-like.
# """
#         else:
#             prompt = f"""
# The user confirmed they have a mental blueprint but hasn’t shared its details: '{user_input}'. Respond empathetically and ask them to share some details from their mental blueprint to provide tailored solutions. Alternatively, ask if they would like to create a new blueprint or proceed with general solutions.

# Conversation history: {chat_memory}
# Keep the response concise and human-like.
# """
#         response = llm.invoke([system_prompt_english if lang == "en" else system_prompt_dutch, HumanMessage(content=prompt)])
#         return response.content

#     # User declines to create a new blueprint
#     if any(word in user_input_lower for word in ["no", "not now", "don't want"]) and has_blueprint:
#         if user_blueprint:
#             context = retriever.invoke(user_blueprint)
#             knowledge = "\n".join([doc.page_content for doc in context])
#             prompt = f"""
# The user declined to create a new mental blueprint and mentioned: '{user_input}'. Provide an empathetic response with tailored suggestions based on their existing blueprint, focusing on actionable exercises or techniques from the Workbook. For each suggestion, include specific Worksheet and Assignment numbers (e.g., "Assignment 3.2 from Worksheet 10"). Ensure suggestions are personalized to the user's blueprint.

# User's blueprint: {user_blueprint}
# Context from books: {knowledge}
# Conversation history: {chat_memory}
# """
#             response = llm.invoke([system_prompt_english if lang == "en" else system_prompt_dutch, HumanMessage(content=prompt)])
#             return response.content
#         else:
#             prompt = f"""
# The user declined to create a new mental blueprint and mentioned: '{user_input}'. Since they confirmed having a blueprint but haven’t shared its details, respond empathetically and ask them to share some details from their mental blueprint to provide tailored solutions. If they decline, provide general solutions based on their stated issue, including specific Worksheet and Assignment numbers from the Workbook.

# Conversation history: {chat_memory}
# Keep the response concise and human-like.
# """
#             response = llm.invoke([system_prompt_english if lang == "en" else system_prompt_dutch, HumanMessage(content=prompt)])
#             return response.content

#     # User explicitly says they don't have a blueprint
#     if intent == "NO_BLUEPRINT":
#         prompt = f"""
# The user said they don't have a mental blueprint: '{user_input}'. Respond empathetically, explaining that there's no problem and that we can create a mental blueprint together using Johan's Main Book and Workbook. Ask if they would like to start creating a mental blueprint now. Keep the response concise and human-like.
# """
#         response = llm.invoke([system_prompt_english if lang == "en" else system_prompt_dutch, HumanMessage(content=prompt)])
#         return response.content

#     # Default response for unrelated input
#     prompt = f"The user said: '{user_input}'. Respond empathetically and guide them toward sharing their mental health concerns or starting a mental blueprint. Keep the response concise and human-like."
#     response = llm.invoke([system_prompt_english if lang == "en" else system_prompt_dutch, HumanMessage(content=prompt)])
#     return response.content

# # Main response function
# def get_rag_response(user_input):                                                                                                                                                                                            
#     lang = detect_language(user_input)
#     system_prompt = system_prompt_dutch if lang == 'nl' else system_prompt_english

#     blueprint_response = ask_about_mental_blueprint(user_input)
#     if blueprint_response:
#         chat_memory.append(HumanMessage(content=user_input))
#         chat_memory.append(AIMessage(content=blueprint_response))
#         return blueprint_response

#     # Fallback for general queries
#     context = retriever.invoke(user_input)
#     knowledge = "\n".join([doc.page_content for doc in context])
#     blueprint_info = user_blueprint if user_blueprint else "Not provided yet."
#     prompt = f"""
# Use the following context from Johan's books to provide a helpful and supportive answer.

# Context:
# {knowledge}

# Mental Blueprint (if available):
# {blueprint_info}

# User's question:
# {user_input}

# Provide an empathetic response, and if relevant, guide the user toward creating a mental blueprint. For each suggestion, include specific Worksheet and Assignment numbers (e.g., "Assignment 3.2 from Worksheet 10").
# """
#     messages = [system_prompt] + chat_memory + [HumanMessage(content=prompt)]
#     response = llm.invoke(messages)

#     chat_memory.append(HumanMessage(content=user_input))
#     chat_memory.append(AIMessage(content=response.content))
#     return response.content

# # Entry point
# def chat():
#     print("🧠 Welcome to Johan's Virtual Psychologist. Type your question in English or Dutch.")
#     while True:
#         user_input = input("\nYou: ").strip()
#         if user_input.lower() in ["exit", "quit"]:
#             print("Goodbye! Take care of yourself.")
#             break
#         answer = get_rag_response(user_input)
#         print(f"\n🤖 Answer: {answer}")

# if __name__ == "__main__":
#     chat()

















import os
import fitz  # PyMuPDF
import glob
import langdetect
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain_core.documents import Document

# Load environment variables
load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

# Global memory and blueprint
chat_memory = []
user_blueprint = None
blueprint_responses = []
current_question_index = 0

# Keywords
ANXIETY_KEYWORDS = [
    "anxiety", "anxious", "stress", "nervous", "panic", "worried", "fearful",
    "mental blueprint", "blueprint", "mental discomfort", "overwhelmed", "can't relax", "overthinking", "presure", "pressure"
]

# System prompts
system_prompt_english = SystemMessage(content="""
You are an AI chatbot designed to assist users with mental health issues based on the content of two specific books: the Main Book (001 Workbook) and the accompanying Workbook. Your primary goal is to guide users through a structured, empathetic, and conversational flow to identify their mental health issues and provide personalized solutions. Follow these steps for every user interaction:

1. **Casual Interaction**: If the user greets you casually (e.g., "hi", "hello", "hey"), respond warmly and conversationally, inviting them to share how you can assist without immediately mentioning a mental blueprint. Keep the response short and human-like.

2. **General Help Request**: If the user asks for help vaguely (e.g., "I need help"), respond empathetically and ask for more details about their situation to understand their needs better. Avoid suggesting exercises immediately.

3. **Intent Detection**: Analyze the user's input to determine their intent:
   - If the user requests solutions (e.g., "what can I do?", "how to fix"), check if they have a mental blueprint. If they do, provide solutions based on their blueprint. If not, ask if they’d like to create one or provide solutions based on their stated issue.
   - If the user mentions a mental health issue (e.g., "I have panic attacks") without requesting solutions, express empathy and ask if they have created a mental blueprint. Follow the blueprint flow if they agree, or provide solutions if they decline.
   - If the user wants to create a mental blueprint, follow the blueprint creation steps below.
   - If the user confirms they have a blueprint, ask if they want to create a new one or proceed with solutions.
   - If the user’s intent is unclear or unrelated, guide them empathetically toward sharing their mental health concerns.

4. **Mental Blueprint Creation**: If the user agrees to create a mental blueprint, guide them through these questions one at a time:
   - Step 1: "What are you struggling with emotionally or mentally?"
   - Step 2: "When do you most often experience this?"
   - Step 3: "What thoughts usually accompany those feelings?"
   - Step 4: "What past events might be related to these emotions?"
   - Step 5: "Do you notice any current habits or routines that affect how you feel?"
   Store each response. After collecting all responses, summarize the blueprint and provide tailored Workbook exercises with specific Worksheet and Assignment numbers (e.g., "Assignment 3.2 from Worksheet 10").

5. **If User Has a Mental Blueprint or Requests Solutions**: Use their blueprint or stated issues to fetch relevant exercises from the Main Book and Workbook. Include specific Worksheet and Assignment numbers.

6. **Maintaining the Flow**: Keep responses conversational, empathetic, and concise. If the user asks unrelated questions, gently redirect to their mental health concerns. Do not ask all blueprint questions at once.

7. **Content Restrictions**: Use only the Main Book (001 Workbook) and Workbook. Clarify this if other books are mentioned.

8. **Personalized Solutions**: Tailor responses to the user’s issues or blueprint with specific Workbook exercises. Acknowledge their unique challenges.

9. **Tone and Style**: Use a supportive, empathetic, and professional tone. Keep responses human-like and avoid overly technical jargon.
""")
system_prompt_dutch = SystemMessage(content="""
Je bent een AI-chatbot ontworpen om gebruikers te helpen met mentale gezondheidsproblemen op basis van de inhoud van twee specifieke boeken: het Hoofdboek (001 Werkboek) en het bijbehorende Werkboek. Je primaire doel is om gebruikers door een gestructureerde, empathische en conversationele flow te leiden om hun mentale gezondheidsproblemen te identificeren en gepersonaliseerde oplossingen te bieden. Volg deze stappen voor elke interactie:

1. **Casuele Interactie**: Als de gebruiker je informeel begroet (bijv. "hallo", "hey"), reageer warm en conversationeel, en nodig hen uit om te delen hoe je kunt helpen zonder meteen naar een mentale blauwdruk te vragen. Houd de reactie kort en menselijk.

2. **Algemene Hulpvraag**: Als de gebruiker vaag om hulp vraagt (bijv. "Ik heb hulp nodig"), reageer empathisch en vraag om meer details over hun situatie om hun behoeften beter te begrijpen. Vermijd het direct voorstellen van oefeningen.

3. **Intentie Detectie**: Analyseer de input van de gebruiker om hun intentie te bepalen:
   - Als de gebruiker om oplossingen vraagt (bijv. "Wat kan ik doen?", "Hoe los ik dit op?"), controleer of ze een mentale blauwdruk hebben. Als ze die hebben, bied oplossingen gebaseerd op hun blauwdruk. Zo niet, vraag of ze er een willen maken of bied oplossingen gebaseerd op hun genoemde probleem.
   - Als de gebruiker een mentaal gezondheidsprobleem noemt (bijv. "Ik heb paniekaanvallen") zonder om oplossingen te vragen, toon empathie en vraag of ze een mentale blauwdruk hebben gemaakt. Volg de blauwdrukstroom als ze instemmen, of bied oplossingen als ze weigeren.
   - Als de gebruiker een mentale blauwdruk wil maken, volg de onderstaande stappen voor het maken van de blauwdruk.
   - Als de gebruiker bevestigt dat ze een blauwdruk hebben, vraag of ze een nieuwe willen maken of oplossingen willen op basis van de bestaande blauwdruk.
   - Als de intentie onduidelijk of niet gerelateerd is, leid hen empathisch naar het delen van hun mentale gezondheidsproblemen.

4. **Mentale Blauwdruk Creatie**: Als de gebruiker instemt met het maken van een mentale blauwdruk, leid hen door de volgende vragen één voor één:
   - Stap 1: "Waarmee worstelt u emotioneel of mentaal?"
   - Stap 2: "Wanneer ervaart u dit het vaakst?"
   - Stap 3: "Welke gedachten gaan meestal gepaard met die gevoelens?"
   - Stap 4: "Welke gebeurtenissen uit het verleden kunnen verband houden met deze emoties?"
   - Stap 5: "Merkt u huidige gewoonten of routines op die invloed hebben op hoe u zich voelt?"
   Sla elke reactie op. Vat na alle antwoorden de blauwdruk samen en beveel Werkboek-oefeningen aan met specifieke Worksheet- en Assignment-nummers (bijv. "Assignment 3.2 van Worksheet 10").

5. **Als de Gebruiker een Mentale Blauwdruk Heeft of Oplossingen Vraagt**: Gebruik hun blauwdruk of genoemde problemen om relevante oefeningen uit het Hoofdboek en Werkboek te halen. Voeg specifieke Worksheet- en Assignment-nummers toe.

6. **Het Behouden van de Flow**: Houd antwoorden conversationeel, empathisch en beknopt. Als de gebruiker niet-relevante vragen stelt, stuur vriendelijk terug naar hun mentale gezondheidsproblemen.

7. **Inhoudsbeperkingen**: Gebruik alleen het Hoofdboek (001 Werkboek) en Werkboek. Verduidelijk dit als andere boeken worden genoemd.

8. **Gepersonaliseerde Oplossingen**: Stem antwoorden af op de blauwdruk of genoemde problemen met specifieke Werkboek-oefeningen. Erken de uniciteit van de uitdagingen van de gebruiker.

9. **Toon en Stijl**: Gebruik een ondersteunende, empathische en professionele toon. Houd reacties menselijk en vermijd overdreven technisch jargon.
""")

# Language detection
def detect_language(text):
    try:
        lang = langdetect.detect(text)
        return "nl" if lang == "nl" else "en"
    except:
        return "en"

# PDF reader
def extract_text_from_all_pdfs(folder_path):
    combined_texts = []
    pdf_files = glob.glob(os.path.join(folder_path, "*.pdf"))
    for pdf_file in pdf_files:
        try:
            with fitz.open(pdf_file) as doc:
                text = "".join(page.get_text() + "\n" for page in doc)
                combined_texts.append(Document(page_content=text.strip()))
                print(f"✅ Loaded: {os.path.basename(pdf_file)}")
        except Exception as e:
            print(f"❌ Failed to process {pdf_file}: {e}")
    return combined_texts

# PDF -> FAISS
pdf_folder = "data"
documents = extract_text_from_all_pdfs(pdf_folder)
splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=200)
split_docs = splitter.split_documents(documents)

faiss_path = "faiss_db_johan"
if os.path.exists(faiss_path):
    vectordb = FAISS.load_local(faiss_path, OpenAIEmbeddings(), allow_dangerous_deserialization=True)
else:
    vectordb = FAISS.from_documents(split_docs, OpenAIEmbeddings())
    vectordb.save_local(faiss_path)

retriever = vectordb.as_retriever(search_kwargs={"k": 3})
llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.6)

# Blueprint conversation
def ask_about_mental_blueprint(user_input):
    global user_blueprint, blueprint_responses, current_question_index
    user_input_lower = user_input.lower()
    lang = detect_language(user_input)

    # Define blueprint questions
    questions = [
        "What are you struggling with emotionally or mentally?",
        "When do you most often experience this?",
        "What thoughts usually accompany those feelings?",
        "What past events might be related to these emotions?",
        "Do you notice any current habits or routines that affect how you feel?"
    ] if lang == "en" else [
        "Waarmee worstelt u emotioneel of mentaal?",
        "Wanneer ervaart u dit het vaakst?",
        "Welke gedachten gaan meestal gepaard met die gevoelens?",
        "Welke gebeurtenissen uit het verleden kunnen verband houden met deze emoties?",
        "Merkt u huidige gewoonten of routines op die invloed hebben op hoe u zich voelt?"
    ]

    # Handle blueprint creation process if already in progress
    if current_question_index > 0:
        blueprint_responses.append(user_input)
        current_question_index += 1

        if current_question_index < len(questions):
            return questions[current_question_index]

        # Summarize blueprint and suggest solutions
        summary = "Your mental blueprint has been created!\n" if lang == "en" else "Uw mentale blauwdruk is gemaakt!\n"
        for q, r in zip(questions, blueprint_responses):
            summary += f"- {q}: {r}\n"
        user_blueprint = summary
        context = retriever.invoke(user_blueprint)
        knowledge = "\n".join([doc.page_content for doc in context])
        prompt = f"""
Based on the user's mental blueprint and the content from the Main Book and Workbook, suggest specific exercises or techniques to address their mental health issues.

User's blueprint: {user_blueprint}
Context from books: {knowledge}

Provide an empathetic response with tailored suggestions, focusing on actionable exercises or techniques from the Workbook. For each suggestion, include specific Worksheet and Assignment numbers (e.g., "Assignment 3.2 from Worksheet 10"). Ensure suggestions are personalized to the user's blueprint.
"""
        response = llm.invoke([system_prompt_english if lang == "en" else system_prompt_dutch, HumanMessage(content=prompt)])
        blueprint_responses.clear()
        current_question_index = 0
        return f"{summary}\n{response.content}"

    # Check conversation history for previous blueprint confirmation
    has_blueprint = any("i have a mental blueprint" in msg.content.lower() or "my blueprint is" in msg.content.lower() for msg in chat_memory if isinstance(msg, HumanMessage))

    # Detect user intent using AI
    intent_prompt = f"""
Analyze the user's input to determine their intent: '{user_input}'.
- If the user is greeting you casually (e.g., "hi", "hello", "hey", "yo", "hiya", "good morning", "good day"), respond with 'GREETING'.
- If the user is requesting general help (e.g., "I need help", "help me"), respond with 'GENERAL_HELP'.
- If the user is requesting solutions (e.g., "what can I do?", "suggest something", "how to fix", "give me solutions", "what should i do?"), respond with 'SOLUTION'.
- If the user is mentioning a mental health issue without explicitly requesting solutions (e.g., "I feel anxious", "I have panic attacks", "I have a mental presure"), respond with 'ISSUE'.
- If the user expresses a desire to create a mental blueprint (e.g., "guide me", "I want to create a blueprint", "let's make one"), respond with 'BLUEPRINT'.
- If the user confirms they have a blueprint (e.g., "I have a mental blueprint", "my blueprint is"), respond with 'HAS_BLUEPRINT'.
- If the user’s intent is unclear or unrelated, respond with 'UNRELATED'.
Examples:
- Input: "i have a mental presure in office time . so now tell me what should i do?" -> Intent: SOLUTION
- Input: "I feel stressed at work" -> Intent: ISSUE
- Input: "hii" -> Intent: GREETING
- Input: "I want to create a blueprint" -> Intent: BLUEPRINT
"""
    intent_response = llm.invoke([system_prompt_english if lang == "en" else system_prompt_dutch, HumanMessage(content=intent_prompt)])
    intent = intent_response.content.strip()

    # Handle casual greetings
    if intent == "GREETING":
        prompt = f"Respond warmly and conversationally to the user's greeting: '{user_input}'. Invite them to share how you can assist without mentioning a mental blueprint. Keep it short and human-like."
        response = llm.invoke([system_prompt_english if lang == "en" else system_prompt_dutch, HumanMessage(content=prompt)])
        return response.content

    # Handle general help requests
    if intent == "GENERAL_HELP":
        prompt = f"The user said: '{user_input}'. Respond empathetically and ask for more details about what they’re going through to better understand their needs. Keep the response short and human-like, avoiding immediate suggestions of exercises or blueprints."
        response = llm.invoke([system_prompt_english if lang == "en" else system_prompt_dutch, HumanMessage(content=prompt)])
        return response.content

    # Handle blueprint creation initiation
    if intent == "BLUEPRINT" or any(word in user_input_lower for word in ["yes", "sure", "okay", "start", "let's do it"]) and current_question_index == 0:
        blueprint_responses = []
        current_question_index = 1
        return questions[0]

    # Handle mental health issues or solution requests
    if intent in ["ISSUE", "SOLUTION"]:
        if has_blueprint and user_blueprint:
            context = retriever.invoke(user_blueprint)
            knowledge = "\n".join([doc.page_content for doc in context])
            prompt = f"""
The user mentioned a mental health issue or requested solutions: '{user_input}' and has an existing mental blueprint. Provide an empathetic response with tailored suggestions based on their existing blueprint, focusing on actionable exercises or techniques from the Workbook. For each suggestion, include specific Worksheet and Assignment numbers (e.g., "Assignment 3.2 from Worksheet 10"). Ensure suggestions are personalized to the user's blueprint.

User's blueprint: {user_blueprint}
Context from books: {knowledge}
Conversation history: {chat_memory}
"""
            response = llm.invoke([system_prompt_english if lang == "en" else system_prompt_dutch, HumanMessage(content=prompt)])
            return response.content
        else:
            prompt = f"""
The user mentioned a mental health issue or requested solutions: '{user_input}'. Respond empathetically, acknowledging their struggle, and explain that creating a mental blueprint can help understand their feelings better. Then ask if they have already created a mental blueprint. Keep the response concise and human-like.
"""
            response = llm.invoke([system_prompt_english if lang == "en" else system_prompt_dutch, HumanMessage(content=prompt)])
            return response.content

    # User confirms they have a blueprint
    if intent == "HAS_BLUEPRINT":
        if "my blueprint is" in user_input_lower:
            user_blueprint = user_input.split("my blueprint is", 1)[-1].strip()
        else:
            user_blueprint = user_input
        prompt = f"""
The user confirmed they have a mental blueprint: '{user_input}'. Respond empathetically and ask if they would like to create a new mental blueprint or proceed with solutions based on their existing blueprint. Include the conversation history to ensure context is maintained.

Conversation history: {chat_memory}
Keep the response concise and human-like.
"""
        response = llm.invoke([system_prompt_english if lang == "en" else system_prompt_dutch, HumanMessage(content=prompt)])
        return response.content

    # User declines to create a new blueprint
    if any(word in user_input_lower for word in ["no", "not now", "don't want"]) and has_blueprint and user_blueprint and current_question_index == 0:
        context = retriever.invoke(user_blueprint)
        knowledge = "\n".join([doc.page_content for doc in context])
        prompt = f"""
The user declined to create a new mental blueprint and mentioned: '{user_input}'. Provide an empathetic response with tailored suggestions based on their existing blueprint, focusing on actionable exercises or techniques from the Workbook. For each suggestion, include specific Worksheet and Assignment numbers (e.g., "Assignment 3.2 from Worksheet 10"). Ensure suggestions are personalized to the user's blueprint.

User's blueprint: {user_blueprint}
Context from books: {knowledge}
Conversation history: {chat_memory}
"""
        response = llm.invoke([system_prompt_english if lang == "en" else system_prompt_dutch, HumanMessage(content=prompt)])
        return response.content

    # User explicitly says they don't have a blueprint
    if "i don't have a mental blueprint" in user_input_lower or "no blueprint" in user_input_lower:
        prompt = f"""
The user said they don't have a mental blueprint: '{user_input}'. Respond empathetically, explaining that there's no problem and that we can create a mental blueprint together using Johan's Main Book and Workbook. Ask if they would like to start creating a mental blueprint now. Keep the response concise and human-like.
"""
        response = llm.invoke([system_prompt_english if lang == "en" else system_prompt_dutch, HumanMessage(content=prompt)])
        return response.content

    # Default response for unrelated input
    prompt = f"The user said: '{user_input}'. Respond empathetically and guide them toward sharing their mental health concerns or starting a mental blueprint. Keep the response concise and human-like."
    response = llm.invoke([system_prompt_english if lang == "en" else system_prompt_dutch, HumanMessage(content=prompt)])
    return response.content

# Main response function
def get_rag_response(user_input):                                                                                                                                                                                            
    lang = detect_language(user_input)
    system_prompt = system_prompt_dutch if lang == 'nl' else system_prompt_english

    blueprint_response = ask_about_mental_blueprint(user_input)
    if blueprint_response:
        chat_memory.append(HumanMessage(content=user_input))
        chat_memory.append(AIMessage(content=blueprint_response))
        return blueprint_response

    # Fallback for general queries
    context = retriever.invoke(user_input)
    knowledge = "\n".join([doc.page_content for doc in context])
    blueprint_info = user_blueprint if user_blueprint else "Not provided yet."
    prompt = f"""
Use the following context from Johan's books to provide a helpful and supportive answer.

Context:
{knowledge}

Mental Blueprint (if available):
{blueprint_info}

User's question:
{user_input}

Provide an empathetic response, and if relevant, guide the user toward creating a mental blueprint. For each suggestion, include specific Worksheet and Assignment numbers (e.g., "Assignment 3.2 from Worksheet 10").
"""
    messages = [system_prompt] + chat_memory + [HumanMessage(content=prompt)]
    response = llm.invoke(messages)

    chat_memory.append(HumanMessage(content=user_input))
    chat_memory.append(AIMessage(content=response.content))
    return response.content

# Entry point
def chat():
    print("🧠 Welcome to Johan's Virtual Psychologist. Type your question in English or Dutch.")
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye! Take care of yourself.")
            break
        answer = get_rag_response(user_input)
        print(f"\n🤖 Answer: {answer}")

if __name__ == "__main__":
    chat()