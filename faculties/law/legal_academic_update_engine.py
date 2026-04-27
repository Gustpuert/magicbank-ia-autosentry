from datetime import datetime


class LegalAcademicUpdateEngine:
    """
    MAGICBANK SUPREME+ — Legal Academic Update Engine

    PURPOSE:
    Transform legal curriculum impact into executable
    academic legal actions.

    INPUT:
    LegalCurriculumMapper output

    OUTPUT:
    - legal module update plan
    - jurisprudence revision
    - case law revision
    - legal assessment revision
    - certification review
    - governance escalation
    - legal academic versioning
    """

    # =========================================================
    # UPDATE RULES
    # =========================================================
    MODULE_UPDATE_RULES = {
        "Immediate": {
            "content_update": True,
            "jurisprudence_update": True,
            "case_law_revision": True,
            "assessment_update": True,
            "certification_review": True,
            "governance_alert": "CRITICAL"
        },
        "Priority": {
            "content_update": True,
            "jurisprudence_update": True,
            "case_law_revision": True,
            "assessment_update": True,
            "certification_review": False,
            "governance_alert": "IMPORTANT"
        },
        "Routine": {
            "content_update": True,
            "jurisprudence_update": False,
            "case_law_revision": False,
            "assessment_update": False,
            "certification_review": False,
            "governance_alert": "INFO"
        }
    }

    # =========================================================
    # VERSION CONTROL
    # =========================================================
    def generate_version(
        self,
        current_version="v1.0"
    ):
        """
        Semantic legal academic versioning:
        v1.0 -> v1.1
        """
        try:
            prefix = current_version[0]

            major, minor = current_version[
                1:
            ].split(".")

            major = int(major)
            minor = int(minor) + 1

            return f"{prefix}{major}.{minor}"

        except Exception:
            return "v1.1"

    # =========================================================
    # MODULE UPDATE PLAN
    # =========================================================
    def build_module_update_plan(
        self,
        affected_modules,
        urgency_level
    ):
        rules = self.MODULE_UPDATE_RULES.get(
            urgency_level,
            self.MODULE_UPDATE_RULES[
                "Routine"
            ]
        )

        module_plan = []

        for module in affected_modules:
            module_plan.append({
                "module_code": module,
                "update_content":
                    rules["content_update"],
                "update_jurisprudence":
                    rules[
                        "jurisprudence_update"
                    ],
                "update_case_law":
                    rules[
                        "case_law_revision"
                    ],
                "update_assessment":
                    rules[
                        "assessment_update"
                    ],
                "priority":
                    urgency_level
            })

        return module_plan

    # =========================================================
    # LEGAL CERTIFICATION REVIEW
    # =========================================================
    def build_certification_review(
        self,
        certifications,
        urgency_level
    ):
        rules = self.MODULE_UPDATE_RULES.get(
            urgency_level,
            self.MODULE_UPDATE_RULES[
                "Routine"
            ]
        )

        review_plan = []

        for certification in certifications:
            review_plan.append({
                "legal_certification":
                    certification,
                "review_required":
                    rules[
                        "certification_review"
                    ],
                "urgency":
                    urgency_level
            })

        return review_plan

    # =========================================================
    # GOVERNANCE ALERT
    # =========================================================
    def build_governance_alert(
        self,
        faculty,
        urgency_level
    ):
        rules = self.MODULE_UPDATE_RULES.get(
            urgency_level,
            self.MODULE_UPDATE_RULES[
                "Routine"
            ]
        )

        return {
            "faculty": faculty,
            "alert_level":
                rules[
                    "governance_alert"
                ],
            "timestamp":
                datetime.utcnow().isoformat(),
            "governance_action":
                f"{faculty} requires "
                f"{urgency_level} legal review"
        }

    # =========================================================
    # LEGAL CHANGE LOG
    # =========================================================
    def build_change_log(
        self,
        mapped_event,
        previous_version="v1.0"
    ):
        new_version = self.generate_version(
            previous_version
        )

        return {
            "previous_version":
                previous_version,
            "new_version":
                new_version,
            "change_timestamp":
                datetime.utcnow().isoformat(),
            "jurisdiction":
                mapped_event.get(
                    "jurisdiction"
                ),
            "faculty":
                mapped_event.get(
                    "faculty"
                ),
            "primary_domain":
                mapped_event.get(
                    "primary_domain"
                )
        }

    # =========================================================
    # FULL LEGAL UPDATE ENGINE
    # =========================================================
    def process_event(
        self,
        mapped_event,
        current_version="v1.0"
    ):
        urgency = mapped_event.get(
            "academic_urgency",
            {}
        )

        urgency_level = urgency.get(
            "level",
            "Routine"
        )

        affected_modules = mapped_event.get(
            "affected_modules",
            []
        )

        certifications = mapped_event.get(
            "certifications_impacted",
            []
        )

        faculty = mapped_event.get(
            "faculty",
            "General Legal Studies"
        )

        return {
            "legal_update_execution_plan": {
                "faculty": faculty,
                "modules":
                    self.build_module_update_plan(
                        affected_modules,
                        urgency_level
                    ),
                "legal_certifications":
                    self.build_certification_review(
                        certifications,
                        urgency_level
                    )
            },
            "legal_governance_alert":
                self.build_governance_alert(
                    faculty,
                    urgency_level
                ),
            "legal_academic_version_control":
                self.build_change_log(
                    mapped_event,
                    current_version
                ),
            "system_status": {
                "update_required": True,
                "legal_processed_at":
                    datetime.utcnow().isoformat(),
                "confidence_score":
                    mapped_event.get(
                        "confidence_score",
                        0
                    )
            }
        }
