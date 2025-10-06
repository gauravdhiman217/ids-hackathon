from pydantic import BaseModel, Field


class CategoriesProbabilities(BaseModel):

    CSG_PDG_17: float = Field(
        ...,
        description="Probability that the ticket is related to Corporate Services Group – Product Development Group internal tools or systems.",
    )
    Desktop_12: float = Field(
        ...,
        description="Probability that the ticket relates to general desktop issues, including software, settings, or performance.",
    )
    Desktop_Application_13: float = Field(
        ...,
        description="Probability that the ticket is about problems with installed desktop applications (e.g., MS Office, browsers).",
    )

    Desktop_Hardware_15: float = Field(
        ...,
        description="Probability that the ticket is related to physical hardware issues such as monitor, keyboard, or peripherals.",
    )
    Desktop_Login_Issue_18: float = Field(
        ...,
        description="Probability that the ticket is about desktop login problems, like incorrect credentials or account lockouts.",
    )

    Email_11: float = Field(
        ...,
        description="Probability that the ticket relates to general email issues, including access, sync, or configuration problems.",
    )
    Email_Email_Create_21: float = Field(
        ...,
        description="Probability that the ticket is a request to create a new company email ID or mailbox.",
    )
    Email_Whitelist_Email_19: float = Field(
        ...,
        description="Probability that the ticket requests to whitelist an email address or domain to prevent blocking or spam issues.",
    )
    Internet_9: float = Field(
        ...,
        description="Probability that the ticket relates to internet connectivity issues, such as no access, slow speed, or frequent disconnections.",
    )
    Network_8: float = Field(
        ...,
        description="Probability that the ticket involves internal network problems, including LAN/Wi-Fi issues or access to shared resources.",
    )
    International_Calling_10: float = Field(
        ...,
        description="Probability that the ticket relates to enabling, disabling, or troubleshooting international calling services.",
    )
    Server_2: float = Field(
        ...,
        description="Probability that the ticket is about general server-related issues or requests not covered by subcategories.",
    )
    Server_Application_4: float = Field(
        ...,
        description="Probability that the ticket concerns applications hosted on servers, including downtime or access errors.",
    )

    Printing_3: float = Field(
        ...,
        description="Probability that the ticket is about printing issues, such as printer detection, queue errors, or print quality problems.",
    )

    Others_6: float = Field(
        ...,
        description="Probability that the ticket does not fall into any predefined categories and needs manual review or reassignment.",
    )

    def top_category(self) -> tuple[str, float]:
        data = self.model_dump()
        return max(data.items(), key=lambda kv: kv[1])
