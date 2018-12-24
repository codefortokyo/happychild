import re
import string
import unicodedata

import mojimoji

SYMBOL_TABLE = str.maketrans("", "", re.sub(r'[-ー&＆/+]', '', string.punctuation + "「」、。・"))


class Normalizer(object):
    def run(self, text: str):
        """
        Normalize a text before extract some spot words

        Parameters
        ----------
        text ``str``, required

        Returns
        -------
        A normalized text
        """
        cleaned_text = self._delete_noisy_chars(text)
        normalized_text = self._normalize(cleaned_text)
        return normalized_text

    @classmethod
    def _delete_noisy_chars(cls, text: str) -> str:
        return text.translate(SYMBOL_TABLE).replace('\n', '').strip()

    @classmethod
    def _normalize(cls, text: str) -> str:
        """
        Normalize a text

        Parameters
        ----------
        text ``str``, required

        Returns
        -------
        A normalized text
        """
        text = unicodedata.normalize("NFKC", text)
        text = text.lower()
        text = text.replace(' ', '').strip()
        return mojimoji.han_to_zen(text, ascii=False)


normalizer = Normalizer()
