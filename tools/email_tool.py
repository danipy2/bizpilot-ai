"""
BizPilot AI — Email Drafting Tool
Agent tool for composing professional business emails.
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
        A formatted, ready-to-send email draft.
    """
    # The agent uses the LLM's capability to draft the actual content
    # This tool structures the output properly

    email_draft = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📧 EMAIL DRAFT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
To:      {to}
Subject: {subject}
Tone:    {tone}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Based on instructions: {body_instructions}

[The AI agent will compose the full email body using the instructions above]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Status: 📝 DRAFT (Review before sending)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    return email_draft
