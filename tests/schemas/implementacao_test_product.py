from pydantic import ValidationError
import pytest
from store.schemas.product import ProductIn
from tests.factories import product_data

# Função de teste para validar dados corretos
def test_schemas_return_success() -> None:
    """
    Testa se a validação do schema retorna sucesso com dados válidos.
    """
    data = product_data()
    product = ProductIn.model_validate(data)

    assert product.name == "Iphone 14 Pro Max"

# Função de teste para validar erro de dados faltantes
def test_schemas_return_raise() -> None:
    """
    Testa se a validação do schema levanta um erro com dados inválidos.
    """
    data = {"name": "Iphone 14 Pro Max", "quantity": 10, "price": 8.5}

    with pytest.raises(ValidationError) as err:
        ProductIn.model_validate(data)

    assert_error_missing_status(err, data)

# Função auxiliar para verificar a mensagem de erro esperada
def assert_error_missing_status(err: ValidationError, data: dict) -> None:
    """
    Verifica se o erro levantado é devido ao campo 'status' ausente.
    """
    expected_error = {
        "type": "missing",
        "loc": ("status",),
        "msg": "Field required",
        "input": data,
        "url": "https://errors.pydantic.dev/2.5/v/missing",
    }
    assert err.value.errors()[0] == expected_error

# Fixture para dados de teste válidos
@pytest.fixture
def valid_product_data() -> dict:
    return product_data()

# Fixture para dados de teste inválidos
@pytest.fixture
def invalid_product_data() -> dict:
    return {"name": "Iphone 14 Pro Max", "quantity": 10, "price": 8.5}

# Função de teste utilizando fixtures
def test_schemas_with_fixtures(valid_product_data: dict, invalid_product_data: dict) -> None:
    product = ProductIn.model_validate(valid_product_data)
    assert product.name == "Iphone 14 Pro Max"

    with pytest.raises(ValidationError) as err:
        ProductIn.model_validate(invalid_product_data)

    assert_error_missing_status(err, invalid_product_data)