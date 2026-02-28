from typing import Tuple, List


class LLMLayer:
    """LLM interaction facade with supply-chain guardrails and retrieval snippets."""

    ALLOWED_KEYWORDS = {
        "supply",
        "inventory",
        "demand",
        "lead time",
        "supplier",
        "logistics",
        "stock",
        "warehouse",
        "forecast",
        "procurement",
    }

    KNOWLEDGE = {
        "safety stock": "Safety stock buffers uncertainty in demand and lead-time variability.",
        "lead time": "Lead time is the latency from ordering to receipt; lower variance improves service level.",
        "reliability": "Supplier reliability score can be used as a risk multiplier in replenishment policies.",
        "forecast": "Simple demand forecasts blend historical demand, promotions, and seasonality signals.",
    }

    def is_in_scope(self, question: str) -> bool:
        q = question.lower()
        return any(keyword in q for keyword in self.ALLOWED_KEYWORDS)

    def answer(self, question: str) -> Tuple[str, List[str]]:
        if not self.is_in_scope(question):
            return (
                "I can only answer supply-chain-related questions. Please ask about demand, inventory, suppliers, logistics, or forecasting.",
                [],
            )

        q = question.lower()
        refs = []
        snippets = []
        for term, insight in self.KNOWLEDGE.items():
            if term in q:
                snippets.append(insight)
                refs.append(f"knowledge:{term}")

        if not snippets:
            snippets.append(
                "For this supply-chain question, start from demand variability, supplier reliability, and lead-time risk to decide replenishment actions."
            )
            refs.append("knowledge:general-principles")

        return " ".join(snippets), refs
