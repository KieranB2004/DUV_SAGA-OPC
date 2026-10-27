# layout_io.py generated with assistance from CHATGPT Tuesday October 27th 2026.
# CHATGPT contribution: designed the load_gdsii() interface, path validation,
# file-extension checks, KLayout loading workflow, top-level-cell validation,
# exception handling, documentation, and initial test procedure.
# Developer responsibility: review, understand, test, and validate this code.

"""Load and validate GDSII layout files for the DUV OPC simulator."""

# Import Path to handle file paths consistently across operating systems.
from pathlib import Path

# Import KLayout's database API for reading GDSII files and accessing cells.
import klayout.db as kdb


def load_gdsii(path: str | Path) -> tuple[kdb.Layout, kdb.Cell]:
    """Load a GDSII file and return its layout and top-level cell.

    Args:
        path: Filesystem path to the input GDSII file.

    Returns:
        A tuple containing:
            - The loaded KLayout Layout object.
            - The single top-level Cell object.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the extension or cell hierarchy is invalid.
        RuntimeError: If KLayout cannot read the file.
    """

    # Convert strings and Path objects into one consistent path representation.
    # Expand "~" so that home-directory paths work on macOS and Linux.
    layout_path = Path(path).expanduser()

    # Reject missing files and directories before attempting to load the layout.
    if not layout_path.is_file():
        raise FileNotFoundError(
            f"GDSII file does not exist or is not a file: {layout_path}"
        )

    # Accept GDSII files with either of the two supported extensions.
    if layout_path.suffix.lower() not in {".gds", ".gdsii"}:
        raise ValueError(
            f"Unsupported file extension: {layout_path.suffix}"
        )

    # Create an empty KLayout database to store the imported design.
    layout = kdb.Layout()

    # Ask KLayout to read the specified file into the database.
    # Add filename context if the external library reports a loading error.
    try:
        layout.read(str(layout_path))
    except Exception as exc:
        raise RuntimeError(
            f"KLayout failed to read the layout: {layout_path}"
        ) from exc

    # Identify cells that do not have a parent in the layout hierarchy.
    # The project specification requires exactly one top-level cell.
    top_cells = list(layout.top_cells())

    # Reject an empty layout that contains no top-level cell.
    if len(top_cells) == 0:
        raise ValueError(
            f"The layout contains no top-level cell: {layout_path}"
        )

    # Reject ambiguous layouts instead of silently choosing one cell.
    if len(top_cells) != 1:
        raise ValueError(
            f"Expected exactly one top-level cell, "
            f"but found {len(top_cells)} in {layout_path}"
        )

    # Return the database and cell so that later modules can inspect both
    # the layout metadata and the geometry contained in the selected cell.
    return layout, top_cells[0]