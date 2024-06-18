import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno

import warnings

warnings.filterwarnings("ignore")

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from xgboost import XGBClassifier

# from catboost import CatBoostClassifier
from sklearn.ensemble import ExtraTreesClassifier
from lightgbm import LGBMClassifier
from sklearn.ensemble import VotingClassifier

import folium
from folium.plugins import HeatMap
import plotly.express as px

plt.style.use("fivethirtyeight")
# %matplotlib inline
pd.set_option("display.max_columns", 32)

df = pd.read_csv("dados.csv")

# remove valores nulos na tabela
null = pd.DataFrame(
    {
        "Null Values": df.isna().sum(),
        "Percentage Null Values": (df.isna().sum()) / (df.shape[0]) * (100),
    }
)
df.fillna(0, inplace=True)

# filtra valores nulos
filter = (df.children == 0) & (df.adults == 0) & (df.babies == 0)
df = df[~filter]


# definir de onde os clientes vem
country_wise_guests = df[df["is_canceled"] == 0]["country"].value_counts().reset_index()
country_wise_guests.columns = ["country", "No of guests"]
basemap = folium.Map()
guests_map = px.choropleth(
    country_wise_guests,
    locations=country_wise_guests["country"],
    color=country_wise_guests["No of guests"],
    hover_name=country_wise_guests["country"],
)

guests_map.update_layout(
    paper_bgcolor="black", plot_bgcolor="black", geo=dict(bgcolor="black")
)

# quanto é pago por tipo de hotel
data = df[df["is_canceled"] == 0]
hotel_price = px.box(
    data_frame=data,
    x="reserved_room_type",
    y="adr",
    color="hotel",
    template="plotly_dark",
)


# Variação dos preços
data_resort = df[(df["hotel"] == "Resort Hotel") & (df["is_canceled"] == 0)]
data_city = df[(df["hotel"] == "City Hotel") & (df["is_canceled"] == 0)]
resort_hotel = data_resort.groupby(["arrival_date_month"])["adr"].mean().reset_index()
city_hotel = data_city.groupby(["arrival_date_month"])["adr"].mean().reset_index()
final_hotel = resort_hotel.merge(city_hotel, on="arrival_date_month")
final_hotel.columns = ["month", "price_for_resort", "price_for_city_hotel"]

import sort_dataframeby_monthorweek as sd


def sort_month(df, column_name):
    return sd.Sort_Dataframeby_Month(df, column_name)


final_prices = sort_month(final_hotel, "month")
plt.figure(figsize=(17, 8))

price_variation = px.line(
    final_prices,
    x="month",
    y=["price_for_resort", "price_for_city_hotel"],
    title="Room price per night over the Months",
    template="plotly_dark",
)

# meses mais movimentados
resort_guests = data_resort["arrival_date_month"].value_counts().reset_index()
resort_guests.columns = ["month", "no of guests"]
city_guests = data_city["arrival_date_month"].value_counts().reset_index()
city_guests.columns = ["month", "no of guests"]
final_guests = resort_guests.merge(city_guests, on="month")
final_guests.columns = ["month", "no of guests in resort", "no of guest in city hotel"]
final_guests = sort_month(final_guests, "month")

total_guests_month = px.line(
    final_guests,
    x="month",
    y=["no of guests in resort", "no of guest in city hotel"],
    title="Total no of guests per Months",
    template="plotly_dark",
)

# tempo de estadia
filter = df["is_canceled"] == 0
data = df[filter]
data["total_nights"] = data["stays_in_weekend_nights"] + data["stays_in_week_nights"]
stay = data.groupby(["total_nights", "hotel"]).agg("count").reset_index()
stay = stay.iloc[:, :3]
stay = stay.rename(columns={"is_canceled": "Number of stays"})
tempo_estadia = px.bar(
    data_frame=stay,
    x="total_nights",
    y="Number of stays",
    color="hotel",
    barmode="group",
    template="plotly_dark",
)
