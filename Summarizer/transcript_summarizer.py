"""
This file generates summary of youtube transcripts
"""
from typing import List, Dict
from langchain_openai import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel
from dotenv import load_dotenv
import os, time

load_dotenv()

class TranscriptSummarizer:
    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            model="gpt-4o-mini", 
            temperature=0.3
        )

        self.map_prompt = PromptTemplate.from_template(
            """
            You will be provided with a chunk and you need to smmarize the key points of that chunk:
            Below is the chunk\n
            {chunk}
            """
        )

        self.reduce_prompt = PromptTemplate.from_template(
            """
            You will be provided with a combined summary of different chunks. You need to generate a summary such that it is consistent and in a natural flow. Below is the combined summary\n
            {combined_summary}
            """
        )

    def generate_chunks(self, transcript: str) -> List[Document]:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        texts = text_splitter.split_text(transcript)
        chunks = [Document(page_content=chunk) for chunk in texts]
        return chunks

    def generate_summary(self, chunks: List[Document]) -> str:
        print(f"\n🟡 Total Chunks to summarize: {len(chunks)}")

        map_chain = (
            {"chunk": lambda chunk: chunk}
            | self.map_prompt
            | self.llm
            | (lambda output : output.content)
        )

        reduce_chain = (
            self.reduce_prompt
            |self.llm
            | (lambda output : output.content)
        )

        map_parallel = RunnableParallel(
            {str(i): map_chain for i in range(len(chunks))}
        )

        inputs = {str(i):chunk.page_content for i, chunk in enumerate(chunks)}

        def join_summaries(results : Dict) -> Dict[str,str]:
            summaries = list(results.values())
            print(f"\n🟢 Finished mapping {len(summaries)} chunks. Combining summaries...")
            return {"combined_summary":"\n\n".join(summaries)}

        full_chain = (
            map_parallel
            | join_summaries
            | reduce_chain
        )
        total_start = time.time()
        print("\n🚀 Starting summarization process...")
        result = full_chain.invoke(inputs)
        total_time = time.time() - total_start
        print(f"\n🎉 Summary generation completed in {total_time:.2f} seconds\n")
        return result