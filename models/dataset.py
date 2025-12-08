# Dataset entity class - represents a single dataset record from the database
class Dataset:
    """Represents a data science dataset in the platform."""

    def __init__(self, dataset_id: int, name: str, category: str, 
                 source: str, last_updated: str, record_count: int, file_size_mb: float):
        self.__id = dataset_id
        self.__name = name
        self.__category = category
        self.__source = source
        self.__last_updated = last_updated
        self.__record_count = record_count
        self.__file_size_mb = file_size_mb


    # These methods allow external code to read the private attributes safely

    def get_id(self) -> int:
        """Return the dataset's unique identifier."""
        return self.__id


    def get_name(self) -> str:
        """Return the dataset's name."""
        return self.__name


    def get_category(self) -> str:
        """Return the dataset's category classification."""
        return self.__category


    def get_source(self) -> str:
        """Return where the dataset came from."""
        return self.__source


    def get_last_updated(self) -> str:
        """Return the timestamp of the last update."""
        return self.__last_updated


    def get_record_count(self) -> int:
        """Return the number of records in the dataset."""
        return self.__record_count

    def get_file_size_mb(self) -> float:
        """Return the file size in megabytes."""
        return self.__file_size_mb

    def calculate_size_bytes(self) -> int:
        """Convert MB to bytes."""
        return int(self.__file_size_mb * 1024 * 1024)


    def to_dict(self) -> dict:
        """
        Convert dataset object to a dictionary.
        Used when converting to pandas DataFrame or JSON response.
        Key names match the database column names.
        """
        return {
            "id": self.__id,
            "dataset_name": self.__name,
            "category": self.__category,
            "source": self.__source,
            "last_updated": self.__last_updated,
            "record_count": self.__record_count,
            "file_size_mb": self.__file_size_mb
        }


    def __str__(self) -> str:
        """
        String representation of the Dataset object.
        Used when printing the object: print(dataset)
        Formats: "Dataset [id]: [name] ([size] MB, [count] rows)"
        Example: "Dataset 5: Security Logs (256.50 MB, 50000 rows)"
        """
        return f"Dataset {self.__id}: {self.__name} ({self.__file_size_mb:.2f} MB, {self.__record_count} rows)"

