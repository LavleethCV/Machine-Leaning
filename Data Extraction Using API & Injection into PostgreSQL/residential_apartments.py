import googlemaps
import pandas as pd
import numpy as np

hyderabad_gps = pd.read_excel("C:/Users/lavle/Desktop/Hyderbad/mapping.xlsx")


def resap_apartments():
    gmaps = googlemaps.Client(key="Enter API Key")
    radius = 1500
    keyword = "residential apartments"
    all_results = []
    for index, row in hyderabad_gps.iterrows():
        latitude = row["Latitude"]
        longitude = row["Longitude"]
        response = gmaps.places_nearby(
            location=(latitude, longitude), radius=radius, keyword=keyword
        )
        results_data = []
        if "results" in response:
            for result in response["results"]:
                Business_Status = result.get("business_status", "N/A")
                Apartment_name = result["name"]
                Address = result.get("vicinity", "N/A")
                Location = result.get("geometry", {}).get("location", {})
                viewport = result.get("geometry", {}).get("viewport", {})
                Reference = result.get("reference", "N/A")
                Icon = result.get("icon", "N/A")
                Place_ID = result.get("place_id", "N/A")
                Rating = result.get("rating", "N/A")
                User_Ratings_Total = result.get("user_ratings_total", "N/A")
                if "photos" in result:
                    photo_reference = result["photos"][0]["photo_reference"]
                    photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key='API KEY'"
                    results_data.append(
                        {
                            "Business_Status": Business_Status,
                            "Apartment_name": Apartment_name,
                            "Address": Address,
                            "Location": Location,
                            "viewport": viewport,
                            "Icon": Icon,
                            "Reference": Reference,
                            "Place_id": Place_ID,
                            "Photourl": photo_url,
                            "Rating": Rating,
                            "User_Ratings_Total": User_Ratings_Total,
                        }
                    )
                else:
                    results_data.append(
                        {
                            "Business_Status": Business_Status,
                            "Apartment_name": Apartment_name,
                            "Address": Address,
                            "Location": Location,
                            "viewport": viewport,
                            "Icon": Icon,
                            "Reference": Reference,
                            "Place_Id": Place_ID,
                            "Photourl": None,
                            "Rating": Rating,
                            "User_Ratings_Total": User_Ratings_Total,
                        }
                    )

        else:
            print("No Apartment Found")
        all_results.extend(results_data)
        apartments = pd.DataFrame(all_results)
        split_columns = apartments["Location"].apply(pd.Series)
        split_columns1 = apartments["viewport"].apply(pd.Series)
        split_columns.rename(
            columns={"lat": "Latitude", "lng": "Longitude"}, inplace=True
        )
        apartments = pd.concat([apartments, split_columns, split_columns1], axis=1)
        split_columns2 = apartments["northeast"].apply(pd.Series)
        split_columns2.rename(
            columns={"lat": "Northeast_lan", "lng": "Northeast_lng"}, inplace=True
        )
        split_columns3 = apartments["southwest"].apply(pd.Series)
        split_columns3.rename(
            columns={"lat": "Southwest_lan", "lng": "Southwest_lng"}, inplace=True
        )
        apartments = pd.concat([apartments, split_columns2, split_columns3], axis=1)
        apartments = apartments.drop(
            labels=["Location", "viewport", "northeast", "southwest"], axis=1
        )
        apartments.fillna("N/A", inplace=True)
        apartments_copy = apartments.copy()
        apartments_copy = apartments_copy.drop_duplicates(subset="Apartment_name")
        apartments_copy.reset_index(drop=True, inplace=True)
        apartments_copy["City"] = pd.Series(
            ["Hyderabad" for i in range(len(apartments_copy))]
        )
        apartments_copy["State"] = pd.Series(
            ["Telangana" for i in range(len(apartments_copy))]
        )
    return apartments_copy
