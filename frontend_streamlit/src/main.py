import os
from typing import Dict, List, Tuple, Union

import folium
import numpy as np
import pandas as pd
import requests
import streamlit as st
from dotenv import find_dotenv, load_dotenv
from streamlit_folium import folium_static


def extract_routes(response: List[Dict[str, Union[float, str]]]
                   ) -> List[Tuple[float, float, float, float]]:
    routes = list(
        map(lambda node: (node["y1"], node["x1"], node["y2"], node["x2"]), response))
    return routes


def extract_names(response: List[Dict[str, Union[float, str]]]) -> List[str]:
    names = list(map(lambda node: node["name"], response))
    return names


def extract_lengths(
        response: List[Dict[str, Union[float, str]]]) -> List[float]:
    lengths = list(map(lambda node: node["length"], response))
    return lengths


def extract_costs(response: List[Dict[str, Union[float, str]]]) -> List[float]:
    costs = list(map(lambda node: node["cost"], response))
    return costs


def process_response(response: List[Dict[str,
                                         Union[float,
                                               str]]]) -> Tuple[List[Tuple[float,
                                                                           float,
                                                                           float,
                                                                           float]],
                                                                List[str],
                                                                List[float]]:
    routes, names, lengths, costs = extract_routes(response), extract_names(
        response), extract_lengths(response), extract_costs(response)
    return routes, names, lengths, costs


def get_response(max_velocity: int, text1, text2, text3, text4,
                 text5, text6) -> List[Dict[str, Union[float, str]]]:
    # url = "http://localhost:8000/find_route"
    url = os.getenv("API_URL")
    payload = {
        'origin_city': text1,
        'origin_street': text2,
        'origin_house_number': text3,
        'destination_city': text4,
        'destination_street': text5,
        'destination_house_number': text6,
        'max_velocity': max_velocity
    }
    response = requests.post(url, json=payload)
    return response


def extract_edges(*args: List[Tuple[float,
                                    float,
                                    float,
                                    float]]) -> Tuple[float,
                                                      float,
                                                      float,
                                                      float]:
    routes = []
    for route in args:
        routes += route

    routes_x = [pos for route in routes for pos in route[1::2]]
    routes_y = [pos for route in routes for pos in route[0::2]]
    center_x = sum(routes_x) / len(routes_x)
    center_y = sum(routes_y) / len(routes_y)
    return center_x, center_y


def draw_routes(route1, route2, route3) -> None:
    center_x, center_y = extract_edges(route1, route2, route3)
    m = folium.Map(location=[center_y, center_x], zoom_start=10)
    for route in route1:
        folium.PolyLine(
            [(route[0], route[1]), (route[2], route[3])], color='green').add_to(m)

    for route in route2:
        folium.PolyLine([(route[0] +
                          0.001, route[1] +
                          0.001), (route[2] +
                                   0.001, route[3] +
                                   0.001)], color='orange').add_to(m)

    for route in route3:
        folium.PolyLine([(route[0] +
                          0.002, route[1] +
                          0.002), (route[2] +
                                   0.002, route[3] +
                                   0.002)], color='red').add_to(m)

    st.write("Folium map")
    folium_static(m, width=1000)


def get_turn_direction(vec1: Tuple[float,
                                   float,
                                   float,
                                   float],
                       vec2: Tuple[float,
                                   float,
                                   float,
                                   float]) -> str:
    v1 = (vec1[2] - vec1[0], vec1[3] - vec1[1])
    v2 = (vec2[2] - vec2[0], vec2[3] - vec2[1])

    cross_product = v1[0] * v2[0] - v1[1] * v2[1]

    if cross_product > 0:
        return "turn left"

    elif cross_product < 0:
        return "turn right"
    else:
        return "go straight"


def handle_buttom_pressed(
        slider1,
        slider2,
        slider3,
        text1,
        text2,
        text3,
        text4,
        text5,
        text6):

    response1 = get_response(slider1, text1, text2, text3, text4, text5, text6)
    if response1.status_code == 404:
        st.warning("Could not find route")
        return
    routes1, names1, lengths1, costs1 = process_response(response1.json())

    response2 = get_response(slider2, text1, text2, text3, text4, text5, text6)
    if response2.status_code == 404:
        st.warning("Could not find route")
        return
    routes2, names2, lengths2, costs2 = process_response(response2.json())

    response3 = get_response(slider3, text1, text2, text3, text4, text5, text6)
    if response3.status_code == 404:
        st.warning("Could not find route")
        return
    routes3, names3, lengths3, costs3 = process_response(response3.json())

    draw_routes(routes1, routes2, routes3)

    return (routes1, names1, lengths1, costs1), (routes2, names2,
                                                 lengths2, costs2), (routes3, names3, lengths3, costs3)


def main_bar():
    text1 = st.text_input('Starting city: ', value='Opole')
    text2 = st.text_input('Starting street: ', value='Kupiecka')
    text3 = st.text_input('Starting house number: ', value='1')
    text4 = st.text_input('Destination city: ', value='Nysa')
    text5 = st.text_input('Destination street: ', value='Bracka')
    text6 = st.text_input('Destination house number: ', value='2')

    slider1 = st.slider(
        ":green[max speed for route 1]",
        min_value=0,
        max_value=250,
        value=20)
    slider2 = st.slider(
        ":orange[max speed for route 2]",
        min_value=0,
        max_value=250,
        value=60)
    slider3 = st.slider(
        ":red[max speed for route 3]",
        min_value=0,
        max_value=250,
        value=250)

    data1 = ()
    data2 = ()
    data3 = ()

    if st.button('Update Routes'):
        data1, data2, data3 = handle_buttom_pressed(
            slider1, slider2, slider3, text1, text2, text3, text4, text5, text6)
    return data1, data2, data3, slider1, slider2, slider3


def display_markdow(text: str) -> None:
    st.markdown(
        f'<p style="font-size:24px;font-weight:bold;color:#3366ff">{text}</p>',
        unsafe_allow_html=True)


def display_route_parameters(
        name: str,
        lengths: List[float],
        costs: List[float],
        vel: float):
    st.title(f"{name}")
    st.write(f"Vehicule maximum velocity : {vel} km/h")
    st.write(f"Total length: {round(sum(lengths)*100, 2)} km")
    st.write(f"Expected time: {round(sum(costs)*100, 2)} h")


def display_route_table(data, title: str) -> None:
    routes, names, lengths, costs = data
    x1 = list(map(lambda x: x[0], routes))
    y1 = list(map(lambda x: x[1], routes))
    x2 = list(map(lambda x: x[2], routes))
    y2 = list(map(lambda x: x[3], routes))
    lengths = list(map(lambda x: x * 100 * 1000, lengths))
    durations = list(map(lambda x: round(x * 60 * 100, 3), costs))
    directions = [""] + [get_turn_direction(routes[turn_index], routes[turn_index + 1])
                         for turn_index in range(len(routes) - 1)]
    df = pd.DataFrame({
        "X1": x1,
        "Y1": y1,
        "X2": x2,
        "Y2": y2,
        "Length [m]": lengths,
        "Duration [min]": durations,
        "Turn direction": directions
    })
    with st.expander(title):
        st.table(df)


def side_bar(data1, data2, data3, vel1, vel2, vel3):
    if data1:
        display_route_parameters("Route 1", data1[2], data1[3], vel1)

    if data2:
        display_route_parameters("Route 2", data2[2], data2[3], vel2)

    if data3:
        display_route_parameters("Route 3", data3[2], data3[3], vel3)

    if data1:
        display_route_table(data1, "Route 1")
    if data2:
        display_route_table(data2, "Route 2")
    if data3:
        display_route_table(data3, "Route 3")


def main():
    col1, col2 = st.columns([1, 2])

    with col2:
        data1, data2, data3, vel1, vel2, vel3 = main_bar()
    with col1:
        side_bar(data1, data2, data3, vel1, vel2, vel3)


if __name__ == '__main__':

    env_file = find_dotenv()

    if env_file:
        load_dotenv(env_file)

    st.set_page_config(
        page_title='Map with Routes',
        page_icon=':earth_americas:',
        layout='wide')
    main()
