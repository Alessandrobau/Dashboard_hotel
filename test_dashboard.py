import pandas as pd
import numpy as np
import pytest
import hotel_data

@pytest.fixture
def load_data_from_csv(file_path):
    return pd.read_csv(file_path)

# validar se os tipos do csv estão certos
def test_data_types():
    test_data_types = load_data_from_csv('dados.csv')
    assert test_data_types['hotel'].dtype == 'object'
    assert test_data_types['is_canceled'].dtype == np.int64  # or 'int64' if preferred
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


def test_map_graph():
    expected_columns = ["country", "No of guests"]
    assert list(hotel_data.country_wise_guests.columns) == expected_columns

