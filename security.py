"""
Tanglish Transliteration Engine
--------------------------------
Converts Tamil script text into natural, creator-friendly "Tanglish"
(Tamil words spelled using English/Roman letters), the way Tamil YouTubers
and Instagram creators actually write captions — not strict academic
transliteration (IAST/ITRANS), but casual readable Romanization.

Strategy:
1. Dictionary-first pass: common conversational words/phrases are mapped
   directly to the way creators actually spell them (e.g. "வணக்கம்" -> "Vanakkam",
   not "vaNakkam").
2. Algorithmic fallback: any word not in the dictionary is transliterated
   character-by-character using a Tamil -> Roman phonetic map tuned for
   "creator spelling" conventions (soft consonants, no diacritics).
3. Post-processing: capitalization, punctuation preservation, sentence casing.
"""
import re

# ---------------------------------------------------------------------------
# 1. High-frequency creator vocabulary — curated for natural Tanglish spelling
#    (this dictionary should keep growing; seed set covers common phrases)
# ---------------------------------------------------------------------------
COMMON_WORDS = {
    "வணக்கம்": "Vanakkam",
    "நண்பர்களே": "Nanbargale",
    "நண்பர்கள்": "Nanbargal",
    "எப்படி": "Epdi",
    "இருக்கீங்க": "Irukeenga",
    "இருக்கீங்களா": "Irukeengala",
    "இன்று": "Inniku",
    "ஒரு": "Oru",
    "புதிய": "Pudhiya",
    "வீடியோ": "Video",
    "நன்றி": "Nandri",
    "சூப்பர்": "Super",
    "செய்வோம்": "Seivom",
    "பார்க்கலாம்": "Paakalam",
    "சரியா": "Sariya",
    "சரி": "Sari",
    "என்ன": "Enna",
    "எனக்கு": "Enakku",
    "உங்களுக்கு": "Ungalukku",
    "பண்ணுங்க": "Pannunga",
    "வாங்க": "Vaanga",
    "போங்க": "Pongo",
    "இது": "Idhu",
    "அது": "Adhu",
    "நல்லா": "Nalla",
    "ரொம்ப": "Romba",
    "மிகவும்": "Migavum",
    "நிறைய": "Niraya",
    "கொஞ்சம்": "Konjam",
    "இப்போ": "Ippo",
    "இப்பொழுது": "Ipozhudhu",
    "அப்புறம்": "Apparam",
    "சாப்பிடலாம்": "Saapidalam",
    "போகலாம்": "Pogalam",
    "வேணும்": "Venum",
    "வேண்டாம்": "Venaam",
    "இல்ல": "Illa",
    "இல்லை": "Illai",
    "ஆமா": "Aama",
    "ஆமாம்": "Aamam",
    "சொல்லுங்க": "Sollunga",
    "கேளுங்க": "Kelunga",
    "பாருங்க": "Paarunga",
    "லைக்": "Like",
    "சப்ஸ்கிரைப்": "Subscribe",
    "காமெண்ட்": "Comment",
    "ஷேர்": "Share",
    "சேனல்": "Channel",
}

# ---------------------------------------------------------------------------
# 2. Tamil Unicode character -> Roman phonetic map (creator-style, no diacritics)
#    Ordered longest-match-first for compound vowel signs / consonant clusters.
# ---------------------------------------------------------------------------
VOWELS = {
    "அ": "a", "ஆ": "aa", "இ": "i", "ஈ": "ee", "உ": "u", "ஊ": "oo",
    "எ": "e", "ஏ": "ae", "ஐ": "ai", "ஒ": "o", "ஓ": "oh", "ஔ": "au",
}

VOWEL_SIGNS = {  # attached to consonants
    "ா": "aa", "ி": "i", "ீ": "ee", "ு": "u", "ூ": "oo",
    "ெ": "e", "ே": "ae", "ை": "ai", "ொ": "o", "ோ": "oh", "ௌ": "au",
    "்": "",  # pulli (virama) — suppresses inherent vowel
}

CONSONANTS = {
    "க": "k", "ங": "ng", "ச": "ch", "ஞ": "nj", "ட": "t", "ண": "n",
    "த": "th", "ந": "n", "ப": "p", "ம": "m", "ய": "y", "ர": "r",
    "ல": "l", "வ": "v", "ழ": "zh", "ள": "l", "ற": "r", "ன": "n",
    "ஜ": "j", "ஷ": "sh", "ஸ": "s", "ஹ": "h", "க்ஷ": "ksh",
}

GRANTHA_AND_MISC = {
    "ஃ": "k",  # aytham, approximated
}


def _transliterate_word(word: str) -> str:
    """Character-by-character phonetic fallback for words not in dictionary."""
    result = []
    i = 0
    n = len(word)
    while i < n:
        ch = word[i]

        # Consonant + vowel sign combo (most common pattern, e.g. கா, கி, கு)
        if ch in CONSONANTS:
            base = CONSONANTS[ch]
            if i + 1 < n and word[i + 1] in VOWEL_SIGNS:
                sign = VOWEL_SIGNS[word[i + 1]]
                result.append(base + sign if sign != "" else base)
                i += 2
                continue
            else:
                # bare consonant carries inherent "a" sound
                result.append(base + "a")
                i += 1
                continue

        if ch in VOWELS:
            result.append(VOWELS[ch])
            i += 1
            continue

        if ch in GRANTHA_AND_MISC:
            result.append(GRANTHA_AND_MISC[ch])
            i += 1
            continue

        # Non-Tamil character (English, digits, punctuation) — keep as-is
        result.append(ch)
        i += 1

    return "".join(result)


def _capitalize_natural(word: str) -> str:
    """Capitalize like a creator typing captions, not formal title-case rules."""
    if not word:
        return word
    return word[0].upper() + word[1:]


def transliterate_text(tamil_text: str) -> str:
    """
    Convert a full Tamil sentence/segment into natural Tanglish,
    preserving punctuation, spacing, and word order.
    """
    if not tamil_text:
        return ""

    # Tokenize while keeping punctuation as separate tokens
    tokens = re.findall(r"[\u0B80-\u0BFF]+|[a-zA-Z0-9]+|[^\s\w]|\s+", tamil_text)

    output = []
    for tok in tokens:
        if tok.isspace():
            output.append(tok)
            continue

        if re.match(r"[\u0B80-\u0BFF]+", tok):
            if tok in COMMON_WORDS:
                output.append(COMMON_WORDS[tok])
            else:
                output.append(_capitalize_natural(_transliterate_word(tok)))
        else:
            # English words / numbers / punctuation pass through unchanged
            output.append(tok)

    tanglish = "".join(output)
    tanglish = re.sub(r"\s+", " ", tanglish).strip()
    return tanglish


def transliterate_segments(segments: list[dict]) -> list[dict]:
    """
    Apply Tanglish conversion to a list of Whisper segments while
    preserving start/end timestamps.
    """
    converted = []
    for seg in segments:
        converted.append({
            **seg,
            "tamil_text": seg["text"],
            "tanglish_text": transliterate_text(seg["text"]),
        })
    return converted
