from jinja2 import Environment, FileSystemLoader

def render_template(client_data):
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("base_email.html")
    return template.render(client=client_data)