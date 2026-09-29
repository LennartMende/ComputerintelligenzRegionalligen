from typing import Protocol, Optional
from src.ClubData import ClubData
from src.RandomLocationsGenerator import RandomLocationsGenerator

class LocationProvider(Protocol):
    """Protocol defining the interface for location providers."""
    
    def get_locations(self) -> dict[int, tuple[float, float]]:
        """
        Returns a dictionary mapping club/location IDs to their coordinates.
        
        Returns:
            dict[int, tuple[float, float]]: Mapping from ID to (latitude, longitude)
        """
        ...

def get_location_provider(use_real_clubs: bool, n: Optional[int] = None) -> LocationProvider:
    """
    Factory function that returns the appropriate location provider.

    Args:
        use_real_clubs: If True, returns ClubDataProvider. If False, returns RandomLocationProvider.
        n: Number of random locations to generate. Required when use_real_clubs is False.

    Returns:
        LocationProvider: An instance of either ClubDataProvider or RandomLocationProvider.

    Raises:
        ValueError: If n is None when use_real_clubs is False.
    """
    
    if use_real_clubs:
        return ClubDataProvider()

    if n is None:
        raise ValueError("n must be provided when using random locations")

    return RandomLocationProvider(n)

class ClubDataProvider:
    def get_locations(self) -> dict[int, tuple[float, float]]:
        """
        Provides the real club coordinates.
        """
        return ClubData().club_coords

class RandomLocationProvider:

    def __init__(self, n: int):
        self.n = n
        self.locations = RandomLocationsGenerator.generate_random_locations(n)

    def get_locations(self) -> dict[int, tuple[float, float]]:
        return self.locations
