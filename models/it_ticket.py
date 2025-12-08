# ITTicket entity class - represents a single IT support ticket

class ITTicket:
    """Represents an IT support ticket in the platform."""

    def __init__(self, ticket_id: int, date: str, category: str, 
                 priority: str, status: str, description: str, assigned_to: str):
        self.__id = ticket_id
        self.__date = date
        self.__category = category
        self.__priority = priority
        self.__status = status
        self.__description = description
        self.__assigned_to = assigned_to


    # These methods allow safe read-only access to private attributes

    def get_id(self) -> int:
        """Return the ticket's unique identifier."""
        return self.__id

    def get_date(self) -> str:
        """Return the date/time when ticket was created."""

        return self.__date

    def get_category(self) -> str:
        """Return the category/type of IT issue."""
        return self.__category

    def get_priority(self) -> str:
        """Return the priority level as a string."""
        return self.__priority


    def get_status(self) -> str:
        """Return the current status of the ticket."""
        return self.__status

    def get_description(self) -> str:
        """Return the full description of the issue."""
        return self.__description

    def get_assigned_to(self) -> str:
        """Return the name of the assigned staff member."""
        return self.__assigned_to


    def assign_to(self, staff: str) -> None:
        """Assign the ticket to a specific staff member"""
        self.__assigned_to = staff

    def close_ticket(self) -> None:
        """
        Mark the ticket as closed/resolved.
        Sets status to "Closed" to indicate the issue has been resolved.
        """
        self.__status = "Closed"

    def get_priority_level(self) -> int:
        """Return an integer priority level."""
        mapping = {
            "low": 1,
            "medium": 2,
            "high": 3,
            "critical": 4,
        }
        return mapping.get(self.__priority.lower(), 0)

    def to_dict(self) -> dict:
        """
        Convert ticket object to a dictionary.
        Used when converting to pandas DataFrame or sending as JSON response.
        Key names match the database column names for consistency.
        """
        return {
            "id": self.__id,
            "date": self.__date,
            "category": self.__category,
            "priority": self.__priority,
            "status": self.__status,
            "description": self.__description,
            "assigned_to": self.__assigned_to
        }

    def __str__(self) -> str:
        """
        String representation of the ITTicket object.
        Used when printing the object: print(ticket)
        Formats: "Ticket [id]: [category] [[priority]] - [status]"
        Example: "Ticket 42: Hardware [critical] - In Progress"
        Provides a quick summary without overwhelming detail.
        """
        return f"Ticket {self.__id}: {self.__category} [{self.__priority}] - {self.__status}"

