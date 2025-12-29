from pydantic import BaseModel, Field


class TicketTypeProbabilities(BaseModel):
    Unclassified_1: float = Field(
        ...,
        description="Probability of an unclassified ticket, needs manual review.",
    )
    # RfC_2: float = Field(
    #     ...,
    #     description="Probability that the ticket is a Request for Change (RFC).",
    # )
    # Incident_3: float = Field(
    #     ...,
    #     description="Probability that the ticket is an Incident (unplanned service disruption).",
    # )
    # Incident_Major_4: float = Field(
    #     ...,
    #     description="Probability that the incident is a major outage or critical failure.",
    # )
    ServiceRequest_5: float = Field(
        ...,
        description="Probability that the ticket is a standard service request.",
    )
    # Problem_6: float = Field(
    #     ...,
    #     description="Probability that the ticket pertains to problem investigation and root cause analysis.",
    # )
    Change_Request_7: float = Field(
        ...,
        description="Probability that the ticket is a formal change request for system updates.",
    )
    Client_Servers_8: float = Field(
        ...,
        description="Probability that the ticket involves client-specific server issues.",
    )
    # Incident_Disaster_9: float = Field(
    #     ...,
    #     description="Probability of a disaster-level incident impacting critical systems.",
    # )
    # Incident_ServiceRequest_10: float = Field(
    #     ...,
    #     description="Probability that the incident is actually a service request ongoing as an incident.",
    # )
    # Problem_KnownError_11: float = Field(
    #     ...,
    #     description="Probability that the problem has a known error with documented workarounds.",
    # )
    # Problem_PendingRfC_12: float = Field(
    #     ...,
    #     description="Probability that problem resolution is pending an RFC implementation.",
    # )
    # Default_13: float = Field(
    #     ...,
    #     description="Probability of a default or unclassified ticket.",
    # )
    Firewall_14: float = Field(
        ...,
        description="Probability that the ticket relates to firewall or network security issues.",
    )
    # Others_15: float = Field(
    #     ...,
    #     description="Probability that the ticket falls outside predefined categories and needs review.",
    # )

    def top_category(self) -> tuple[str, float]:
        data = self.model_dump()
        return max(data.items(), key=lambda kv: kv[1])
