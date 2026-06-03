import re


class RAGEngine:
    def __init__(self):
        self.document_text = ""

    def add_documents(self, docs):
        self.document_text = " ".join(docs)

    # ---------- ENTITY EXTRACTION ----------
    def extract_entities(self, text):
        sections = re.findall(r"(Section\s*\d+[A-Za-z]*)", text, re.IGNORECASE)
        dates = re.findall(r"\d{1,2}\s+[A-Za-z]+\s+\d{4}", text)
        names = re.findall(r"(Mr\.?\s+[A-Z][a-z]+\s+[A-Z][a-z]+)", text)

        return {
            "sections": list(set(sections)),
            "dates": list(set(dates)),
            "names": list(set(names))
        }

    # ---------- RISK INDICATOR ----------
    def detect_risk(self, text):
        text_lower = text.lower()

        if any(word in text_lower for word in ["court", "legal notice", "summon", "police", "offence"]):
            return "🔴 HIGH RISK"

        elif any(word in text_lower for word in ["warning", "notice", "complaint"]):
            return "🟡 MEDIUM RISK"

        else:
            return "🟢 LOW RISK"

    # ---------- ACTIONABLE GUIDANCE ----------
    def generate_actions(self, entities):
        actions = []

        if entities["dates"]:
            actions.append(f"Attend the legal proceeding on {entities['dates'][0]}")

        if entities["sections"]:
            actions.append(f"Understand implications of {entities['sections'][0]}")

        actions.append("Carry all relevant legal documents")
        actions.append("Consult a qualified legal advisor")

        return actions

    # ---------- FORMAT ----------
    def format_top_matches(self, entities):
        matches = []

        if entities["sections"]:
            matches.append("⚖ Sections: " + ", ".join(entities["sections"]))

        if entities["dates"]:
            matches.append("📅 Dates: " + ", ".join(entities["dates"]))

        if entities["names"]:
            matches.append("👤 Persons: " + ", ".join(entities["names"]))

        while len(matches) < 3:
            matches.append("Additional information not available")

        return matches[:3]

    # ---------- MAIN ----------
    def search(self, query):
        if not self.document_text:
            return {
                "question": query,
                "answer": "No document uploaded yet.",
                "top_3_sections": ["No data"] * 3,
                "risk": "Unknown",
                "actions": [],
                "confidence": "No data"
            }

        entities = self.extract_entities(self.document_text)

        # LLM call
        try:
            import llm_engine
            answer = llm_engine.generate_llm_response(self.document_text, query)
        except:
            answer = "This document contains legal information."

        top_matches = self.format_top_matches(entities)
        risk = self.detect_risk(self.document_text)
        actions = self.generate_actions(entities)

        return {
            "question": query,
            "answer": answer,
            "top_3_sections": top_matches,
            "risk": risk,
            "actions": actions,
            "confidence": "AI + LLM powered response"
        }