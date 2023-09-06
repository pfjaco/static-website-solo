"""Build static HTML site from directory of HTML templates and plain files."""
import click
import pathlib

@click.command()
@click.option('--output','-o', help="Output directory.", is_flag=True)
@click.option('--verbose','-v', help="Print more output.", metavar="PATH")
@click.argument("input_dir", nargs=1, type=click.Path(exists=True))
def main(input_dir,output,verbose):
    input_dir = pathlib.Path(input_dir)
    print(f"DEBUG input_dir={input_dir}")

if __name__ == "__main__":
    main()