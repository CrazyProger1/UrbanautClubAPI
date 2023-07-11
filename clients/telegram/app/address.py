from .models import City, Country


def get_address(street_number: str, street: str, city: City, country: Country, ) -> str:
    address = []

    if street_number and street:
        address.append(street_number)
        address.append(street)
    elif street:
        address.append(street)

    if city:
        address.append(city.display_name)
    else:
        address.append(country.name)

    return ', '.join(address)
