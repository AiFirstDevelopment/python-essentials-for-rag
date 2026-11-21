def chunk_text(text: str, size: int = 120, overlap: int = 20) -> list[str]:
    """Split text into chunks of `size` words, each sharing `overlap` words with the one before."""
    if overlap >= size:
        raise ValueError("overlap must be smaller than size")
    words = text.split()
    step = size - overlap
    return [" ".join(words[i:i + size]) for i in range(0, max(len(words) - overlap, 1), step)]
