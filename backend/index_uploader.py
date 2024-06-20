import chromadb
from langchain_community.document_loaders.pdf import PyMuPDFLoader
from os import listdir
from langchain_text_splitters import RecursiveCharacterTextSplitter
import pymupdf
import re
import io
from PIL import Image

def add_document(arxivId: str, title: str, authors: str, year: int, figureStdAnnot: str = 'Fig. '):
    """
    Adds a documents to the index

    Args:
        arxivId: arXiv ID of the paper (also name of the pdf file)
        title: title of the paper
        authors: authors of the paper
        year: year of pubblication of the paper
        figureStdAnnot: standard annotation for figures in the paper
    """

    client = chromadb.PersistentClient(path="./data/chroma_db")

    collection = client.get_or_create_collection("my-papers")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=5000,
        chunk_overlap=100
    )

    loader = PyMuPDFLoader(f"./data/papers/{arxivId}.pdf")
    docs = loader.load_and_split(text_splitter)

    i = 1

    for doc in docs:

        collection.add(
            documents=[re.sub(r'(\w|[,\"\'\s])\n', r'\1 ', doc.page_content)], 
            metadatas=[{"title": title,
                        "authors": authors,
                        "year": year,
                        "arxivId": arxivId}],
            ids=[f"{arxivId}_{i}"],
        )
        i += 1

    captions = __extractImages(arxivId, figureStdAnnot)
    print(captions)

    i = 1
    for key,value in captions.items():
        collection.add(
            documents=[value],
            metadatas=[{"title": title,
                        "authors": authors,
                        "year": year,
                        "arxivId": arxivId,
                        "image": key
                        }], 
            ids=[f"{arxivId}_image{i}"], 
        )
        i += 1

def __extractImages(arxivId, figureStdAnnot):
    """
    Extracts and saves figures from the paper and returns their captions

    Args:
        arxivId: arXiv ID of the paper (also name of the pdf file)
        figureStdAnnot: standard annotation for figures in the paper

    Returns:
        Dict: figure captions, with the key as the figure number
    """

    doc = pymupdf.open(f"./data/papers/{arxivId}.pdf")

    i = 1

    captions = {}

    # iterate over pdf pages
    for page in doc:

        for img in page.get_images():
            # get the XREF of the image
            xref = img[0]
            # extract the image bytes
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            # get the image extension
            image_ext = base_image["ext"]
            # load it to PIL
            image = Image.open(io.BytesIO(image_bytes))
            # save it to local disk
            image.save(open(f"./data/images/{arxivId}_image{i}.png", "wb"))

            i += 1

        matches = re.findall(r"((?<=\n"+figureStdAnnot+")|(?<=^"+figureStdAnnot+"))(.+(\n.*)?(\n[a-z (].*)*)(?=\n)",page.get_text())

        for m in matches:
            if isinstance(m, str):
                m = m.replace('\n', ' ')
                n = re.findall(r"\d+",m)[0]
                try:
                    c = re.findall(r"(?<=\. ).+",m)[0]
                except:
                    continue
                if len(c.strip())==0:
                    continue
                captions[n] = c
            else:
                for el in m:
                    el = el.replace('\n', ' ')
                    n = re.findall(r"\d+",el)
                    if len(n) == 0:
                        continue
                    n = n[0]
                    try:
                        c = re.findall(r"(?<=\. ).+",el)[0]
                    except:
                        continue
                    captions[n] = c

    return captions
