# -*- coding: utf-8 -*-
# system libraries

def main():

    import os
    from flask import Flask, request, render_template, url_for, redirect, send_from_directory
    import flask
    import matplotlib as mpl
    mpl.use('Agg')
    from elab import Elab

    obj_elab = Elab()

    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    ALLOWED_EXTENSIONS = set(["xlsx", "csv"])

    os.chdir(APP_ROOT)
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'gogogogo' #modify on server machine
    app.config["CLIENT_IMAGES"] = "./static/images"

    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @app.route("/")
    def index():
        files = os.listdir("./static/uploads/")
        return render_template("index.html", files=files, upload="initial")

    @app.route('/upload_file', methods=['GET', 'POST'])
    def upload_file():
        if request.method == 'POST':
            f = request.files['file']
            if allowed_file(f.filename):
                f.save(os.path.join(APP_ROOT, 'static', 'uploads', f.filename))
                files = os.listdir("./static/uploads/")
                return render_template("index.html", files=files, upload="true")
            else:
                return render_template("index.html", files=files, upload="false")

    @app.route('/load', methods=['GET', 'POST'])
    def load():
        #return obj_elab.operation.load(request, obj_elab)
        try:
            return obj_elab.load(request)
        except:
            request.form = {"load": obj_elab.selected_file,
                         "file_config": obj_elab.action_to_file}
            return obj_elab.load(request)
    @app.route("/create_subset", methods=['POST'])
    def create_subset():
        return obj_elab.operation.create_subset(obj_elab.dataset)


    @app.route('/action', methods=['GET', 'POST'])
    def action():
        return obj_elab.action(request)
## action navbar
    @app.route('/monovariate', methods=['GET', 'POST'])
    def monovariate():
        return render_template("monovariate/monovariate_selection.html",
                                   variable_name_type=obj_elab.variable_name_type,
                                   dataset=obj_elab.selected_file)

    @app.route('/recode', methods=['GET', 'POST'])
    def recode():
        return render_template("recode/recode_selection.html",
                                   variable_name_type=obj_elab.variable_name_type,
                                   dataset=obj_elab.selected_file)

    @app.route('/bivariate_and_regression', methods=['GET', 'POST'])
    def bivariate_and_regression():
        return render_template("bivariate/bivariate_selection.html",
                                   variable_name_type=obj_elab.variable_name_type_obj,
                                   dataset=obj_elab.selected_file,
                                   variable_name_type_obj=obj_elab.variable_name_type_only_obj)

    @app.route('/crosstab_and_typological_classification', methods=['GET', 'POST'])
    def crosstab_and_typological_classification():
        return render_template("crosstab/crosstab_selection.html",
                               variable_name_type=obj_elab.variable_name_type,
                               dataset=obj_elab.selected_file)

    @app.route('/k_mean_classification', methods=['GET', 'POST'])
    def k_mean_classification():
        return render_template("cluster/cluster_selection.html",
                               variable_name_type=obj_elab.variable_name_type_obj,
                               dataset=obj_elab.selected_file)

    @app.route("/compute", methods=['GET', 'POST'])
    def compute():
        return render_template("calc.html",
                               variable_name_type=obj_elab.variable_name_type,
                               dataset=obj_elab.selected_file)

    ## plot and operation
    @app.route('/monovariate_plot', methods=['GET', 'POST'])
    def monovariate_plot():
        return obj_elab.output.monovariate_plot(request, obj_elab.dataset)

    @app.route('/set_monovariate_plot_sorted', methods=["GET", 'POST'])
    def set_monovariate_plot_sorted():
        posted = request.get_json()
        obj_elab.output.monovariate_plot_session["option_categorical_list"] = posted['cagory_order']
        return "change_page"

    @app.route('/monovariate_plot_sorted', methods=["GET", 'POST'])
    def monovariate_plot_sorted():
        return obj_elab.output.monovariate_plot_sorted(obj_elab.dataset)

    @app.route('/recode_operation', methods=['GET', 'POST'])
    def recode_operation():
        return obj_elab.operation.recode_operation(request, obj_elab.dataset)

    @app.route('/recode_output', methods=['GET', 'POST'])
    def recode_output():
        return obj_elab.output.recode_output(request, obj_elab.dataset)

    @app.route('/bivariate_plot', methods=['GET', 'POST'])
    def bivariate_plot():
        return obj_elab.output.bivariate_plot(request, obj_elab.dataset)

    @app.route('/ncrosstab_output', methods=['GET', 'POST'])
    def ncrosstab_output():
        return obj_elab.output.ncrosstab_output(request, obj_elab.dataset)

    @app.route('/ncrosstab_classification', methods=['GET', 'POST'])
    def ncrosstab_classification():
        return obj_elab.output.ncrosstab_classification()

    @app.route('/ncrosstab_classification_output', methods=["GET", "POST"])
    def ncrosstab_classification_output():
        return obj_elab.output.ncrosstab_classification_ouput(obj_elab.dataset,
                                                              obj_elab.selected_file_link)

    @app.route('/cluster_output', methods=["POST"])
    def cluster_output():
        return obj_elab.output.cluster_output(request,
                                              obj_elab.dataset,
                                              obj_elab.selected_file_link)

    @app.route('/calc_output', methods=['GET', 'POST'])
    def calc_output():
        return obj_elab.output.calc_output(request, obj_elab.dataset)

    @app.route("/post_arrive", methods=["GET", 'POST'])
    def post_arrive():
        obj_elab.operation.post_arrive(request, obj_elab)

    @app.route("/profiling_output", methods=["GET", 'POST'])
    def profiling_output():
        return obj_elab.output.profiling_output(obj_elab)


    @app.route("/get-image/<image_name>")
    def get_image(image_name):
        try:
            return send_from_directory(app.config["CLIENT_IMAGES"], filename="{}.png".format(flask.session["img.png"]),
                                       as_attachment=False)
        except FileNotFoundError:
            abort(404)

    @app.route("/jupyter")
    def jupyter():
        import webbrowser
        url = "http://localhost:8888/"
        import os
        import subprocess
        #threading.Timer(1.50, lambda: os.system("jupyter notebook"))
        proc = subprocess.Popen('jupyter notebook', shell=True, stdout=subprocess.PIPE)
        return "start jupyter"

    app.run(port=5555, debug=True)

if __name__ == "__main__":
    main()