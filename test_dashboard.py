import pandas as pd
import numpy as np
import pytest
import hotel_data
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

@pytest.fixture(name='my_data')
def my_data():    
    return pd.read_csv('dados.csv')

def my_dataframe():
    return hotel_data.df

# verificar se o dataframe não está vazio
def test_read_csv():
    assert not my_dataframe().empty
    assert len(my_dataframe()) > 0
    assert len(my_dataframe().columns) > 0

# validar se os tipos do csv estão certos
def test_data_types(my_data):
    test_data_types = my_data
    assert test_data_types['hotel'].dtype == 'object'
    assert test_data_types['is_canceled'].dtype == np.int64  
    assert test_data_types['lead_time'].dtype == np.int64
    assert test_data_types['arrival_date_year'].dtype == np.int64
    assert test_data_types['arrival_date_month'].dtype == 'object'
    assert test_data_types['arrival_date_week_number'].dtype == np.int64
    assert test_data_types['arrival_date_day_of_month'].dtype == np.int64
    assert test_data_types['stays_in_weekend_nights'].dtype == np.int64
    assert test_data_types['stays_in_week_nights'].dtype == np.int64
    assert test_data_types['adults'].dtype == np.int64
    assert test_data_types['children'].dtype == np.float64
    assert test_data_types['babies'].dtype == np.int64
    assert test_data_types['meal'].dtype == 'object'
    assert test_data_types['country'].dtype == 'object'
    assert test_data_types['market_segment'].dtype == 'object'
    assert test_data_types['distribution_channel'].dtype == 'object'
    assert test_data_types['is_repeated_guest'].dtype == np.int64
    assert test_data_types['previous_cancellations'].dtype == np.int64
    assert test_data_types['previous_bookings_not_canceled'].dtype == np.int64
    assert test_data_types['reserved_room_type'].dtype == 'object'
    assert test_data_types['assigned_room_type'].dtype == 'object'
    assert test_data_types['booking_changes'].dtype == np.int64
    assert test_data_types['deposit_type'].dtype == 'object'
    assert test_data_types['agent'].dtype == np.float64
    assert test_data_types['company'].dtype == np.float64
    assert test_data_types['days_in_waiting_list'].dtype == np.int64
    assert test_data_types['customer_type'].dtype == 'object'
    assert test_data_types['adr'].dtype == np.float64
    assert test_data_types['required_car_parking_spaces'].dtype == np.int64
    assert test_data_types['total_of_special_requests'].dtype == np.int64
    assert test_data_types['reservation_status'].dtype == 'object'
    assert test_data_types['reservation_status_date'].dtype == 'object'

# validar se a função de remover nulos esta realmente removendo os nulos
def test_remove_null_values():
    dataframe = my_dataframe()
    dataframe.fillna(0, inplace=True)
    assert not dataframe.isna().sum().any()

# teste se as colunas usadas no gráfico de mapas são as colunas corretas
def test_country_wise_guests():
    expected_columns = ["country", "No of guests"]
    assert list(hotel_data.country_wise_guests.columns) == expected_columns

# testar se o merge entre os dados esta ocorrendo corretamente
def test_data_merging():
    hotel_data.data_resort = my_dataframe()[(my_dataframe()['hotel'] == 'Resort Hotel') & (my_dataframe()['is_canceled'] == 0)]
    hotel_data.data_city = my_dataframe()[(my_dataframe()['hotel'] == 'City Hotel') & (my_dataframe()['is_canceled'] == 0)]
    hotel_data.resort_hotel = hotel_data.data_resort.groupby(['arrival_date_month'])['adr'].mean().reset_index()
    hotel_data.city_hotel = hotel_data.data_city.groupby(['arrival_date_month'])['adr'].mean().reset_index()
    hotel_data.final_hotel = hotel_data.resort_hotel.merge(hotel_data.city_hotel, on='arrival_date_month')
    assert not hotel_data.final_hotel.empty
    assert 'arrival_date_month' in hotel_data.final_hotel.columns

# testar se a filtragem está correta
def test_filtering(my_data):
    df_test = my_data.copy()
    filter_condition =  (df_test.children == 0) & (df_test.adults == 0) & (df_test.babies == 0)
    filtered_df = df_test[~filter_condition]
    assert len(filtered_df) == len(my_dataframe())
