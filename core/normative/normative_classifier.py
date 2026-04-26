import re
import unicodedata
from collections import defaultdict


class NormativeClassifier:
    """
    MAGICBANK SUPREME+ — Advanced Normative Classification Engine

    PURPOSE:
    Institutional-grade classification of normative events with:

    - Primary domain
    - Secondary domains
    - Jurisdiction
    - Severity
    - Subdomains
    - Confidence scoring
    - Weighted classification
    - Unicode normalization
    - Multi-impact analysis

    OUTPUT:
    Academic, curricular, and governance-ready classification structure.
    """

    # =========================================================
    # DOMAIN RULES (WEIGHTED)
    # =========================================================
    DOMAIN_RULES = {
        "tributario": {
            "impuesto": 10,
            "tributario": 10,
            "retencion": 9,
            "declaracion": 9,
            "iva": 9,
            "tax": 9,
            "filing": 8,
            "withholding": 8,
            "irs": 8,
            "dian": 8,
            "cra": 8,
            "facturacion": 8,
            "sales tax": 8,
            "ein": 7
        },
        "contable": {
            "ifrs": 10,
            "niif": 10,
            "us gaap": 10,
            "gaap": 9,
            "financial reporting": 9,
            "disclosure": 8,
            "recognition": 8,
            "measurement": 8,
            "accounting standard": 9,
            "financial statement": 8
        },
        "auditoria": {
            "audit": 10,
            "auditoria": 10,
            "assurance": 9,
            "control interno": 8,
            "internal control": 8,
            "risk assessment": 8,
            "fraud": 8,
            "audit evidence": 8
        },
        "compliance": {
            "compliance": 10,
            "mandatory": 9,
            "obligatorio": 9,
            "obligatoria": 9,
            "sanction": 9,
            "penalty": 9,
            "regulation": 8,
            "regulatory": 8,
            "filing requirement": 8
        },
        "financiero": {
            "financial": 8,
            "liquidity": 8,
            "solvency": 8,
            "cash flow": 8,
            "capital": 7,
            "budget": 7,
            "financing": 7,
            "investment": 7
        }
    }

    # =========================================================
    # JURISDICTION RULES
    # =========================================================
    JURISDICTION_RULES = {
        "CO": {
            "dian": 10,
            "colombia": 10,
            "nit": 8,
            "retencion": 8,
            "facturacion electronica": 9,
            "rut": 8
        },
        "US": {
            "irs": 10,
            "usa": 10,
            "united states": 10,
            "federal tax": 9,
            "ein": 9,
            "payroll tax": 9,
            "sec": 8
        },
        "CA": {
            "cra": 10,
            "canada": 10,
            "gst": 9,
            "hst": 9
        },
        "INTERNATIONAL": {
            "ifrs": 10,
            "iasb": 9,
            "oecd": 9,
            "global tax": 8,
            "international": 8
        }
    }

    # =========================================================
    # SEVERITY RULES
    # =========================================================
    SEVERITY_RULES = {
        "critical": {
            "reforma": 10,
            "resolucion": 10,
            "decreto": 10,
            "ley": 10,
            "mandatory": 9,
            "obligatorio": 9,
            "sanction": 9,
            "penalty": 9
        },
        "important": {
            "impuesto": 8,
            "tributario": 8,
            "tax": 8,
            "filing": 8,
            "compliance": 8,
            "reporting": 7,
            "withholding": 7
        },
        "informational": {
            "calendario": 5,
            "notice": 5,
            "guidance": 5,
            "recordatorio": 5,
            "boletin": 5
        }
    }

    # =========================================================
    # SUBDOMAINS
    # =========================================================
    SUBDOMAIN_RULES = {
        "facturacion_electronica": [
            "facturacion electronica",
            "electronic invoicing",
            "e invoicing"
        ],
        "iva_vat": [
            "iva",
            "vat",
            "sales tax"
        ],
        "retencion_withholding": [
            "retencion",
            "withholding"
        ],
        "payroll_tax": [
            "payroll",
            "social security",
            "medicare"
        ],
        "financial_reporting": [
            "financial statement",
            "reporting",
            "disclosure"
        ],
        "audit_assurance": [
            "audit",
            "assurance",
            "fraud",
            "internal control"
        ],
        "us_gaap": [
            "us gaap",
            "gaap"
        ],
        "ifrs_niif": [
            "ifrs",
            "niif"
        ]
    }

    # =========================================================
    # NORMALIZATION
    # =========================================================
    def normalize_text(self, text):
        if not text:
            return ""

        text = str(text).lower().strip()

        text = unicodedata.normalize(
            "NFKD",
            text
        ).encode(
            "ascii",
            "ignore"
        ).decode(
            "utf-8"
        )

        text = re.sub(r"[^a-z0-9\s\-]", " ", text)

        text = re.sub(r"\s+", " ", text)

        return text.strip()

    # =========================================================
    # KEYWORD SCORE
    # =========================================================
    def score_keywords(self, text, weighted_keywords):
        score = 0

        for keyword, weight in weighted_keywords.items():
            normalized_keyword = self.normalize_text(keyword)

            if re.search(
                rf"\b{re.escape(normalized_keyword)}\b",
                text
            ):
                score += weight

        return score

    # =========================================================
    # DOMAIN CLASSIFICATION
    # =========================================================
    def classify_domains(self, text):
        text = self.normalize_text(text)

        scores = {}

        for domain, keywords in self.DOMAIN_RULES.items():
            score = self.score_keywords(
                text,
                keywords
            )

            if score > 0:
                scores[domain] = score

        if not scores:
            return {
                "primary_domain": "general_normative",
                "secondary_domains": [],
                "domain_scores": {}
            }

        sorted_domains = sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        primary = sorted_domains[0][0]

        secondary = [
            domain for domain, score
            in sorted_domains[1:]
            if score >= 0.5 * sorted_domains[0][1]
        ]

        return {
            "primary_domain": primary,
            "secondary_domains": secondary,
            "domain_scores": scores
        }

    # =========================================================
    # JURISDICTION
    # =========================================================
    def classify_jurisdiction(self, text):
        text = self.normalize_text(text)

        scores = {}

        for jurisdiction, keywords in self.JURISDICTION_RULES.items():
            score = self.score_keywords(
                text,
                keywords
            )

            if score > 0:
                scores[jurisdiction] = score

        if not scores:
            return {
                "jurisdiction": "GLOBAL",
                "jurisdiction_score": 0
            }

        best = max(
            scores.items(),
            key=lambda x: x[1]
        )

        return {
            "jurisdiction": best[0],
            "jurisdiction_score": best[1]
        }

    # =========================================================
    # SEVERITY
    # =========================================================
    def classify_severity(self, text):
        text = self.normalize_text(text)

        scores = {}

        for severity, keywords in self.SEVERITY_RULES.items():
            score = self.score_keywords(
                text,
                keywords
            )

            if score > 0:
                scores[severity] = score

        if not scores:
            return {
                "severity": "informational",
                "severity_score": 0
            }

        best = max(
            scores.items(),
            key=lambda x: x[1]
        )

        return {
            "severity": best[0],
            "severity_score": best[1]
        }

    # =========================================================
    # SUBDOMAINS
    # =========================================================
    def classify_subdomains(self, text):
        text = self.normalize_text(text)

        matched = []

        for subdomain, keywords in self.SUBDOMAIN_RULES.items():
            for keyword in keywords:
                normalized_keyword = self.normalize_text(keyword)

                if re.search(
                    rf"\b{re.escape(normalized_keyword)}\b",
                    text
                ):
                    matched.append(subdomain)
                    break

        return matched

    # =========================================================
    # CONFIDENCE ENGINE
    # =========================================================
    def calculate_confidence(
        self,
        domain_score,
        jurisdiction_score,
        severity_score,
        subdomain_count
    ):
        raw_score = (
            domain_score +
            jurisdiction_score +
            severity_score +
            (subdomain_count * 5)
        )

        return min(raw_score, 100)

    # =========================================================
    # FULL CLASSIFICATION
    # =========================================================
    def classify_event(
        self,
        title,
        source_url="",
        source_name=""
    ):
        combined_text = " ".join([
            str(title),
            str(source_url),
            str(source_name)
        ])

        domain_data = self.classify_domains(
            combined_text
        )

        jurisdiction_data = self.classify_jurisdiction(
            combined_text
        )

        severity_data = self.classify_severity(
            combined_text
        )

        subdomains = self.classify_subdomains(
            combined_text
        )

        confidence_score = self.calculate_confidence(
            domain_score=max(
                domain_data["domain_scores"].values(),
                default=0
            ),
            jurisdiction_score=jurisdiction_data[
                "jurisdiction_score"
            ],
            severity_score=severity_data[
                "severity_score"
            ],
            subdomain_count=len(subdomains)
        )

        return {
            "primary_domain": domain_data[
                "primary_domain"
            ],
            "secondary_domains": domain_data[
                "secondary_domains"
            ],
            "domain_scores": domain_data[
                "domain_scores"
            ],
            "jurisdiction": jurisdiction_data[
                "jurisdiction"
            ],
            "severity": severity_data[
                "severity"
            ],
            "subdomains": subdomains,
            "confidence_score": confidence_score
        }
