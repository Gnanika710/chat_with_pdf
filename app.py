import streamlit as st
import openai
from dotenv import load_dotenv
import os
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
import pytesseract
from PIL import Image
from gtts import gTTS
import tempfile
import streamlit.components.v1 as components
from htmlTemplates import user_template, bot_template, typing_indicator_template, css  




def get_text_chunks(raw_text):
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return text_splitter.split_text(raw_text)

def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    return FAISS.from_texts(text_chunks, embeddings)

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    return ConversationalRetrievalChain.from_llm(llm, vectorstore.as_retriever(), memory=memory)

def get_pdf_text(pdf_docs, page_number=None):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        if page_number:
            if 1 <= page_number <= len(pdf_reader.pages):
                page = pdf_reader.pages[page_number - 1]  # Zero-indexed
                page_text = page.extract_text()
                if page_text:
                    text += page_text
                else:
                    st.warning(f"Page {page_number} of the PDF is empty or not readable.")
            else:
                st.error(f"Page {page_number} is out of range for the uploaded PDF.")
        else:
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                text += page_text if page_text else ""
    return text

def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        st.audio(fp.name, format="audio/mp3")

def handle_userinput(user_question):
    typing_indicator = st.empty()
    typing_indicator.markdown(typing_indicator_template, unsafe_allow_html=True)

    
    if "chat_history" not in st.session_state or st.session_state.chat_history is None:
        st.session_state.chat_history = []
    
    
    response = st.session_state.conversation({
        'question': user_question,
        'chat_history': st.session_state.chat_history
    })

    typing_indicator.empty()

   
    
    st.session_state.chat_history = response['chat_history']

    
    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
            text_to_speech(message.content)

    

def main():
    load_dotenv()
    openai.api_key = os.getenv('OPENAI_API_KEY')
    if not openai.api_key:
        st.error("API key not found. Please check your .env file.")
        return

    st.set_page_config(page_title="Chat with multiple PDFs", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)  # Inject the CSS for styling
    
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with multiple PDFs :books:")
    
    with st.sidebar:
        play_music = st.checkbox("Play Background Music")
        if play_music:
            st.markdown(background_music, unsafe_allow_html=True) 

        st.subheader("Choose Your Avatar")
        user_avatar_url = st.text_input("Enter URL of your avatar:", value="https://i.scdn.co/image/ab67616d00001e02964a582949cbf461ce54375f")
        bot_avatar_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRdJGnVoEMYC_2cdHJLZPezjqse6nLYURLcCQ&s"

        global user_template, bot_template
        user_template = f'''
        <div class="chat-message user">
            <div class="avatar">
                <img src="{user_avatar_url}">
            </div>
            <div class="message">{{{{MSG}}}}</div>
        </div>
        '''

        bot_template = f'''
        <div class="chat-message bot">
            <div class="avatar">
                <img src="{bot_avatar_url}">
            </div>
            <div class="message">{{{{MSG}}}}</div>
        </div>
        '''

    user_question = st.text_input("Ask a question about your documents:")
    page_number = st.number_input("Enter the page number to read (leave blank to read all):", min_value=1, step=1, format="%d")
    page_number = page_number if page_number > 0 else None  # Convert to None if not specified

    if user_question:
        if st.session_state.conversation is not None:
            handle_userinput(user_question)
        else:
            st.warning("Please process the PDFs before asking questions.")

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing..."):
                if pdf_docs:
                    raw_text = get_pdf_text(pdf_docs, page_number)
                    if raw_text.strip():  # Ensure text isn't empty
                        text_chunks = get_text_chunks(raw_text)
                        vectorstore = get_vectorstore(text_chunks)
                        st.session_state.conversation = get_conversation_chain(vectorstore)
                    else:
                        st.warning("The specified page or document is empty or couldn't be read.")
                else:
                    st.error("Please upload some PDFs.")

if __name__ == '__main__':
    main()
