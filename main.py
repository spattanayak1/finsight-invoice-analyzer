from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
import pdfplumber
import io

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)) -> Dict[str, float]:
    contents = await file.read()
    sum_total = 0.0

    with pdfplumber.open(io.BytesIO(contents)) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if not table:
                continue
            headers = [h.strip().lower() for h in table[0]]
            if 'product' in headers and 'total' in headers:
                product_idx = headers.index('product')
                total_idx = headers.index('total')

                for row in table[1:]:
                    product = str(row[product_idx]).strip().lower()
                    total_val = str(row[total_idx]).strip()
                    if product == "doodad":
                        try:
                            sum_total += float(total_val)
                        except ValueError:
                            pass

    return {"sum": sum_total}
