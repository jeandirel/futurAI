"""
Extract text from all PDFs in data/raw and write plain text files to data/processed.
Skips non-PDF files (e.g., pptx).
Optimized with multiprocessing for faster execution.
"""

import shutil
import concurrent.futures
import multiprocessing
from pathlib import Path
import time
import PyPDF2

RAW_DIR = Path("data/raw")
OUT_DIR = Path("data/processed")


def extract_single_pdf(pdf_path: Path) -> str:
    """
    Worker function to extract text from a single PDF.
    Returns a status string.
    """
    out_path = OUT_DIR / (pdf_path.stem + ".txt")
    
    # Skip if already exists (optional, but good for incremental runs)
    # if out_path.exists():
    #     return f"[SKIP] {pdf_path.name}: already exists"

    try:
        reader = PyPDF2.PdfReader(str(pdf_path))
        texts = []
        for i, page in enumerate(reader.pages):
            try:
                text = page.extract_text() or ""
                texts.append(text.strip())
            except Exception:
                # Log warning but continue with other pages
                pass
        
        full_text = "\n\n".join(texts)
        out_path.write_text(full_text, encoding="utf-8")
        return f"[OK] {pdf_path.name} -> {out_path.name} ({len(reader.pages)} pages)"
    except Exception as e:
        return f"[ERR] {pdf_path.name}: {str(e)}"


def main() -> None:
    start_time = time.perf_counter()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    
    pdf_files = list(RAW_DIR.glob("*.pdf"))
    if not pdf_files:
        print("No PDF files found in data/raw")
        return

    # Use all available cores
    max_workers = multiprocessing.cpu_count()
    print(f"Starting extraction of {len(pdf_files)} PDFs using {max_workers} workers...")

    processed_count = 0
    errors_count = 0

    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        future_to_pdf = {executor.submit(extract_single_pdf, pdf): pdf for pdf in pdf_files}
        for future in concurrent.futures.as_completed(future_to_pdf):
            result = future.result()
            print(result)
            if "[ERR]" in result:
                errors_count += 1
            else:
                processed_count += 1

    # Copy manifest for traceability
    manifest = RAW_DIR / "manifest.csv"
    if manifest.exists():
        shutil.copy(manifest, OUT_DIR / "manifest.csv")

    # Report skipped files (non-PDF)
    skipped = [p.name for p in RAW_DIR.iterdir() if p.is_file() and p.suffix.lower() != ".pdf"]
    if skipped:
        print(f"[INFO] Skipped non-PDF files: {', '.join(skipped)}")

    elapsed = time.perf_counter() - start_time
    print(f"\nDone in {elapsed:.2f}s. Processed: {processed_count}, Errors: {errors_count}")


if __name__ == "__main__":
    main()

