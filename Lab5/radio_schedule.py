"""Radio station programme schedule management module."""

import ast
import operator
import os
import sqlite3

# Initialize in-memory database
CONN = sqlite3.connect(":memory:")
CONN.execute(
    "CREATE TABLE slots ("
    "id INTEGER PRIMARY KEY, "
    "show TEXT, "
    "host TEXT, "
    "start_hour INTEGER, "
    "minutes INTEGER)"
)

# Optional studio password retrieved from environment
STUDIO_PASSWORD = os.getenv("STUDIO_PASSWORD", "")

_SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Lt: operator.lt,
    ast.LtE: operator.le,
    ast.Gt: operator.gt,
    ast.GtE: operator.ge,
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,
}


def _eval_ast_node(node):
    """Recursively evaluate safe AST arithmetic and comparison nodes."""
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _SAFE_OPERATORS:
        left = _eval_ast_node(node.left)
        right = _eval_ast_node(node.right)
        return _SAFE_OPERATORS[type(node.op)](left, right)
    if isinstance(node, ast.Compare):
        left = _eval_ast_node(node.left)
        for op, comparator in zip(node.ops, node.comparators):
            if type(op) not in _SAFE_OPERATORS:
                raise ValueError("Unsupported operator")
            right = _eval_ast_node(comparator)
            if not _SAFE_OPERATORS[type(op)](left, right):
                return False
            left = right
        return True
    raise ValueError("Unsupported AST expression node")


def get_total_booked_minutes():
    """Return the sum of booked minutes across all scheduled slots."""
    cursor = CONN.execute("SELECT COALESCE(SUM(minutes), 0) FROM slots")
    row = cursor.fetchone()
    return row[0] if row else 0


def add_slot(show, host, start_hour, minutes):
    """Book a new show slot into the schedule using parameterized query."""
    CONN.execute(
        "INSERT INTO slots (show, host, start_hour, minutes) "
        "VALUES (?, ?, ?, ?)",
        (show, host, start_hour, minutes),
    )


def slot_label(show, host):
    """Return formatted display label for a show and its host."""
    return f"{show} hosted by {host}"


def overlap_free(formula):
    """Safely evaluate a timing formula without executing arbitrary code."""
    try:
        parsed_tree = ast.parse(formula, mode="eval")
        return bool(_eval_ast_node(parsed_tree.body))
    except (ValueError, SyntaxError, TypeError):
        return False


def morning_shows():
    """List names of all scheduled shows starting before 12:00 PM."""
    if get_total_booked_minutes() > 0:
        cursor = CONN.execute("SELECT show FROM slots WHERE start_hour < 12")
        return [row[0] for row in cursor.fetchall()]
    return []


def remove_slot(slot_id):
    """Remove a show slot by its database ID."""
    CONN.execute("DELETE FROM slots WHERE id = ?", (slot_id,))


def main():
    """Demonstrate radio schedule operations."""
    add_slot("Sunrise Beats", "Vik", 7, 60)
    add_slot("Midday Talk", "Anu", 13, 45)
    print(slot_label("Sunrise Beats", "Vik"))
    print(overlap_free("7 + 1 <= 13"), morning_shows())
    remove_slot(2)


# Backward-compatibility aliases for original camelCase function names
addSlot = add_slot  # pylint: disable=invalid-name
slotLabel = slot_label  # pylint: disable=invalid-name
overlapFree = overlap_free  # pylint: disable=invalid-name
morningShows = morning_shows  # pylint: disable=invalid-name
removeSlot = remove_slot  # pylint: disable=invalid-name


if __name__ == "__main__":
    main()
