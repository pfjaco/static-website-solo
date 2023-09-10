"""Build static HTML site from directory of HTML templates and plain files."""

import pathlib
import os
import json
import shutil
import jinja2
import click


@click.command()
@click.option('--output', '-o', help="Output directory.",
              metavar="PATH", default=None)
@click.option('--verbose', '-v', help="Print more output.", is_flag=True)
@click.argument("input_dir", nargs=1, type=click.Path(exists=True))
def main(input_dir, output, verbose):
    """Templated static website generator."""
    file_read = load_json(input_dir)
    for q in range(len(file_read)):
        file_url = file_read[q]['url']
        file_url = ''.join(file_url)
        template_dir = file_read[q]['template']
        template_dir = ''.join(template_dir)
        pwd = os.getcwd()
        load_template_dir = pwd + '/' + input_dir + "/templates/"
        template_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(load_template_dir),
            autoescape=jinja2.select_autoescape(['html', 'xml']),
        )
        template = template_env.get_template(template_dir)
        html_output = template.render(file_read[q]["context"])
        if output is not None:
            output_dir = ''.join(output)
            output_p = output_dir
        else:
            output_dir = input_dir + "/html"
            output_p = input_dir
        try:
            pathlib.Path(pwd + file_url + output_dir).mkdir(parents=True,
                        exist_ok=False)
            filename = pathlib.Path(pwd + file_url + output_dir +
                                    "/" + template_dir)
            with open(filename, "w") as file_open:
                file_open.write(html_output)
            if pathlib.Path.exists(pathlib.Path(pwd + file_url
                                + input_dir + "/static/")):
                shutil.copytree(pathlib.Path(pwd + file_url
                        + input_dir + "/static/css/"),
                        pathlib.Path(pwd + file_url + output_dir + "/css/"))
                if verbose:
                    print(f"Copied {input_dir}/static -> {output_dir}")
            if verbose:
                print(f"Rendered {template_dir} -> {output_dir}{file_url}index.html/")
        except FileExistsError:
            print(f"Error: '{output_p}' already exists")


def load_json(input_dir):
    try:
        pwd = os.getcwd()
        config_filename = pathlib.Path(pwd + "/" + input_dir + "/config.json")
        with config_filename.open() as config_file:
            # config_filename is open within this code block
            return json.load(config_file)
    except FileNotFoundError:
        print("Error: '" + input_dir + "/config.json' not found")
    print(f"DEBUG input_dir={input_dir}")


if __name__ == "__main__":
    main()
