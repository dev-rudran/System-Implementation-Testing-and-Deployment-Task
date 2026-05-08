import re
from typing import Dict, Union


class TextAnalyzerTool:
    def analyze(self, text: str) -> Dict[str, Union[int, float, str, list]]:
        if not text or not text.strip():
            return {"error": "No text provided for analysis."}

        words = text.split()
        word_count = len(words)
        char_count = len(text)
        char_count_no_spaces = len(text.replace(" ", ""))
        sentences = re.split(r"[.!?]+", text)
        sentences = [s.strip() for s in sentences if s.strip()]
        sentence_count = len(sentences)

        avg_word_length = round(char_count_no_spaces / word_count, 2) if word_count > 0 else 0
        avg_sentence_length = round(word_count / sentence_count, 2) if sentence_count > 0 else 0

        unique_words = set(w.lower().strip(".,!?;:\"'()[]{}") for w in words)
        unique_word_count = len(unique_words)

        word_frequency = {}
        for w in words:
            w_clean = w.lower().strip(".,!?;:\"'()[]{}")
            if w_clean:
                word_frequency[w_clean] = word_frequency.get(w_clean, 0) + 1

        sorted_words = sorted(word_frequency.items(), key=lambda x: x[1], reverse=True)
        top_words = sorted_words[:5]

        return {
            "word_count": word_count,
            "character_count": char_count,
            "character_count_no_spaces": char_count_no_spaces,
            "sentence_count": sentence_count,
            "average_word_length": avg_word_length,
            "average_sentence_length": avg_sentence_length,
            "unique_word_count": unique_word_count,
            "top_words": top_words,
        }
