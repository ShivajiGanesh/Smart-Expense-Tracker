"""Voice expense-entry prototype.

This module deliberately keeps audio capture and parsing separate from persistence.
Speech-to-text and saving are not enabled until a supported recognition provider is configured.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional

import streamlit as st


CATEGORY_ALIASES = {
    "Petrol / Fuel": (
        "petrol", "fuel", "diesel", "పెట్రోల్", "పెట్రోలు", "ఇంధనం",
        "पेट्रोल", "डीजल", "ईंधन",
    ),
    "Food / Groceries": (
        "food", "lunch", "dinner", "breakfast", "groceries", "grocery",
        "భోజనం", "తిండి", "కూరగాయలు", "खाना", "भोजन", "किराना",
    ),
    "Transport": (
        "bus", "train", "metro", "auto", "cab", "transport",
        "బస్సు", "రైలు", "ఆటో", "यात्रा", "बस", "ऑटो",
    ),
    "Bills": (
        "bill", "electricity", "internet", "mobile recharge",
        "బిల్లు", "కరెంట్", "విద్యుత్", "बिल", "बिजली", "रिचार्ज",
    ),
    "Shopping": (
        "shopping", "clothes", "shirt", "shoes",
        "షాపింగ్", "బట్టలు", "खरीदारी", "कपड़े",
    ),
}


@dataclass
class ExpenseDraft:
    amount: Optional[float]
    category: Optional[str]
    transcript: str


def parse_expense_text(text: str) -> ExpenseDraft:
    """Extract a likely amount and category from a natural-language transcript."""
    amount_match = re.search(
        r"(?<![\w.])(?:₹\s*)?(\d+(?:,\d{3})*(?:\.\d{1,2})?)(?![\w.])",
        text.replace("rupees", " ",).replace("रुपये", " "),
        flags=re.IGNORECASE,
    )
    amount = None
    if amount_match:
        try:
            amount = float(amount_match.group(1).replace(",", ""))
        except ValueError:
            amount = None

    lowered = text.casefold()
    category = None
    for canonical, aliases in CATEGORY_ALIASES.items():
        if any(alias.casefold() in lowered for alias in aliases):
            category = canonical
            break

    return ExpenseDraft(amount=amount, category=category, transcript=text.strip())


def render_voice_entry() -> None:
    st.header("Voice Expense Entry")
    st.caption(
        "Speak naturally in Telugu, Hindi, English, or a mix. "
        "The current prototype previews recognition results; it does not save expenses."
    )

    language = st.selectbox(
        "Primary speech language",
        [
            "Auto-detect / mixed Telugu + English + Hindi",
            "Telugu",
            "Hindi",
            "English",
        ],
        index=0,
        help="Mixed-language recognition requires a compatible speech-to-text provider.",
    )

    audio = st.audio_input("Record an expense", key="voice_expense_audio")
    if audio is not None:
        st.audio(audio)
        st.info(
            "Audio captured. Speech-to-text is not connected yet, so no transcript "
            "has been inferred from this recording."
        )

    transcript = st.text_area(
        "Transcript preview",
        placeholder=(
            'Example: "Ninna petrol ki 200 rupees pettanu" or '
            '"आज खाने पर 250 रुपये खर्च किए"'
        ),
        help="For this UI prototype, enter the transcript here to test amount/category extraction.",
        key="voice_expense_transcript",
    )

    if st.button("Preview expense", type="primary"):
        if not transcript.strip():
            st.warning("Record audio and connect speech recognition, or enter a transcript to preview.")
            return

        draft = parse_expense_text(transcript)
        st.subheader("Detected expense")
        left, right = st.columns(2)
        left.metric("Amount", f"₹{draft.amount:,.2f}" if draft.amount is not None else "Not detected")
        right.metric("Category", draft.category or "Choose category")

        if draft.amount is None or draft.category is None:
            st.warning("Some details are unclear. Choose a suggestion or enter the transcript again.")
            options = ["Fuel", "Food / Groceries"] if draft.category is None else ["Amount is correct", "Re-enter amount"]
            choice = st.radio("Quick options", options, horizontal=True, key="voice_expense_quick_choice")
            if st.button("Use selected option", key="voice_expense_use_choice"):
                st.session_state["voice_expense_selected_choice"] = choice
                st.info(f"Selected: {choice}. Saving is not enabled in this prototype.")
            st.caption("Neither option fits? Edit the transcript above and preview again.")

        st.caption(f"Language mode: {language}")
        st.caption("No expense has been written to CSV or SQLite.")
