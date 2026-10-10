"""Voice expense-entry prototype.

Audio capture and parsing are separate from persistence. Speech-to-text and saving
remain disabled until a supported recognition provider and storage flow are configured.
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
        "భోజనం", "తిండి", "కూరగాయలు", "खाना", "खाने", "भोजन", "किराना",
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
    normalized = text.replace(",", "")
    amount_match = re.search(
        r"(?<![\w.])(?:₹\s*)?(\d+(?:\.\d{1,2})?)(?![\w.])",
        normalized,
        flags=re.IGNORECASE,
    )
    amount = None
    if amount_match:
        try:
            amount = float(amount_match.group(1))
            if amount <= 0:
                amount = None
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
        "This prototype previews recognition results; it does not save expenses."
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
        help="Enter a transcript here to test amount and category extraction.",
        key="voice_expense_transcript",
    )

    if st.button("Preview expense", type="primary"):
        if not transcript.strip():
            st.warning("Enter a transcript to preview. Audio transcription is not connected yet.")
            return
        st.session_state["voice_expense_draft"] = parse_expense_text(transcript).__dict__
        st.session_state.pop("voice_expense_correction", None)

    draft_data = st.session_state.get("voice_expense_draft")
    if not draft_data:
        return

    amount = draft_data["amount"]
    category = draft_data["category"]
    correction = st.session_state.get("voice_expense_correction")
    if correction and correction.get("transcript") == draft_data["transcript"]:
        if correction.get("category"):
            category = correction["category"]
        if correction.get("amount") is not None:
            amount = correction["amount"]

    st.subheader("Detected expense")
    left, right = st.columns(2)
    left.metric("Amount", f"₹{amount:,.2f}" if amount is not None else "Not detected")
    right.metric("Category", category or "Choose category")

    if amount is None and category is None:
        st.warning("The amount and category are unclear.")
        choice = st.radio(
            "Choose what to correct",
            ["Enter amount", "Choose category"],
            horizontal=True,
            key="voice_expense_missing_both",
        )
        if choice == "Enter amount":
            manual_amount = st.number_input(
                "Amount (₹)", min_value=0.01, step=1.0, key="voice_expense_manual_amount"
            )
            if st.button("Apply amount", key="voice_expense_apply_amount"):
                st.session_state["voice_expense_correction"] = {
                    "transcript": draft_data["transcript"], "amount": manual_amount
                }
                st.rerun()
        else:
            selected_category = st.radio(
                "Category",
                ["Petrol / Fuel", "Food / Groceries"],
                horizontal=True,
                key="voice_expense_category_both",
            )
            if st.button("Apply category", key="voice_expense_apply_category_both"):
                st.session_state["voice_expense_correction"] = {
                    "transcript": draft_data["transcript"], "category": selected_category
                }
                st.rerun()
    elif category is None:
        st.warning("Choose the closest category, or edit the transcript and preview again.")
        choice = st.radio(
            "Quick options",
            ["Petrol / Fuel", "Food / Groceries"],
            horizontal=True,
            key="voice_expense_quick_choice",
        )
        if st.button("Apply selected category", key="voice_expense_use_choice"):
            st.session_state["voice_expense_correction"] = {
                "transcript": draft_data["transcript"], "category": choice
            }
            st.rerun()
    elif amount is None:
        st.warning("The amount is unclear.")
        choice = st.radio(
            "Quick options",
            ["Enter amount", "Edit transcript and try again"],
            horizontal=True,
            key="voice_expense_amount_choice",
        )
        if choice == "Enter amount":
            manual_amount = st.number_input(
                "Amount (₹)", min_value=0.01, step=1.0, key="voice_expense_manual_amount_only"
            )
            if st.button("Apply amount", key="voice_expense_apply_amount_only"):
                st.session_state["voice_expense_correction"] = {
                    "transcript": draft_data["transcript"], "amount": manual_amount
                }
                st.rerun()
        else:
            st.caption("Edit the transcript above and select Preview expense again.")

    if amount is not None and category is not None:
        st.success(f"Draft ready: ₹{amount:,.2f} · {category}")
        st.caption("This is a preview only. No expense has been written to CSV or SQLite.")

    st.caption(f"Language mode: {language}")
    st.caption("Neither quick option fits? Edit the transcript above and preview again.")
