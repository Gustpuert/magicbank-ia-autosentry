from collections import defaultdict


class CurriculumMapper:
    """
    MAGICBANK SUPREME+ — Curriculum Mapping Engine

    PURPOSE:
    Transform normative classification into academic impact.

    INPUT:
    NormativeClassifier output

    OUTPUT:
    - impacted faculty
    - affected modules
    - specialization tracks
    - certification impact
    - academic urgency
    """

    # =====================================================
    # DOMAIN → FACULTY MAP
    # =====================================================
    DOMAIN_FACULTY_MAP = {
        "tributario": "Tax & Compliance Faculty",
        "contable": "Financial Accounting Faculty",
        "auditoria": "Audit & Assurance Faculty",
        "compliance": "Regulatory Compliance Faculty",
        "financiero": "Corporate Finance Faculty",
        "general_normative": "General Academic Governance"
    }

    # =====================================================
    # SUBDOMAIN → MODULE MAP
    # =====================================================
    SUBDOMAIN_MODULE_MAP = {
        "facturacion_electronica": [
            "CO-TAX-FACT-201",
            "CO-COMPLIANCE-FACT-301",
            "BOOKKEEPING-DIGITAL-110"
        ],
        "iva_vat": [
            "CO-TAX-VAT-202",
            "US-SALES-TAX-204",
            "CA-GST-HST-205"
        ],
        "retencion_withholding": [
            "CO-TAX-WITHHOLDING-203",
            "US-PAYROLL-TAX-305"
        ],
        "payroll_tax": [
            "US-PAYROLL-306",
            "CA-PAYROLL-307"
        ],
        "financial_reporting": [
            "IFRS-REPORT-401",
            "US-GAAP-402",
            "FIN-STMT-210"
        ],
        "audit_assurance": [
            "AUDIT-601",
            "RISK-602",
            "CONTROL-603"
        ],
        "us_gaap": [
            "US-GAAP-401",
            "US-GAAP-702"
        ],
        "ifrs_niif": [
            "IFRS-401",
            "IFRS-702"
        ]
    }

    # =====================================================
    # JURISDICTION TRACKS
    # =====================================================
    JURISDICTION_TRACK_MAP = {
        "CO": [
            "Colombia Taxation",
            "Colombia Compliance",
            "DIAN Professional Track"
        ],
        "US": [
            "US Taxation",
            "IRS Compliance",
            "US GAAP",
            "CPA Track"
        ],
        "CA": [
            "Canada Taxation",
            "CRA Compliance",
            "Canadian Accounting"
        ],
        "INTERNATIONAL": [
            "IFRS International",
            "Global Compliance"
        ],
        "GLOBAL": [
            "Global Governance"
        ]
    }

    # =====================================================
    # CERTIFICATION IMPACT
    # =====================================================
    CERTIFICATION_MAP = {
        "tributario": [
            "Tax & Compliance Certification",
            "Jurisdiction Tax Specialist"
        ],
        "contable": [
            "Financial Accounting Certification",
            "IFRS / GAAP Professional"
        ],
        "auditoria": [
            "Audit & Assurance Certification"
        ],
        "compliance": [
            "Regulatory Compliance Certification"
        ],
        "financiero": [
            "Corporate Finance Certification"
        ]
    }

    # =====================================================
    # SEVERITY → ACADEMIC URGENCY
    # =====================================================
    URGENCY_MAP = {
        "critical": {
            "level": "Immediate",
            "update_window_days": 1
        },
        "important": {
            "level": "Priority",
            "update_window_days": 7
        },
        "informational": {
            "level": "Routine",
            "update_window_days": 30
        }
    }

    # =====================================================
    # FACULTY
    # =====================================================
    def map_faculty(self, primary_domain):
        return self.DOMAIN_FACULTY_MAP.get(
            primary_domain,
            "General Academic Governance"
        )

    # =====================================================
    # MODULES
    # =====================================================
    def map_modules(self, subdomains):
        modules = []

        for subdomain in subdomains:
            modules.extend(
                self.SUBDOMAIN_MODULE_MAP.get(
                    subdomain,
                    []
                )
            )

        return sorted(list(set(modules)))

    # =====================================================
    # TRACKS
    # =====================================================
    def map_tracks(self, jurisdiction):
        return self.JURISDICTION_TRACK_MAP.get(
            jurisdiction,
            ["Global Governance"]
        )

    # =====================================================
    # CERTIFICATIONS
    # =====================================================
    def map_certifications(self, primary_domain):
        return self.CERTIFICATION_MAP.get(
            primary_domain,
            []
        )

    # =====================================================
    # URGENCY
    # =====================================================
    def map_urgency(self, severity):
        return self.URGENCY_MAP.get(
            severity,
            {
                "level": "Routine",
                "update_window_days": 30
            }
        )

    # =====================================================
    # FULL CURRICULUM IMPACT
    # =====================================================
    def map_event(self, classification):
        primary_domain = classification.get(
            "primary_domain",
            "general_normative"
        )

        jurisdiction = classification.get(
            "jurisdiction",
            "GLOBAL"
        )

        severity = classification.get(
            "severity",
            "informational"
        )

        subdomains = classification.get(
            "subdomains",
            []
        )

        return {
            "faculty": self.map_faculty(
                primary_domain
            ),
            "primary_domain": primary_domain,
            "secondary_domains": classification.get(
                "secondary_domains",
                []
            ),
            "jurisdiction": jurisdiction,
            "affected_modules": self.map_modules(
                subdomains
            ),
            "specialization_tracks": self.map_tracks(
                jurisdiction
            ),
            "certifications_impacted": self.map_certifications(
                primary_domain
            ),
            "academic_urgency": self.map_urgency(
                severity
            ),
            "confidence_score": classification.get(
                "confidence_score",
                0
            )
        }
