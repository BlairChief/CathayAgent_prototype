import os
from dotenv import load_dotenv
from phi.vectordb.pgvector import PgVector
from phi.knowledge.pdf import PDFKnowledgeBase, PDFReader

load_dotenv()

class PdfKnowledgeBase:
    def __init__(
        self, 
        source_path="data/pdfs", 
        table_name="pdfs", 
        db_url=os.getenv('DB_URL'), 
        chunk=True
    ):
        self.source_path = source_path
        self.table_name = table_name
        self.db_url = db_url
        self.chunk = chunk
        self.pdf_knowledge_base = None

    def initialize_knowledge_base(self):
        vector_db = PgVector(
            table_name=self.table_name,
            db_url=self.db_url
        )
        reader = PDFReader(chunk=self.chunk)
        self.pdf_knowledge_base = PDFKnowledgeBase(
            path=self.source_path,
            vector_db=vector_db,
            reader=reader
        )

    def get_knowledge_base(self):
        if self.pdf_knowledge_base is None:
            self.initialize_knowledge_base()
        return self.pdf_knowledge_base