from django.test import TestCase

# Create your tests here.
from .models import BusRoute

locations = [
    "Thrissur", "Ollur", "Irinjalakuda", "Chalakudy", "Kunnamkulam", 
    "Guruvayur", "Kodungallur", "Chavakkad", "Wadakkanchery", "Mala", 
    "Pavaratty", "Kaipamangalam", "Mannuthy"
]

distance_map = {
    ("Thrissur", "Ollur"): 7,
    ("Thrissur", "Irinjalakuda"): 20,
    ("Thrissur", "Chalakudy"): 25,
    ("Thrissur", "Kunnamkulam"): 22,
    ("Thrissur", "Guruvayur"): 30,
    ("Thrissur", "Kodungallur"): 40,
    ("Thrissur", "Chavakkad"): 25,
    ("Thrissur", "Wadakkanchery"): 15,
    ("Thrissur", "Mala"): 10,
    ("Thrissur", "Pavaratty"): 18,
    ("Thrissur", "Kaipamangalam"): 30,
    ("Thrissur", "Mannuthy"): 10,
    ("Ollur", "Irinjalakuda"): 12,
    ("Ollur", "Chalakudy"): 18,
    ("Ollur", "Kunnamkulam"): 18,
    ("Ollur", "Guruvayur"): 26,
    ("Ollur", "Kodungallur"): 35,
    ("Ollur", "Chavakkad"): 20,
    ("Ollur", "Wadakkanchery"): 10,
    ("Ollur", "Mala"): 15,
    ("Ollur", "Pavaratty"): 8,
    ("Ollur", "Kaipamangalam"): 20,
    ("Ollur", "Mannuthy"): 12,
    ("Irinjalakuda", "Chalakudy"): 13,
    ("Irinjalakuda", "Kunnamkulam"): 19,
    ("Irinjalakuda", "Guruvayur"): 24,
    ("Irinjalakuda", "Kodungallur"): 32,
    ("Irinjalakuda", "Chavakkad"): 18,
    ("Irinjalakuda", "Wadakkanchery"): 9,
    ("Irinjalakuda", "Mala"): 12,
    ("Irinjalakuda", "Pavaratty"): 15,
    ("Irinjalakuda", "Kaipamangalam"): 20,
    ("Irinjalakuda", "Mannuthy"): 16,
    ("Chalakudy", "Kunnamkulam"): 17,
    ("Chalakudy", "Guruvayur"): 25,
    ("Chalakudy", "Kodungallur"): 35,
    ("Chalakudy", "Chavakkad"): 15,
    ("Chalakudy", "Wadakkanchery"): 10,
    ("Chalakudy", "Mala"): 14,
    ("Chalakudy", "Pavaratty"): 12,
    ("Chalakudy", "Kaipamangalam"): 24,
    ("Chalakudy", "Mannuthy"): 18,
    ("Kunnamkulam", "Guruvayur"): 8,
    ("Kunnamkulam", "Kodungallur"): 18,
    ("Kunnamkulam", "Chavakkad"): 10,
    ("Kunnamkulam", "Wadakkanchery"): 12,
    ("Kunnamkulam", "Mala"): 13,
    ("Kunnamkulam", "Pavaratty"): 10,
    ("Kunnamkulam", "Kaipamangalam"): 10,
    ("Kunnamkulam", "Mannuthy"): 14,
    ("Guruvayur", "Kodungallur"): 12,
    ("Guruvayur", "Chavakkad"): 6,
    ("Guruvayur", "Wadakkanchery"): 20,
    ("Guruvayur", "Mala"): 15,
    ("Guruvayur", "Pavaratty"): 18,
    ("Guruvayur", "Kaipamangalam"): 28,
    ("Guruvayur", "Mannuthy"): 22,
    ("Kodungallur", "Chavakkad"): 13,
    ("Kodungallur", "Wadakkanchery"): 23,
    ("Kodungallur", "Mala"): 28,
    ("Kodungallur", "Pavaratty"): 18,
    ("Kodungallur", "Kaipamangalam"): 16,
    ("Kodungallur", "Mannuthy"): 28,
    ("Chavakkad", "Wadakkanchery"): 12,
    ("Chavakkad", "Mala"): 18,
    ("Chavakkad", "Pavaratty"): 12,
    ("Chavakkad", "Kaipamangalam"): 15,
    ("Chavakkad", "Mannuthy"): 16,
    ("Wadakkanchery", "Mala"): 12,
    ("Wadakkanchery", "Pavaratty"): 14,
    ("Wadakkanchery", "Kaipamangalam"): 20,
    ("Wadakkanchery", "Mannuthy"): 7,
    ("Mala", "Pavaratty"): 9,
    ("Mala", "Kaipamangalam"): 15,
    ("Mala", "Mannuthy"): 13,
    ("Pavaratty", "Kaipamangalam"): 10,
    ("Pavaratty", "Mannuthy"): 9,
    ("Kaipamangalam", "Mannuthy"): 17
}

def calculate_fare(distance):
    base_fare = 10
    if distance <= 5:
        return base_fare
    return base_fare + (distance - 5) * 2

for start in locations:
    for end in locations:
        if start != end:  # Ensure no route is from the same location to the same location
            # Fetch or calculate the distance
            distance = distance_map.get((start, end)) or distance_map.get((end, start))
            
            if distance:  # If we have a valid distance
                fare = calculate_fare(distance)
                route_name = f"Route from {start} to {end}"
                
                # Create a new BusRoute object and save it
                BusRoute.objects.create(
                    route_name=route_name,
                    start_point=start,
                    end_point=end,
                    fare=fare,
                )

print("Routes have been successfully saved.")