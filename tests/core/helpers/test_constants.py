from backend.core.helpers.constants import SalesCashbackRange


def test_sales_cashback_range_success():
    # Prepare
    sales_value_1 = 300000
    sales_value_2 = 1500
    sales_value_3 = 1499
    sales_value_4 = 1000
    sales_value_5 = 999
    sales_value_6 = 0

    # Get Cashback percentual
    cashback_range_1 = SalesCashbackRange.get_percentual_by_total_value(sales_value_1)
    cashback_range_2 = SalesCashbackRange.get_percentual_by_total_value(sales_value_2)
    cashback_range_3 = SalesCashbackRange.get_percentual_by_total_value(sales_value_3)
    cashback_range_4 = SalesCashbackRange.get_percentual_by_total_value(sales_value_4)
    cashback_range_5 = SalesCashbackRange.get_percentual_by_total_value(sales_value_5)
    cashback_range_6 = SalesCashbackRange.get_percentual_by_total_value(sales_value_6)

    # Assert

    assert cashback_range_1 == 0.2
    assert cashback_range_2 == 0.2
    assert cashback_range_3 == 0.15
    assert cashback_range_4 == 0.15
    assert cashback_range_5 == 0.1
    assert cashback_range_6 == 0.1
