from datetime import datetime
import uuid


class GovernanceAuditLayer:
    """
    MAGICBANK SUPREME+ — Governance & Audit Layer

    PURPOSE:
    Institutional control layer for:
    - approval
    - escalation
    - auditability
    - certification integrity
    - deployment governance

    INPUT:
    AcademicUpdateEngine output

    OUTPUT:
    - governance decision
    - escalation path
    - audit log
    - certification protection
    - deployment authorization
    """

    # =========================================================
    # CONFIDENCE THRESHOLDS
    # =========================================================
    CONFIDENCE_RULES = {
        "auto_approve": 85,
        "human_review": 60
    }

    # =========================================================
    # ALERT ESCALATION
    # =========================================================
    ALERT_ESCALATION = {
        "CRITICAL": {
            "approval_mode": "committee_review",
            "deployment_status": "blocked_pending_committee",
            "certification_lock": True
        },
        "IMPORTANT": {
            "approval_mode": "human_review",
            "deployment_status": "pending_specialist_review",
            "certification_lock": False
        },
        "INFO": {
            "approval_mode": "auto_approve",
            "deployment_status": "approved",
            "certification_lock": False
        }
    }

    # =========================================================
    # AUDIT ID
    # =========================================================
    def generate_audit_id(self):
        return f"MAGIC-AUDIT-{uuid.uuid4()}"

    # =========================================================
    # DETERMINE REVIEW PATH
    # =========================================================
    def determine_review_path(
        self,
        confidence_score,
        governance_alert_level
    ):
        if governance_alert_level == "CRITICAL":
            return self.ALERT_ESCALATION[
                "CRITICAL"
            ]

        if confidence_score >= self.CONFIDENCE_RULES[
            "auto_approve"
        ]:
            return self.ALERT_ESCALATION[
                "INFO"
            ]

        if confidence_score >= self.CONFIDENCE_RULES[
            "human_review"
        ]:
            return self.ALERT_ESCALATION[
                "IMPORTANT"
            ]

        return {
            "approval_mode": "manual_investigation",
            "deployment_status":
                "blocked_low_confidence",
            "certification_lock": True
        }

    # =========================================================
    # CERTIFICATION IMPACT
    # =========================================================
    def build_certification_integrity(
        self,
        certifications,
        certification_lock
    ):
        integrity_plan = []

        for certification in certifications:
            integrity_plan.append({
                "certification": certification,
                "status":
                    "locked_pending_review"
                    if certification_lock
                    else "active",
                "recertification_required":
                    certification_lock
            })

        return integrity_plan

    # =========================================================
    # DEPLOYMENT GOVERNANCE
    # =========================================================
    def build_deployment_governance(
        self,
        review_path,
        faculty
    ):
        return {
            "faculty": faculty,
            "approval_mode": review_path[
                "approval_mode"
            ],
            "deployment_status": review_path[
                "deployment_status"
            ],
            "governance_owner":
                "MagicBank Normative Governance Committee"
                if review_path[
                    "approval_mode"
                ] == "committee_review"
                else "Assigned Academic Specialist"
        }

    # =========================================================
    # AUDIT LOG
    # =========================================================
    def build_audit_log(
        self,
        academic_update_output,
        review_path
    ):
        governance_alert = academic_update_output.get(
            "governance_alert",
            {}
        )

        version_control = academic_update_output.get(
            "academic_version_control",
            {}
        )

        return {
            "audit_id": self.generate_audit_id(),
            "timestamp": datetime.utcnow().isoformat(),
            "faculty": governance_alert.get(
                "faculty"
            ),
            "alert_level": governance_alert.get(
                "alert_level"
            ),
            "approval_mode": review_path.get(
                "approval_mode"
            ),
            "previous_version": version_control.get(
                "previous_version"
            ),
            "target_version": version_control.get(
                "new_version"
            ),
            "audit_status":
                "pending"
                if "blocked" in review_path.get(
                    "deployment_status",
                    ""
                )
                else "approved"
        }

    # =========================================================
    # FULL GOVERNANCE PROCESS
    # =========================================================
    def process_update(
        self,
        academic_update_output
    ):
        system_status = academic_update_output.get(
            "system_status",
            {}
        )

        governance_alert = academic_update_output.get(
            "governance_alert",
            {}
        )

        execution_plan = academic_update_output.get(
            "update_execution_plan",
            {}
        )

        confidence_score = system_status.get(
            "confidence_score",
            0
        )

        governance_alert_level = governance_alert.get(
            "alert_level",
            "INFO"
        )

        faculty = governance_alert.get(
            "faculty",
            "General Academic Governance"
        )

        certifications = [
            cert.get("certification")
            for cert in execution_plan.get(
                "certifications",
                []
            )
        ]

        review_path = self.determine_review_path(
            confidence_score,
            governance_alert_level
        )

        certification_integrity = (
            self.build_certification_integrity(
                certifications,
                review_path.get(
                    "certification_lock",
                    False
                )
            )
        )

        deployment_governance = (
            self.build_deployment_governance(
                review_path,
                faculty
            )
        )

        audit_log = self.build_audit_log(
            academic_update_output,
            review_path
        )

        return {
            "governance_decision": deployment_governance,
            "certification_integrity": (
                certification_integrity
            ),
            "audit_log": audit_log,
            "institutional_status": {
                "system_approved":
                    deployment_governance[
                        "deployment_status"
                    ] == "approved",
                "requires_human_action":
                    review_path[
                        "approval_mode"
                    ] != "auto_approve",
                "certification_lock_active":
                    review_path.get(
                        "certification_lock",
                        False
                    )
            }
        }
