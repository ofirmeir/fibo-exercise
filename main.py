from flask import Flask, jsonify, render_template, request
from github import Github

app = Flask(__name__)


def repository_structure_builder(repository, path):
    repository_dict = {}
    files_list = []
    dir_contents = repository.get_contents(path)
    for item in dir_contents:
        if item.type == "dir":
            repository_dict[item.name] = repository_structure_builder(repository, item.path)
        else:
            files_list.append(item.name)
    repository_dict["files"] = files_list
    return repository_dict


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/repositories/get")
def get_repository_files():
    owner_name = request.args["owner"]
    repository_name = request.args["repository"]
    github = Github()
    repository = github.get_user(login=owner_name).get_repo(repository_name)
    repository_dict = repository_structure_builder(repository, "")
    return jsonify(repository_dict)


if __name__ == '__main__':
    app.run(debug=True)
