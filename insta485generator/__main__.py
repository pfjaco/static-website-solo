"""Build static HTML site from directory of HTML templates and plain files."""
import click
import pathlib
import os
import jinja2
import json
import shutil
@click.command()
@click.option('--output','-o', help="Output directory.", is_flag=True)
@click.option('--verbose','-v', help="Print more output.", metavar="PATH")
@click.argument("input_dir", nargs=1, type=click.Path(exists=True))
def main(input_dir,output,verbose):
    
    file_read = load_json(input_dir)
    file_url = [x['url'] for x in file_read]
    file_url= ''.join(file_url)
    template_dir = [x['template'] for x in file_read]
    template_dir = ''.join(template_dir)
    pwd = os.getcwd()
    load_template_dir = pwd + file_url + input_dir + "/templates/"
    template_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(load_template_dir),
        autoescape=jinja2.select_autoescape(['html', 'xml']),
    )
    template = template_env.get_template(template_dir)    
    output = template.render(file_read[0]["context"])
    try:
        pathlib.Path(pwd + file_url + input_dir +"/html").mkdir(parents=True, exist_ok=False)
        filename = pathlib.Path(pwd + file_url + input_dir + "/html/" + template_dir)
        print(filename)
        with open(filename, "w") as f:
            f.write(output)               
    except FileExistsError:
            print(f"Error: '{input_dir}/html' directory already exists")
    if(pathlib.Path.exists(pathlib.Path(pwd + file_url + input_dir + "/static/"))):
            shutil.copytree(pathlib.Path(pwd + file_url + input_dir + "/static/css/"),pathlib.Path(pwd + file_url + input_dir + "/html/css/"))


def load_json(input_dir):
    try:
        pwd = os.getcwd()
        config_filename = pathlib.Path(pwd+ "/" + input_dir + "/config.json")
        with config_filename.open() as config_file:
        # config_filename is open within this code block
            return json.load(config_file)        
    except:
        print(f"Error: '"+input_dir+"/config.json' not found")
        #except Exception as error:
        #print("An error occurred:", error)
    print(f"DEBUG input_dir={input_dir}")


if __name__ == "__main__":
    main()