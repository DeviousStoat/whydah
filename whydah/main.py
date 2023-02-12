import click
from gargle.maybe import Some, as_maybe
from gargle.result import Result

from whydah.api import data_search, data_top_100
from whydah.models import Category, PirateTorrent


@click.group()
def main() -> None:
    ...


@main.command()
def list_categories() -> None:
    click.echo("\n".join(str(cat) for cat in Category))


@main.command()
@click.argument("category")
def top_100(category: str) -> None:
    maybe_category(category).and_then(lambda cat: data_top_100(cat)).either(
        display_torrents, display_error
    )


@main.command()
@click.argument("search_term")
@click.option("-c", "--category")
def search(search_term: str, category: str | None = None) -> None:
    maybe_category(category).and_then(lambda cat: data_search(search_term, cat)).either(
        display_torrents, display_error
    )


def maybe_category(category: str | None) -> Result[Category, str]:
    return (
        as_maybe(category)
        .map_or(Category.from_name, default=Some(Category.NONE))
        .ok_or(
            f"no matching category found for '{category}',"
            " use `list-category` command to see the list of available categories"
        )
    )


def display_torrents(torrents: list[PirateTorrent]) -> None:
    click.echo("\n".join(t.format() for t in torrents))


def display_error(err: str) -> None:
    click.echo(click.style(err, fg="red"), err=True)


if __name__ == "__main__":
    raise SystemExit(main())
