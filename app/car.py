from app.open_json import config_json
from app.product_calculation import product_calculation


def trip_price(customer,
               shops,
               count_milk,
               count_bread,
               count_butter):

    global result_shop

    """
    dictionary with distances (value - store name )
    to the store (key - distance) and back home
    """
    distance_to_the_store = {}
    for i in range(len(shops)):
        point_x = ((customer["location"][0] - shops[i]["location"][0]) ** 2)
        point_y = ((customer["location"][1] - shops[i]["location"][1]) ** 2)
        result = round((point_x + point_y) ** 0.5, 2)
        distance_to_the_store[f'distance_to_the_{shops[i]["name"]}'] \
            = result * 2

    """
    Dictionary with store name (key) and fuel price (value)
    """
    fare = {}
    for i in range(len(shops)):
        fuel_consumption = customer["car"]["fuel_consumption"]
        distance = distance_to_the_store[f'distance_to_the_{shops[i]["name"]}']
        fuel_price = config_json["FUEL_PRICE"]
        rounding = round(((fuel_consumption * distance) / 100) * fuel_price, 3)

        fare[f'fare_to_the_{shops[i]["name"]}'] = rounding

    """
    Printing the amount of money a person has
    """
    print(f'{customer["name"]} has {customer["money"]} dollars')

    """
    Calculation of purchase costs in different shops with a driveway
    """
    temp_dict = {}
    for i in range(len(shops)):
        cost = product_calculation(count_milk,
                                   count_bread,
                                   count_butter,
                                   shops[i])

        cost_plus_fuel = fare[f'fare_to_the_{shops[i]["name"]}'] + cost

        temp_dict[f'{shops[i]["name"]}'] = round(cost_plus_fuel, 2)

        print(f'{customer["name"]}`s trip to the {shops[i]["name"]} '
              f'costs {round(cost_plus_fuel, 2)}')

    """
    Choosing a store at a lower price and the amount of money a person has
    """
    temp_list = []
    for value in temp_dict.values():
        temp_list.append(value)

    for key, value in temp_dict.items():
        if value == min(temp_list):
            result_shop = key

    if min(temp_list) < customer["money"]:
        print(f'{customer["name"]} rides to {result_shop}\n')

        """
        The function returns the selected store
        """
        select_shop = {}
        for i in range(len(shops)):
            select_shop[shops[i]["name"]] = i

        for key, value in select_shop.items():
            if key == result_shop:
                return [shops[value], min(temp_list)]
    else:
        print(f'{customer["name"]} doesn`t have enough money '
              f'to make purchase in any shop\n')