import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from htmlTemplate import css, bot_template, user_template


def read_pdf(pdf_files):
    raw_text = ""
    for pdf in pdf_files:
        pdfReader = PdfReader(pdf)
        for page in pdfReader.pages:
            raw_text += page.extract_text()
    return raw_text


def get_chunks(raw_text):
    splitter = CharacterTextSplitter(
        separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len
    )
    text_chunks = splitter.split_text(raw_text)
    return text_chunks


def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm, retriever=vectorstore.as_retriever(), memory=memory
    )
    return conversation_chain


def handle_usrinput(usr_ques):
    response = st.session_state.conversation({"question": usr_ques})
    st.session_state.chat_history = response["chat_history"]

    for i, message in enumerate(response["chat_history"]):
        if i % 2 == 0:
            st.write(
                user_template.replace("{{MSG}}", message.content),
                unsafe_allow_html=True,
            )
        else:
            st.write(
                bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True
            )


def main():
    load_dotenv()
    st.set_page_config(page_title="PDFGPT", page_icon=":book:", layout="wide")

    st.write(f"<style>{css}</style>", unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("PDFGPT")

    usr_ques = st.text_input("Ask me what you want!")
    if usr_ques:
        handle_usrinput(usr_ques)

    with st.sidebar:
        st.sidebar.header("Your pdfs")
        pdf_files = st.file_uploader("Choose a file", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing..."):
                # get pdf files
                raw_text = read_pdf(pdf_files)
                # split text into chunks
                text_chunks = get_chunks(raw_text)
                # store chunks in vectorstore
                vectorstore = get_vectorstore(text_chunks)
                # create conversation chain
                st.session_state.conversation = get_conversation_chain(vectorstore)

                st.success("Done!")
                st.balloons()


if __name__ == "__main__":
    main()
