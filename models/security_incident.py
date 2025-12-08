# SecurityIncident entity class - represents a single cybersecurity incident

class SecurityIncident:
    """Represents a cybersecurity incident in the platform."""

    def __init__(self, incident_id: int, date: str, incident_type: str, 
                 severity: str, status: str, description: str):
        self.__id = incident_id
        self.__date = date
        self.__incident_type = incident_type
        self.__severity = severity
        self.__status = status
        self.__description = description

    # These methods provide safe read-only access to private incident data
    def get_id(self) -> int:
        """Return the incident's unique identifier."""
        return self.__id

    def get_date(self) -> str:
        """Return the date/time when the incident was detected."""
        return self.__date

    def get_incident_type(self) -> str:
        """Return the type/category of the security incident."""
        return self.__incident_type

    def get_severity(self) -> str:
        """Return the severity level as a string."""
        return self.__severity

    def get_status(self) -> str:
        """Return the current status of the incident."""
        return self.__status

    def get_description(self) -> str:
        """Return the full description of the incident details."""
        return self.__description
    
    # These methods update the incident status as it progresses through investigation and resolution

    def update_status(self, new_status: str) -> None:
        self.__status = new_status

    def get_severity_level(self) -> int:
        """Return an integer severity level."""
        mapping = {
            "low": 1,
            "medium": 2,
            "high": 3,
            "critical": 4,
        }
        return mapping.get(self.__severity.lower(), 0)

    def to_dict(self) -> dict:
        """
        Convert incident object to a dictionary.
        Used when converting to pandas DataFrame or sending as JSON response.
        Key names match the database column names for consistency.
        Allows easy serialization for API responses and data storage.
        """
        return {
            "id": self.__id,
            "date": self.__date,
            "incident_type": self.__incident_type,
            "severity": self.__severity,
            "status": self.__status,
            "description": self.__description
        }

    def __str__(self) -> str:
        """
        String representation of the SecurityIncident object.
        Used when printing the object: print(incident)
        Formats: "Incident [id] [SEVERITY] [type]"
        Example: "Incident 15 [CRITICAL] Malware"
        
        Provides a quick, scannable summary with severity in caps for visibility
        (critical incidents stand out in logs and dashboards).
        """

        return f"Incident {self.__id} [{self.__severity.upper()}] {self.__incident_type}"

