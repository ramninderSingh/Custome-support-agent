import re
from pathlib import Path

from transformers import AutoTokenizer


class MarkdownChunker:

    def __init__(
        self,
        chunk_size: int = 400,
        chunk_overlap: int = 60,
        tokenizer_name: str = "BAAI/bge-small-en-v1.5",
    ):
        """
        Args:
            chunk_size:
                Maximum target size of a chunk in tokens.

            chunk_overlap:
                Number of tokens worth of previous content
                carried into the next chunk.

            tokenizer_name:
                Tokenizer used to measure chunk size.
        """

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        self.tokenizer = AutoTokenizer.from_pretrained(
            tokenizer_name
        )

    def chunk_document(
        self,
        text: str,
        source: str,
    ) -> list[dict]:

        sections = self._split_sections(text)

        all_chunks = []

        for section in sections:

            chunks = self._chunk_section(
                section_text=section["text"],
                section_title=section["title"],
            )

            for chunk_index, chunk in enumerate(chunks):

                # Add context to the chunk itself.
                contextualized_text = (
                    f"Document: {source}\n"
                    f"Section: {section['title']}\n\n"
                    f"{chunk}"
                )

                all_chunks.append(
                    {
                        "text": contextualized_text,
                        "metadata": {
                            "source": source,
                            "section": section["title"],
                            "chunk_id": chunk_index,
                            "document_type": "policy",
                        },
                    }
                )

        return all_chunks

    # ---------------------------------------------------------
    # STEP 1: Markdown section detection
    # ---------------------------------------------------------

    def _split_sections(
        self,
        text: str,
    ) -> list[dict]:

        lines = text.splitlines()

        sections = []

        current_title = "Introduction"
        current_content = []

        for line in lines:

            # Match #, ## or ###
            if re.match(r"^#{1,3}\s+", line):

                if current_content:

                    sections.append(
                        {
                            "title": current_title,
                            "text": "\n".join(
                                current_content
                            ).strip(),
                        }
                    )

                current_title = re.sub(
                    r"^#{1,3}\s+",
                    "",
                    line,
                ).strip()

                current_content = []

            else:
                current_content.append(line)

        if current_content:

            sections.append(
                {
                    "title": current_title,
                    "text": "\n".join(
                        current_content
                    ).strip(),
                }
            )

        return [
            section
            for section in sections
            if section["text"]
        ]

    # ---------------------------------------------------------
    # STEP 2: Paragraph detection
    # ---------------------------------------------------------

    def _split_paragraphs(
        self,
        text: str,
    ) -> list[str]:

        paragraphs = re.split(
            r"\n\s*\n",
            text,
        )

        return [
            paragraph.strip()
            for paragraph in paragraphs
            if paragraph.strip()
        ]

    # ---------------------------------------------------------
    # STEP 3: Sentence detection
    # ---------------------------------------------------------

    def _split_sentences(
        self,
        text: str,
    ) -> list[str]:

        # Basic sentence splitter.
        # We can replace this with spaCy later if needed.
        sentences = re.split(
            r"(?<=[.!?])\s+",
            text,
        )

        return [
            sentence.strip()
            for sentence in sentences
            if sentence.strip()
        ]

    # ---------------------------------------------------------
    # STEP 4: Build token-sized chunks
    # ---------------------------------------------------------

    def _chunk_section(
        self,
        section_text: str,
        section_title: str,
    ) -> list[str]:

        paragraphs = self._split_paragraphs(
            section_text
        )

        chunks = []
        current_sentences = []
        current_tokens = 0

        for paragraph in paragraphs:

            sentences = self._split_sentences(
                paragraph
            )

            for sentence in sentences:

                sentence_tokens = len(
                    self.tokenizer.encode(
                        sentence,
                        add_special_tokens=False,
                    )
                )

                # Handle a single sentence larger
                # than the chunk size.
                if sentence_tokens > self.chunk_size:

                    if current_sentences:
                        chunks.append(
                            " ".join(
                                current_sentences
                            )
                        )

                        current_sentences = []
                        current_tokens = 0

                    chunks.extend(
                        self._split_large_sentence(
                            sentence
                        )
                    )

                    continue

                # Would this sentence exceed the limit?
                if (
                    current_tokens + sentence_tokens
                    > self.chunk_size
                ):

                    chunks.append(
                        " ".join(
                            current_sentences
                        )
                    )

                    # Keep some overlap.
                    overlap_sentences = (
                        self._get_overlap_sentences(
                            current_sentences
                        )
                    )

                    current_sentences = (
                        overlap_sentences
                    )

                    current_tokens = sum(
                        len(
                            self.tokenizer.encode(
                                sentence,
                                add_special_tokens=False,
                            )
                        )
                        for sentence
                        in current_sentences
                    )

                current_sentences.append(
                    sentence
                )

                current_tokens += sentence_tokens

        if current_sentences:

            chunks.append(
                " ".join(current_sentences)
            )

        return chunks

    # ---------------------------------------------------------
    # STEP 5: Overlap
    # ---------------------------------------------------------

    def _get_overlap_sentences(
        self,
        sentences: list[str],
    ) -> list[str]:

        overlap = []
        token_count = 0

        for sentence in reversed(sentences):

            sentence_tokens = len(
                self.tokenizer.encode(
                    sentence,
                    add_special_tokens=False,
                )
            )

            if (
                token_count + sentence_tokens
                > self.chunk_overlap
            ):
                break

            overlap.insert(
                0,
                sentence,
            )

            token_count += sentence_tokens

        return overlap

    # ---------------------------------------------------------
    # STEP 6: Very large sentence
    # ---------------------------------------------------------

    def _split_large_sentence(
        self,
        sentence: str,
    ) -> list[str]:

        tokens = self.tokenizer.encode(
            sentence,
            add_special_tokens=False,
        )

        chunks = []

        start = 0

        while start < len(tokens):

            end = start + self.chunk_size

            chunk_tokens = tokens[start:end]

            chunk = self.tokenizer.decode(
                chunk_tokens,
                skip_special_tokens=True,
            )

            chunks.append(chunk)

            start = end - self.chunk_overlap

        return chunks