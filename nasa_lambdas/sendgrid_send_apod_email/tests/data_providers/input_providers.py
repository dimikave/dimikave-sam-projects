def greeting_provider() -> list[list[int | str]]:
    """
    Data provider with sample greetings.
    """
    return [
        # Example greeting for day 1
        [1, "Hello, Earth!"],
        # Example greeting for day 2
        [2, "Hi from beyond!"],
        # Example greeting for day 3
        [3, "Greetings from space!"],
        # Example greeting for day 11
        [11, "Hi from beyond!"],
        # Example greeting for day 12
        [12, "Greetings from space!"],
    ]


def title_extraction_provider() -> list[list[dict[str, str] | str]]:
    """
    Data provider with sample NASA APOD responses.
    """
    return [
        [{"title": "A Beautiful Galaxy"}, "A Beautiful Galaxy"],
        [{"title": "Stellar Nebula"}, "Stellar Nebula"],
    ]


def url_extraction_provider() -> list[list[dict[str, str] | str]]:
    """
    Data provider with sample NASA APOD responses.
    """
    return [
        [{"url": "https://example.com/image1.jpg"}, "https://example.com/image1.jpg"],
        [{"url": "https://example.com/image2.jpg"}, "https://example.com/image2.jpg"],
    ]


def explanation_extraction_provider() -> list[list[dict[str, str] | str]]:
    """
    Data provider for get_explanation function with sample NASA APOD responses.
    """
    return [
        [{"explanation": "A fascinating galaxy far away."}, "A fascinating galaxy far away."],
        [{"explanation": "This nebula is a stellar nursery."}, "This nebula is a stellar nursery."],
    ]
