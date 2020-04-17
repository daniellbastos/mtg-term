from mtg_term.constants import VALID_COLORS
from mtg_term.exceptions import InvalidColorError


def _validate_color(color, raise_exception=False):
    validated_color = color in VALID_COLORS
    if raise_exception and not validated_color:
        raise InvalidColorError(f'"{color}" isn\'t a valid color. The valid colors are: {VALID_COLORS}')

    return validated_color
