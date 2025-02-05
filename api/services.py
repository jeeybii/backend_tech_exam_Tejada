from api.repository import insert_medalist, find_existing_medalist, get_aggregated_event_stats

# Insert Medalist (with Validation)
async def add_medalist(medalist_data):
    """ Add a medalist after checking for duplicates. """
    existing = await find_existing_medalist(medalist_data["name"], medalist_data["event"], medalist_data["medal_type"])
    if not existing:
        return await insert_medalist(medalist_data)
    return None  # Medalist already exists

# Get Event Statistics (Used in API)
async def fetch_event_stats(page: int = 1, limit: int = 10):
    """ Retrieve event statistics (calls repository). """
    return await get_aggregated_event_stats(page, limit)
