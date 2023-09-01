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
    # Use PgVector to store the arXiv knowledge base
    # Table name: arxiv_documents
    vector_db=PgVector(
        collection="arxiv_documents",
        db_url=db_url,
    ),
)

website_knowledge_base = WebsiteKnowledgeBase(
    urls=["https://www.phidata.com"],
    # Maximal number of links to follow from the seed URLs
    max_links=10,
    # Use PgVector to store the website knowledge base
    # Table name: website_documents
    vector_db=PgVector(
        collection="website_documents",
        db_url=db_url,
    ),
)
