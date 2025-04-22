from models.address import Address


def test_address_str():
    address = Address("5 rue des fleurs", "Toulouse", 31000)

    expected_value = "5 rue des fleurs, 31000 Toulouse"

    assert str(address) == expected_value
