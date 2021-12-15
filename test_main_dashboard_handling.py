from main_dashboard_handling import formatted_news_API_data
from main_dashboard_handling import local_7day_infections



def test_formatted_news_API_data():
    data = formatted_news_API_data()
    assert isinstance(data, list)

def test_local_7day_infections():
    data = local_7day_infections()
    assert isinstance(data, int)
    
if __name__ == '__main__':
    test1 = test_formatted_news_API_data()
    test2 = test_local_7day_infections()