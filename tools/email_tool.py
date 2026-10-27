"""
BizPilot AI — Email Drafting Tool
Agent tool for composing professional business emails.
The LLM composes the actual email body content; this tool formats it properly.
"""

from langchain.tools import tool


@tool
def draft_email(
    to: str,
    subject: str,
    body_instructions: str,
    tone: str = "professional",
) -> str:
    """
    Draft a professional business email based on instructions.
    Use this tool when the user asks to write, compose, or send an email.

    Args:
        to: Recipient email address or name.
        subject: Email subject line.
        body_instructions: Instructions for what the email body should contain.
        tone: Tone of the email (professional, friendly, formal, urgent). Default: professional.

    Returns:
        A formatted, ready-to-send email draft with the full composed body.
    """
    # Tone-based greeting/sign-off mapping
    tone_map = {
        "professional": ("Dear", "Best regards,\nBizPilot AI Business Team"),
        "friendly":     ("Hi", "Warm regards,\nBizPilot AI Business Team"),
        "formal":       ("To Whom It May Concern" if "@" not in to else f"Dear {to.split('@')[0].title()},", "Yours sincerely,\nBizPilot AI Business Team"),
        "urgent":       ("Dear", "Urgent regards,\nBizPilot AI Business Team"),
    }
    greeting_prefix, sign_off = tone_map.get(tone.lower(), ("Dear", "Best regards,\nBizPilot AI Business Team"))
    recipient_name = to.split("@")[0].title() if "@" in to else to

    email_draft = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📧 EMAIL DRAFT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
To:      {to}
Subject: {subject}
Tone:    {tone.title()}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{greeting_prefix} {recipient_name},

{body_instructions}

{sign_off}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 Status: DRAFT — Please review before sending
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    return email_draft
