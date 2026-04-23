"""
CLI Entry Point for the Binance Futures Testnet Trading Bot.

Uses **Typer** for argument parsing and **Rich** for polished terminal
output (panels, tables, styled error messages).

Usage::

    python cli.py place-order --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.01
    python cli.py place-order --symbol ETHUSDT --side SELL --order-type LIMIT --quantity 0.5 --price 1800.00
"""

import sys

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from bot.logging_config import setup_logging
from bot.orders import place_order

# ── Initialise logging before anything else ──────────────────────────
setup_logging()

# ── Rich console (all output goes through this) ─────────────────────
console = Console()

# ── Typer application ────────────────────────────────────────────────
app = typer.Typer(
    name="trading-bot",
    help="Binance Futures Testnet Trading Bot — place orders from the command line.",
    add_completion=False,
    no_args_is_help=True,
)


def _banner() -> None:
    """Print a startup banner via Rich."""
    banner_text = Text()
    banner_text.append("Binance Futures Testnet Trading Bot", style="bold cyan")
    banner_text.append("  v1.0.0", style="dim")
    console.print(
        Panel(
            banner_text,
            border_style="bright_blue",
            padding=(0, 2),
        )
    )


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """Show the startup banner on every invocation."""
    _banner()


# ── place-order command ──────────────────────────────────────────────
@app.command("place-order")
def cmd_place_order(
    symbol: str = typer.Option(
        ...,
        "--symbol",
        "-s",
        help="Trading pair symbol (e.g. BTCUSDT).",
    ),
    side: str = typer.Option(
        ...,
        "--side",
        "-S",
        help="Order side: BUY or SELL.",
    ),
    order_type: str = typer.Option(
        ...,
        "--order-type",
        "-t",
        help="Order type: MARKET or LIMIT.",
    ),
    quantity: float = typer.Option(
        ...,
        "--quantity",
        "-q",
        help="Quantity to trade (positive number).",
    ),
    price: float | None = typer.Option(
        None,
        "--price",
        "-p",
        help="Limit price (required for LIMIT orders).",
    ),
) -> None:
    """
    Place an order on Binance Futures Testnet.

    Validates all inputs, submits the order, and displays the result
    in a formatted table.
    """
    # ── Order request summary panel ──────────────────────────────────
    summary_lines = (
        f"[bold]Symbol:[/bold]     {symbol.upper()}\n"
        f"[bold]Side:[/bold]       {side.upper()}\n"
        f"[bold]Type:[/bold]       {order_type.upper()}\n"
        f"[bold]Quantity:[/bold]   {quantity}"
    )
    if price is not None:
        summary_lines += f"\n[bold]Price:[/bold]      {price}"

    console.print(
        Panel(
            summary_lines,
            title="Order Request",
            border_style="yellow",
            padding=(1, 2),
        )
    )

    # ── Place the order ──────────────────────────────────────────────
    try:
        result = place_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
        )
    except ValueError as exc:
        console.print(
            Text(f"[ERROR] Validation failed: {exc}", style="bold red")
        )
        raise typer.Exit(code=1) from exc
    except Exception as exc:
        console.print(
            Text(f"[ERROR] {exc}", style="bold red")
        )
        raise typer.Exit(code=1) from exc

    # ── Success table ────────────────────────────────────────────────
    table = Table(
        title="Order Placed Successfully",
        title_style="bold green",
        border_style="green",
        show_header=True,
        header_style="bold bright_green",
    )
    table.add_column("Field", style="cyan", min_width=14)
    table.add_column("Value", style="white")

    for field, value in result.items():
        table.add_row(field, str(value))

    console.print(table)


# ── Entrypoint ───────────────────────────────────────────────────────
if __name__ == "__main__":
    app()
