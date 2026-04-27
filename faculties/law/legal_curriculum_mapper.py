class LegalCurriculumMapper:
    """
    MAGICBANK SUPREME+ — Legal Curriculum Mapping Engine

    PURPOSE:
    Transform legal classification into academic legal impact.
    """

    # =====================================================
    # DOMAIN → FACULTY
    # =====================================================
    DOMAIN_FACULTY_MAP = {
        "constitucional": "Constitutional Law Faculty",
        "penal": "Criminal Law Faculty",
        "civil": "Civil Law Faculty",
        "laboral": "Labor Law Faculty",
        "administrativo": "Administrative Law Faculty",
        "tributario": "Tax Law Faculty",
        "comercial": "Commercial Law Faculty",
        "internacional": "International Law Faculty",
        "general_legal": "General Legal Studies"
    }

    # =====================================================
    # SUBDOMAIN → MODULES
    # =====================================================
    SUBDOMAIN_MODULE_MAP = {
        "reforma_constitucional": [
            "LAW-CONST-201",
            "LAW-STATE-202",
            "LAW-JURIS-301"
        ],
        "jurisprudencia_constitucional": [
            "LAW-CONST-301",
            "LAW-RIGHTS-302"
        ],
        "codigo_penal": [
            "LAW-PENAL-201",
            "LAW-CRIMPROC-202"
        ],
        "derecho_laboral": [
            "LAW-LABOR-201",
            "LAW-SOCSEC-202",
            "LAW-LITLAB-301"
        ],
        "derecho_administrativo": [
            "LAW-ADMIN-201",
            "LAW-PUBLIC-202"
        ],
        "derecho_tributario": [
            "LAW-TAX-201",
            "LAW-FISCAL-301"
        ]
    }

    # =====================================================
    # JURISDICTION TRACKS
    # =====================================================
    JURISDICTION_TRACK_MAP = {
        "CO": [
            "Colombian Legal Practice",
            "Public Law Colombia",
            "National Jurisprudence"
        ],
        "INTERNATIONAL": [
            "International Law",
            "Human Rights",
            "Treaty Law"
        ],
        "GLOBAL": [
            "General Legal Governance"
        ]
    }

    # =====================================================
    # CERTIFICATION MAP
    # =====================================================
    CERTIFICATION_MAP = {
        "constitucional": [
            "Constitutional Law Certification"
        ],
        "penal": [
            "Criminal Law Certification"
        ],
        "civil": [
            "Civil Law Certification"
        ],
        "laboral": [
            "Labor Law Certification"
        ],
        "administrativo": [
            "Administrative Law Certification"
        ],
        "tributario": [
            "Tax Law Certification"
        ],
        "comercial": [
            "Commercial Law Certification"
        ],
        "internacional": [
            "International Legal Certification"
        ]
    }

    # =====================================================
    # SEVERITY → URGENCY
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
            "General Legal Studies"
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
            ["General Legal Governance"]
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
    # FULL LEGAL CURRICULUM IMPACT
    # =====================================================
    def map_event(self, classification):
        primary_domain = classification.get(
            "primary_domain",
            "general_legal"
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
