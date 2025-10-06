from pydantic import BaseModel, Field


class CategoriesProbabilities(BaseModel):
    Desktop: float = Field(
        ...,
        description="Probability that the ticket relates to general desktop issues, including software, settings, or performance.",
    )
    Desktop_Application: float = Field(
        ...,
        description="Probability that the ticket is about problems with installed desktop applications (e.g., MS Office, browsers).",
    )
    Desktop_Asset_Management: float = Field(
        ...,
        description="Probability that the ticket concerns desktop asset tracking, inventory, or allocation.",
    )
    Desktop_Hardware: float = Field(
        ...,
        description="Probability that the ticket is related to physical hardware issues such as monitor, keyboard, or peripherals.",
    )
    Desktop_Login_Issue: float = Field(
        ...,
        description="Probability that the ticket is about desktop login problems, like incorrect credentials or account lockouts.",
    )
    Desktop_Storage: float = Field(
        ...,
        description="Probability that the ticket involves local storage issues, such as low disk space or drive access problems.",
    )
    Email: float = Field(
        ...,
        description="Probability that the ticket relates to general email issues, including access, sync, or configuration problems.",
    )
    Email_Email_Create: float = Field(
        ...,
        description="Probability that the ticket is a request to create a new company email ID or mailbox.",
    )
    Email_Whitelist_Email: float = Field(
        ...,
        description="Probability that the ticket requests to whitelist an email address or domain to prevent blocking or spam issues.",
    )
    Internet: float = Field(
        ...,
        description="Probability that the ticket relates to internet connectivity issues, such as no access, slow speed, or frequent disconnections.",
    )
    Network: float = Field(
        ...,
        description="Probability that the ticket involves internal network problems, including LAN/Wi-Fi issues or access to shared resources.",
    )
    International_Calling: float = Field(
        ...,
        description="Probability that the ticket relates to enabling, disabling, or troubleshooting international calling services.",
    )
    Server: float = Field(
        ...,
        description="Probability that the ticket is about general server-related issues or requests not covered by subcategories.",
    )
    Server_Application: float = Field(
        ...,
        description="Probability that the ticket concerns applications hosted on servers, including downtime or access errors.",
    )
    Server_Client_Servers: float = Field(
        ...,
        description="Probability that the ticket relates to client-specific servers, configurations, or deployment problems.",
    )
    Storage: float = Field(
        ...,
        description="Probability that the ticket involves shared or cloud storage issues (e.g., OneDrive, NAS, shared drives).",
    )
    Printing: float = Field(
        ...,
        description="Probability that the ticket is about printing issues, such as printer detection, queue errors, or print quality problems.",
    )
    Website_Blocked: float = Field(
        ...,
        description="Probability that the ticket requests access to a blocked website or restricted web content.",
    )
    New_Service_Request: float = Field(
        ...,
        description="Probability that the ticket is a request for a new IT service, software installation, or hardware provisioning.",
    )
    CSG_PDG: float = Field(
        ...,
        description="Probability that the ticket is related to Corporate Services Group – Product Development Group internal tools or systems.",
    )
    Others: float = Field(
        ...,
        description="Probability that the ticket does not fall into any predefined categories and needs manual review or reassignment.",
    )
    
    def top_category(self) -> tuple[str, float]:
        data = self.model_dump()  
        return max(data.items(), key=lambda kv: kv[1])
