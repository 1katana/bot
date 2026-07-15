

def lamports_to_sol(lamports: int) -> float:
    """
    Конвертирует лампорты в SOL.

    :param lamports: Количество лампортов.
    :return: Количество SOL.
    """
    return lamports / 1_000_000_000

def sol_to_lamports(sol: float) -> int:
    """
    Конвертирует SOL в лампорты.

    :param sol: Количество SOL.
    :return: Количество лампортов.
    """
    return int(sol * 1_000_000_000)

def token_units_to_amount(units: int, decimals: int) -> float:
    """
    Конвертирует наименьшие единицы токена в целые единицы токена.

    :param units: Количество наименьших единиц токена.
    :param decimals: Количество децимальных мест для токена.
    :return: Количество целых единиц токена.
    """
    return units / (10 ** decimals)

def amount_to_token_units(amount: float, decimals: int) -> int:
    """
    Конвертирует целые единицы токена в наименьшие единицы токена.

    :param amount: Количество целых единиц токена.
    :param decimals: Количество децимальных мест для токена.
    :return: Количество наименьших единиц токена.
    """
    return int(amount * (10 ** decimals))