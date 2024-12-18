
from phi.knowledge.pdf import PDFKnowledgeBase, PDFReader
from phi.vectordb.pgvector import PgVector
from phi.agent import Agent

class KnowledgeBaseManager:
    def __init__(self, 
                 pdf_path="data/pdfs", 
                 table_name="pdf_documents", 
                 db_url="postgresql+psycopg://ai:ai@localhost:5532/ai", 
                 chunk=True):
        """
        Initializes the KnowledgeBaseManager.

        :param pdf_path: Path to the directory containing PDFs.
        :param table_name: Name of the table in the vector database.
        :param db_url: Database connection URL.
        :param chunk: Whether to enable chunking for the PDFReader.
        """
        self.pdf_path = pdf_path
        self.table_name = table_name
        self.db_url = db_url
        self.chunk = chunk
        self.knowledge_base = None

    def initialize_knowledge_base(self):
        """
        Initializes the PDFKnowledgeBase instance.
        """
        vector_db = PgVector(
            table_name=self.table_name,
            db_url=self.db_url
        )
        reader = PDFReader(chunk=self.chunk)
        self.knowledge_base = PDFKnowledgeBase(
            path=self.pdf_path,
            vector_db=vector_db,
            reader=reader
        )

    def get_knowledge_base(self):
        """
        Returns the initialized PDFKnowledgeBase instance.

        :return: PDFKnowledgeBase instance
        """
        if self.knowledge_base is None:
            self.initialize_knowledge_base()
        return self.knowledge_base

class AgentManager:
    def __init__(self, knowledge_base_manager):
        """
        Initializes the AgentManager with a KnowledgeBaseManager.

        :param knowledge_base_manager: Instance of KnowledgeBaseManager.
        """
        self.knowledge_base_manager = knowledge_base_manager
        self.agent = None

    def initialize_agent(self, search_knowledge=True, recreate=False):
        """
        Initializes the Agent instance.

        :param search_knowledge: Whether the agent should search the knowledge base.
        :param recreate: Whether to recreate the knowledge base.
        """
        knowledge_base = self.knowledge_base_manager.get_knowledge_base()
        self.agent = Agent(
            knowledge=knowledge_base,
            search_knowledge=search_knowledge
        )
        self.agent.knowledge.load(recreate=recreate)

    def get_agent(self):
        """
        Returns the initialized Agent instance.

        :return: Agent instance
        """
        if self.agent is None:
            self.initialize_agent()
        return self.agent

    def ask_agent(self, query):
        """
        Asks the agent a question and prints the response.

        :param query: The question to ask the agent.
        """
        if self.agent is None:
            self.initialize_agent()
        self.agent.print_response(query)


