from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# For genesets:

@app.get("/genesets", response_model=List[schemas.Geneset])
def read_all_genesets(db: Session = Depends(get_db)):
    """GET all genesets"""

    genesets = crud.get_genesets(db)
    return genesets


@app.get("/genesets/search", response_model=List[schemas.Geneset])
# '/genesets/search?title=my_set1' is better than 'genesets/search/my_set1'
# because when a geneset has more attributes and you want to put multiple attributes
# in a search query, you can do like '/genesets/search?title=my_set1&nucleotide=guanine'
def read_match_genesets(title: str, db: Session = Depends(get_db)):
    """GET specific genesets, search by title"""

    genesets = crud.get_geneset_by_title(db, title)
    return genesets

@app.get("/genesets/{geneset_id}", response_model=schemas.Geneset)
def read_geneset(geneset_id: int, db: Session = Depends(get_db)):

    """GET a single geneset by geneset_id"""
    return crud.get_geneset(db, geneset_id)


@app.put("/genesets/{geneset_id}", response_model=schemas.Geneset)
def update_genesets(
    geneset_id: int, geneset: schemas.GenesetCreate, db: Session = Depends(get_db)
):
    """PUT a single geneset by geneset_id"""

    return crud.update_geneset(db, geneset_id, geneset.title, geneset.genes)


@app.post("/genesets")
def create_geneset(geneset: schemas.GenesetCreate, db: Session = Depends(get_db)):
    """POST a single geneset with genes"""

    db_geneset = crud.create_geneset_with_genes(db, geneset)
    return db_geneset.id


# For genes:

@app.get("/genes", response_model=List[schemas.Gene])
def read_all_genes(db: Session = Depends(get_db)):
    """GET all genes"""

    return crud.get_genes(db)


@app.get("/genes/search", response_model=List[schemas.Gene])
# for the same reason as '/genesets/search'
def read_match_genes(name: str, db: Session = Depends(get_db)):
    """GET specific genes, search by name"""

    genes = crud.get_gene_by_name(db, name)
    return genes


@app.get("/genes/{gene_id}", response_model=schemas.Gene)
def read_gene(gene_id: int, db: Session = Depends(get_db)):
    """GET a single gene by gene_id"""

    return crud.get_gene(db, gene_id)
