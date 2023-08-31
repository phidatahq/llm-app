from phi.knowledge.pdf import PDFKnowledgeBase
from phi.knowledge.arxiv import ArxivKnowledgeBase
from phi.knowledge.website import WebsiteKnowledgeBase
from phi.vectordb.pgvector import PgVector

from db.session import db_url

pdf_knoweldge_base = PDFKnowledgeBase(
    path="data/pdfs",
    vector_db=PgVector(
        collection="pdf_documents",
        db_url=db_url,
    ),
)

arxiv_knowledge_base = ArxivKnowledgeBase(
    vector_db=PgVector(
        collection="arxiv_documents",
        db_url=db_url,
    ),
)

website_knowledge_base = WebsiteKnowledgeBase(
    urls=["https://www.phidata.com/"],
    vector_db=PgVector(
        collection="website_documents",
        db_url=db_url,
    ),
)
