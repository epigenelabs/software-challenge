from sqlalchemy.orm import Session
from typing import List


from models import Gene, Geneset
from schemas import GenesetCreate, GeneCreate


"""For genesets:"""

def get_genesets(db: Session, skip: int = 0, limit: int = 100):
    """GET all genesets, default limit 100"""

    return db.query(Geneset).offset(skip).limit(limit).all()


def get_geneset_by_title(db: Session, pattern: str):
    """GET specific genesets, search by title"""

    return db.query(Geneset).filter(Geneset.title.like("%" + pattern + "%")).all()


def get_geneset(db: Session, geneset_id: int):
    """GET a single geneset by geneset_id"""

    return db.query(Geneset).filter(Geneset.id == geneset_id).first()


# PUT a single geneset by geneset_id
def update_geneset(db: Session, geneset_id: int, title: str, genes: List[str]):
    """PUT a single geneset by geneset_id"""

    geneset = db.query(Geneset).filter(Geneset.id == geneset_id).first()
    geneset.title = title

    db.query(Gene).filter(Gene.geneset_id == geneset_id).delete()
    for gene in genes:
        geneset.genes.append(Gene(name=gene.name))

    db.commit()
    return geneset


def create_geneset_with_genes(db: Session, geneset: GenesetCreate):
    """POST a single geneset with genes"""

    db_geneset = Geneset(title=geneset.title)
    db.add(db_geneset)

    for gene in geneset.genes:
        db_geneset.genes.append(Gene(name=gene.name))

    db.commit()
    db.refresh(db_geneset)
    return db_geneset


# POST a single geneset (Currently not in use)
# def create_geneset(db: Session, geneset: GenesetCreate):
#     db_geneset = Geneset(title=geneset.title)
#     db.add(db_geneset)
#     db.commit()
#     db.refresh(db_geneset)
#     return db_geneset


# (Currently not in use)
# def create_geneset_item(db: Session, item: GeneCreate, geneset_id: int):
#     db_gene = Gene(**item.dict(), geneset_id=geneset_id)
#     db.add(db_gene)
#     db.commit()
#     db.refresh(db_gene)
#     return db_gene


def get_genes(db: Session, skip: int = 0, limit: int = 100):
    """GET all genes"""

    return db.query(Gene).offset(skip).limit(limit).all()


def get_gene_by_name(db: Session, pattern: str):
    """GET specific genes, search by name"""

    return db.query(Gene).filter(Gene.name.like("%" + pattern + "%")).all()


def get_gene(db: Session, gene_id: int):
    """GET a single gene by gene_id"""

    return db.query(Gene).filter(Gene.id == gene_id).first()
