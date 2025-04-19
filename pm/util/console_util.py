import subprocess
from enum import Enum

from typing import Tuple, List, Optional, Callable


class TextStyle(Enum):
    """
    Represents various ANSI text styles for terminal output.

    Attributes:
        NORMAL: Default terminal style.
        BOLD: Bold text.
        RED_FG: Red foreground text.
        GREEN_FG: Green foreground text.
        YELLOW_FG: Yellow foreground text.
        BLUE_FG: Blue foreground text.
        CYAN_FG: Cyan foreground text.
        RED_BG: Red background color.
        GREEN_BG: Green background color.
        YELLOW_BG: Yellow background color.
        BLUE_BG: Blue background color.
        CYAN_BG: Cyan background color.
    """
    NORMAL = "normal"
    BOLD = "bold"
    RED_FG = "red_fg"
    GREEN_FG = "green_fg"
    YELLOW_FG = "yellow_fg"
    BLUE_FG = "blue_fg"
    CYAN_FG = "cyan_fg"
    RED_BG = "red_bg"
    GREEN_BG = "green_bg"
    YELLOW_BG = "yellow_bg"
    BLUE_BG = "blue_bg"
    CYAN_BG = "cyan_bg"


STYLE_MAP = {
    TextStyle.NORMAL: "\033[0m", TextStyle.BOLD: "\033[1m",
    TextStyle.RED_FG: "\033[31m", TextStyle.GREEN_FG: "\033[32m",
    TextStyle.YELLOW_FG: "\033[33m", TextStyle.BLUE_FG: "\033[34m",
    TextStyle.CYAN_FG: "\033[36m", TextStyle.RED_BG: "\033[41m",
    TextStyle.GREEN_BG: "\033[42m", TextStyle.YELLOW_BG: "\033[43m",
    TextStyle.BLUE_BG: "\033[44m", TextStyle.CYAN_BG: "\033[46m"
}


def display_table_in_less_with_ansi(
        header: Tuple[str, ...],
        rows: List[Tuple[str, ...]],
        renderers: Optional[List[Optional[Callable[[str], List[TextStyle]]]]] = None
) -> None:
    """
    Displays a formatted table in a paginated terminal view using 'less' with ANSI styles.

    Args:
        header (Tuple[str, ...]): Column headers for the table.
        rows (List[Tuple[str, ...]]): List of row entries for the table.
        renderers (Optional[List[Optional[Callable[[str], List[TextStyle]]]]]): 
            Optional list of rendering functions that apply text styles to individual cell content.
    """
    table = create_table(header=header, rows=rows, renderers=renderers)
    subprocess.run(["less", "-S", "-R"], input=table.encode("utf-8"))


def create_table(
        header: Tuple[str, ...],
        rows: List[Tuple[str, ...]],
        renderers: Optional[List[Optional[Callable[[str], List[TextStyle]]]]] = None
) -> str:
    """
    Constructs an ANSI-styled table string from the given headers and rows.

    Args:
        header (Tuple[str, ...]): Column headers for the table.
        rows (List[Tuple[str, ...]]): List of row entries for the table.
        renderers (Optional[List[Optional[Callable[[str], List[TextStyle]]]]]): 
            Optional list of rendering functions that apply styles to each cell.

    Returns:
        str: The rendered table as a single string.
    """
    column_widths = [max(len(str(item)) for item in column) for column in zip(header, *rows)]

    top_border    = "┌" + "┬".join("─" * (width + 2) for width in column_widths) + "┐"
    middle_border = "├" + "┼".join("─" * (width + 2) for width in column_widths) + "┤"
    bottom_border = "└" + "┴".join("─" * (width + 2) for width in column_widths) + "┘"

    table_content = [top_border]
    table_content.append(format_row(header, column_widths, renderers, True))
    table_content.append(middle_border)
    for row in rows:
        table_content.append(format_row(row, column_widths, renderers))
    table_content.append(bottom_border)

    return "\n".join(table_content)


def default_renderer(item: str) -> List[TextStyle]:
    """
    Default renderer that applies no additional styling to the text.

    Args:
        item (str): The string to render.

    Returns:
        List[TextStyle]: List containing a single `TextStyle.NORMAL` entry.
    """
    return [TextStyle.NORMAL]


def format_row(table_row, column_widths, renderers, is_header=False):
    """
    Formats a single table row with the appropriate width and text styles.

    Args:
        table_row (Tuple[str, ...]): A row of values to format.
        column_widths (List[int]): List of column widths.
        renderers (Optional[List[Callable[[str], List[TextStyle]]]]): 
            Functions to apply text styles to each cell.
        is_header (bool): Whether the row is a header row.

    Returns:
        str: Formatted and styled row string.
    """
    formatted_cells = []
    for idx, (item, width) in enumerate(zip(table_row, column_widths)):
        item = str(item)
        if is_header:
            styled_item = apply_styles(item.ljust(width),[TextStyle.BOLD])  # Bold header
        else:
            renderer = renderers[idx] if renderers and idx < len(renderers) and renderers[idx] else default_renderer
            if renderer is None:
                renderer = default_renderer
            styles = renderer(item)
            styled_item = apply_styles(item.ljust(width), styles)
        formatted_cells.append(styled_item)

    formatted_row = "│ " + " │ ".join(formatted_cells) + " │"
    return formatted_row


def apply_styles(text: str, styles: List[TextStyle]) -> str:
    """
    Applies a list of ANSI styles to a given text.

    Args:
        text (str): The text to be styled.
        styles (List[TextStyle]): List of styles to apply.

    Returns:
        str: The styled string with ANSI codes.
    """
    style_sequence = ''.join(STYLE_MAP[style] for style in styles)
    return f"{style_sequence}{text}{STYLE_MAP[TextStyle.NORMAL]}"
