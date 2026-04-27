import re
import unicodedata


class LegalClassifier:
    """
    MAGICBANK SUPREME+ — Legal Classification Engine

    PURPOSE:
    Institutional classification of legal normative events.

    CLASSIFIES:
    - Primary legal domain
    - Secondary legal domains
    - Jurisdiction
    - Severity
    - Legal subdomains
    - Confidence score
    """

    # =========================================================
    # LEGAL DOMAIN RULES
    # =========================================================
    DOMAIN_RULES = {
        "constitucional": {
            "constitucion": 10,
            "constitucional": 10,
            "acto legislativo": 10,
            "derechos fundamentales": 9,
            "corte constitucional": 9,
            "sentencia c": 9,
            "sentencia su": 10
        },
        "penal": {
            "penal": 10,
            "codigo penal": 10,
            "delito": 9,
            "fiscalia": 8,
            "condena": 8,
            "procedimiento penal": 9
        },
        "civil": {
            "civil": 10,
            "codigo civil": 10,
            "contrato": 8,
            "obligaciones": 8,
            "responsabilidad civil": 9
        },
        "laboral": {
            "laboral": 10,
            "trabajo": 9,
            "codigo sustantivo": 9,
            "seguridad social": 9,
            "pension": 8,
            "empleador": 8
        },
        "administrativo": {
            "decreto": 9,
            "resolucion": 9,
            "acto administrativo": 10,
            "funcion publica": 8,
            "consejo de estado": 9
        },
        "tributario": {
            "tributario": 10,
            "impuesto": 9,
            "dian": 9,
            "estatuto tributario": 10
        },
        "comercial": {
            "comercial": 10,
            "sociedades": 9,
            "empresa": 8,
            "superintendencia": 8
        },
        "internacional": {
            "tratado": 10,
            "convencion": 9,
            "cidh": 9,
            "onu": 8,
            "internacional": 8
        }
    }

    # =========================================================
    # JURISDICTION RULES
    # =========================================================
    JURISDICTION_RULES = {
        "CO": {
            "colombia": 10,
            "ley": 8,
            "dian": 8,
            "senado": 8,
            "presidencia": 8,
            "corte constitucional": 9,
            "consejo de estado": 9
        },
        "INTERNATIONAL": {
            "onu": 10,
            "oea": 9,
            "cidh": 9,
            "tratado": 8
        }
    }

    # =========================================================
    # SEVERITY RULES
    # =========================================================
    SEVERITY_RULES = {
        "critical": {
            "reforma": 10,
            "acto legislativo": 10,
            "codigo": 10,
            "estatuto": 10,
            "ley": 9,
            "sentencia su": 10
        },
        "important": {
            "decreto": 8,
            "resolucion": 8,
            "sentencia c": 8
        },
        "informational": {
            "circular": 5,
            "boletin": 5,
            "concepto": 5
        }
    }

    # =========================================================
    # LEGAL SUBDOMAINS
    # =========================================================
    SUBDOMAIN_RULES = {
        "reforma_constitucional": [
            "acto legislativo",
            "reforma constitucional"
        ],
        "jurisprudencia_constitucional": [
            "sentencia c",
            "sentencia su",
            "corte constitucional"
        ],
        "codigo_penal": [
            "codigo penal",
            "procedimiento penal"
        ],
        "derecho_laboral": [
            "laboral",
            "seguridad social",
            "codigo sustantivo"
        ],
        "derecho_administrativo": [
            "acto administrativo",
            "decreto",
            "resolucion"
        ],
        "derecho_tributario": [
            "estatuto tributario",
            "impuesto",
            "dian"
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
            normalized_keyword = self.normalize_text(
                keyword
            )

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
                "primary_domain": "general_legal",
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
                normalized_keyword = self.normalize_text(
                    keyword
                )

                if re.search(
                    rf"\b{re.escape(normalized_keyword)}\b",
                    text
                ):
                    matched.append(subdomain)
                    break

        return matched

    # =========================================================
    # CONFIDENCE
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
