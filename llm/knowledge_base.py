from phi.knowledge.pdf import PDFKnowledgeBase
from phi.knowledge.arxiv import ArxivKnowledgeBase
from phi.knowledge.website import WebsiteKnowledgeBase
from phi.vectordb.pgvector import PgVector

from db.session import db_url

pdf_knowledge_base = PDFKnowledgeBase(
    path="data/pdfs",
    vector_db=PgVector(
        collection="pdf_documents",
        db_url=db_url,
    ),
)

arxiv_knowledge_base = ArxivKnowledgeBase(
    # See the arXiv API for Query Construction: https://arxiv.org/help/api/user-manual#query_details
    queries=["ti:Generative AI", "ti:LLM", "ti:AI", "ti:AI Security"],
    vector_db=PgVector(
        collection="arxiv_documents",
        db_url=db_url,
    ),
)

website_knowledge_base = WebsiteKnowledgeBase(
    urls=["https://www.phidata.com"],
    max_links=10,
    vector_db=PgVector(
        collection="website_documents",
        db_url=db_url,
    ),
)
