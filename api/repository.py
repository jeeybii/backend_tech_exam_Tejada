from api.db import insert_medalist, find_existing_medalist, insert_medalists_bulk, medalists_collection

# Fetch Aggregated Event Stats (Used by API)
async def get_aggregated_event_stats(page: int = 1, limit: int = 10):
    """ Retrieve event statistics with pagination. """
    skip = (page - 1) * limit

    pipeline = [
        {
            "$group": {
                "_id": {
                    "discipline": "$discipline",
                    "event": "$event",
                    "event_date": {
                        "$dateToString": {"format": "%Y-%m-%d", "date": "$medal_date"}
                    }
                },
                "medalists": {
                    "$push": {
                        "name": "$name",
                        "medal_type": "$medal_type",
                        "gender": "$gender",
                        "country_code": "$country_code",
                        "country": "$country",
                        "country_long": "$country_long",
                        "nationality": "$nationality",
                        "medal_code": "$medal_code",
                        "event_type": "$event_type",
                        "url_event": "$url_event",
                        "birth_date": "$birth_date",
                        "code_athlete": "$code_athlete",
                        "code_team": "$code_team",
                        "team": "$team",
                        "team_gender": "$team_gender"
                    }
                }
            }
        },
        {"$sort": {"_id.event_date": 1, "_id.discipline": 1, "_id.event": 1}},
        {"$skip": skip},
        {"$limit": limit},
        {
            "$project": {
                "_id": 0,
                "discipline": "$_id.discipline",
                "event": "$_id.event",
                "event_date": "$_id.event_date",
                "medalists": "$medalists"
            }
        }
    ]

    results = await medalists_collection.aggregate(pipeline).to_list(length=limit)
    total_count = await medalists_collection.count_documents({})
    total_pages = (total_count + limit - 1) // limit

    return {
        "data": results,
        "paginate": {
            "current_page": page,
            "total_pages": total_pages,
            "next_page": page + 1 if page < total_pages else None,
            "previous_page": page - 1 if page > 1 else None
        }
    }
