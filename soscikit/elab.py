import webbrowser
import os
import pandas as pd
from collections import OrderedDict
# flask libraries
from flask import Flask, request, render_template, url_for, redirect, send_from_directory
import flask
# from flask_bootstrap import Bootstrap
import json
from stats_tools import tools
from stats_tools import table
import seaborn as sns
from scipy.cluster.vq import kmeans, vq
import uuid
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from plotting.altarian import altair_monovariate, altair_bivariate
import pandas_profiling
import re

class Output():
    """output operation"""
    def __init__(self):
        pass

    monovariate_plot_session = {}
    script = ""
    crosstab_session = {}

    def monovariate_plot(self, request, dataset):
        r = request
        g = r.form.getlist('monovariate')
        options_tipo_var = r.form["var_type"]
        #options_ordinal_list = r.form["ordinal_list"]
        options_drop = r.form["drop_missing"]

        self.monovariate_plot_session = {
            "g": g,
            "options_tipo_var": options_tipo_var,
            #'options_categorical_list': options_ordinal_list
        }
        """
        if request.form["ordinal_list"] == "":
            lista_ordinale = False
        else:
            lista_ordinale = request.form["ordinal_list"].split(",")
            try:
                lista_ordinale = [int(x) for x in lista_ordinale]
            except:
                lista_ordinale
        print(lista_ordinale)
        """
        if options_drop == "drop":
            dataset.dropna(subset=[g[0]], inplace=True)
        elif options_drop == "no_drop":
            pass

        unique_values = dataset[g[0]].unique()

        data = table.dist_frequenza(dataset,
                                    g[0],
                                    save=False,
                                    tipo=options_tipo_var)

        data_non_tot = data.drop("Totale")

        """if lista_ordinale != False:
            data.index = data.index.map(str)
        """
        datatest = pd.DataFrame({"X": data_non_tot.index.values,
                                 "Frequency": data_non_tot["Frequenze"].values})

        equilibrium_values = tools.Sq_output(datatest["Frequency"])
        if options_tipo_var == "cardinale":
            characteristic_values = {
                "mean": datatest["Frequency"].mean(),
                "standard deviation": datatest["Frequency"].std(),
                "gini index": tools.gini(datatest["Frequency"].values)

            }

        if options_tipo_var == "categoriale":
            characteristic_values = {
                "mode": datatest[datatest["Frequency"] == datatest["Frequency"].max()]["X"].values[0],
                "total equilibrium": datatest["Frequency"].sum() / len(datatest["Frequency"].unique()),
                "Sq": equilibrium_values["Sq"],
                "Sq_norm": equilibrium_values["Sq_Norm"],
                "Eq": equilibrium_values["Eq"]

            }

        chart = altair_monovariate(data=datatest, options_tipo_var=options_tipo_var, lista_ordinale=False)

        return render_template("monovariate/monovariate_plot.html",
                               operation_form=g,
                               chart_json=chart.to_json(),
                               data=data.to_html(classes="table table-striped"),
                               unique_values=unique_values,
                               options_tipo_var=options_tipo_var,
                               characteristic_values=characteristic_values
                               )

    def monovariate_plot_sorted(self, dataset):
        g = self.monovariate_plot_session["g"]
        options_tipo_var = self.monovariate_plot_session["options_tipo_var"]
        options_categorical_list = self.monovariate_plot_session["option_categorical_list"]
        dataset = dataset
        unique_values = dataset[g[0]].unique()

        data = table.dist_frequenza(dataset,
                                    g[0],
                                    save=False,
                                    tipo="categoriale",
                                    lista_ordinale=options_categorical_list)

        data_non_tot = data.drop("Totale")

        datatest = pd.DataFrame({"X": data_non_tot.index.values,
                                 "Frequency": data_non_tot["Frequenze"].values})
        # print(datatest)
        datatest.dropna(inplace=True)
        datatest.set_index(datatest["X"], inplace=True)
        datatest.index = datatest.index.map(str)
        datatest = datatest.loc[options_categorical_list]
        # print("{}{}".format(data.columns[0], ":Q"), "{}{}".format(data.columns[1], ":0"))

        equilibrium_values = tools.Sq_output(datatest["Frequency"])
        if options_tipo_var == "cardinale":
            characteristic_values = {
                "mean": datatest["Frequency"].mean(),
                "standard deviation": datatest["Frequency"].std(),
                "gini index": tools.gini(datatest["Frequency"].values)

            }

        if options_tipo_var == "categoriale":
            characteristic_values = {
                "mode": datatest[datatest["Frequency"] == datatest["Frequency"].max()]["X"].values[0],
                "total equilibrium": datatest["Frequency"].sum() / len(datatest["Frequency"].unique()),
                "Sq": equilibrium_values["Sq"],
                "Sq_norm": equilibrium_values["Sq_Norm"],
                "Eq": equilibrium_values["Eq"]

            }
        chart = altair_monovariate(data=datatest, options_tipo_var=options_tipo_var,
                                   lista_ordinale=options_categorical_list)

        return render_template("monovariate/monovariate_plot.html",
                               operation_form=g,
                               chart_json=chart.to_json(),
                               data=data.to_html(classes="table table-striped"),
                               unique_values=unique_values, options_tipo_var=options_tipo_var,
                               characteristic_values=characteristic_values)

    def bivariate_plot(self, request, dataset):
        g = request
        g_x = g.form.getlist('bivariate_x')[0]
        g_y = g.form.getlist('bivariate_y')[0]

        print(g_x, g_y)
        try:
            data = dataset
        except:
            dataset = pd.read_excel("./static/uploads/" + flask.session["selected_file"])
            data = dataset


        correlation = data[[g_x, g_y]].corr()

        chart = altair_bivariate(dataset, g_x, g_y)

        script = g.form["textarea_script"]
        print(script)
        plt.figure()
        result = eval(script, {'data': data, "pd": pd, "sns": sns})
        img_name = uuid.uuid4()
        flask.session["img.png"] = img_name

        plt.savefig("./static/images/{}.png".format(img_name))
        plt.figure()
        img_link = url_for("get_image", image_name="{}.png".format(img_name))

        # maybe solution https://stackoverflow.com/questions/53268133/generate-image-on-the-fly-using-flask-and-matplotlib
        return render_template("bivariate/bivariate_plot.html",
                               operation_form=str((g_x, g_y)),
                               chart_json=chart.to_json(),
                               correlation=correlation.to_html(classes="table table-striped"),
                               img_link=img_link)

    def cluster_output(self, request, dataset, selected_file_link):
        data = dataset

        nome_var = request.form["new_var_name"]
        script = request.form["textarea_script"]
        self.script = script
        result = eval(script, {'data': data, "pd": pd, "vq": vq, "kmeans": kmeans})
        data_select = data[result[0]]
        data_select.dropna(inplace=True)
        data_select = data_select.applymap(float)

        data_values = data_select.values

        centroids, _ = kmeans(data_values, result[1])
        # assign each sample to a cluster
        idx, _ = vq(data_values, centroids)
        data_select[nome_var] = idx
        output = pd.concat([data_select[nome_var], data], axis=1)
        plt.figure()
        variabile = eval(script)[0]
        if len(variabile) == 2:
            img_name = uuid.uuid4()

            c = output[nome_var]
            flask.session["img.png"] = img_name
            for classes in c.unique():
                output_temp = output[output[nome_var] == classes]
                x = output_temp[variabile[0]]
                y = output_temp[variabile[1]]

                result = sns.scatterplot(x=x, y=y, data=output_temp, cmap="tab20c", label=classes)
                result.legend()

            # result.figure.savefig("./static/images/{}.png".format(img_name))
            plt.savefig("./static/images/{}.png".format(img_name))
            img_link = url_for("get_image", image_name="{}.png".format(img_name))
        elif len(variabile) == 3:
            img_name = uuid.uuid4()

            c = output[nome_var]

            flask.session["img.png"] = img_name
            result = plt.axes(projection='3d')
            for classes in c.unique():
                output_temp = output[output[nome_var] == classes]
                x = output_temp[variabile[0]]
                y = output_temp[variabile[1]]
                z = output_temp[variabile[2]]

                result.scatter3D(x, y, z, cmap="tab20c", label=classes)
                result.legend()

            plt.savefig("./static/images/{}.png".format(img_name))
            img_link = url_for("get_image", image_name="{}.png".format(img_name))
        else:
            img_link = ""
        output.to_excel(selected_file_link, index=False)
        output = output.to_html(table_id="result_data")
        plt.figure()


        return render_template("cluster/cluster_output.html", data=output, img_link=img_link)

    def ncrosstab_output(self, request, dataset):
        try:
            script = request.form["textarea_script"]
            index_series = request.form["textarea_script_index"]
            columns_series = request.form["textarea_script_columns"]
            self.script = script
            self.index_series = index_series
            self.columns_series = columns_series
        except:
            script = self.script
        data = dataset
        result = eval(script, {'data': data, "pd": pd})


        '''
        index = script.split("index=[")[1].split("]],")[0]
        columns = script.split("columns=[")[1].split("]],")[0]
        print(index, columns)
        '''
        try:
            print(result.index.nlevels)
            self.crosstab_session["ncrosstab_classification_index"] = result.index.nlevels
        except:
            pass
        try:
            print(result.columns.nlevels)
            self.crosstab_session["ncrosstab_classification_columns"] = result.columns.nlevels

        except:
            pass

        if result.index.nlevels == 1 & result.columns.nlevels == 1:
            abilitate_tipology = "abilitate"
            stacked = result.stack().reset_index().rename(columns={0: 'value'})
            print(stacked)
            result_img = sns.barplot(x=stacked.columns[0], y=stacked.columns[2], hue=stacked.columns[1], data=stacked)
            img_name = uuid.uuid4()
            flask.session["img.png"] = img_name

            plt.savefig("./static/images/{}.png".format(img_name))
            plt.figure()
            img_link = url_for("get_image", image_name="{}.png".format(img_name))
        else:
            abilitate_tipology = "disabilitate"
            img_link = ""

        self.crosstab_session["ncrosstab_output"] = result.to_html(classes="draggable", table_id="corr_tab")
        self.crosstab_session["ncrosstab_output_margin"] = "pass"
        self.crosstab_session["crosstab_output_descriptive"] = "pass"

        return render_template("crosstab/crosstab_output.html",
                               table=result.to_html(classes="draggable",
                                                    table_id="corr_tab"),
                               abilitate_tipology=abilitate_tipology,
                               img_link=img_link)

    def ncrosstab_classification(self):
        result = self.crosstab_session["ncrosstab_output"]
        ncrosstab_classification_index = self.crosstab_session["ncrosstab_classification_index"]
        ncrosstab_classification_columns = self.crosstab_session["ncrosstab_classification_columns"]
        return render_template("crosstab/crosstab_classification.html",
                               table=result,
                               classification_index=ncrosstab_classification_index,
                               classification_columns=ncrosstab_classification_columns
                               )

    def ncrosstab_classification_ouput(self, dataset, selected_file_link):
        dataset.to_excel(selected_file_link, index=False)
        return render_template("crosstab/crosstab_classification_output.html",
                               table= dataset.to_html(table_id = "result_data"))

    def recode_output(self, request, dataset):
        g = request.values.to_dict()
        new_var_name = g["new_variabile_name"]
        recode_var = flask.session["recode_var"]
        print(recode_var[0])
        dataset = pd.read_excel("./static/uploads/" + flask.session["selected_file"])

        def recode(dictionary, x):
            try:
                return dictionary[x]
            except:
                return x

        dataset[new_var_name] = dataset[recode_var[0]].apply(lambda x: recode(g, x))
        dataset.to_excel("./static/uploads/" + flask.session["selected_file"], index=False)

        output = dataset.to_html(table_id="result_data")
        return render_template("cluster/cluster_output.html", data=output)

    def calc_output(self, request, dataset):
        g = request
        print(g.form)
        dataset = g.form["dataset"]
        data = pd.read_excel("./static/uploads/" + dataset)
        result = eval(g.form["formula"], {'data': data})

        if g.form["new_variabile"] == "":
            if isinstance(result, pd.Series):
                return eval(g.form["formula"], {'data': data}).to_frame().to_html(classes="table table-striped")
            elif not isinstance(result, pd.Series):
                return eval(g.form["formula"], {'data': data})
        else:
            data[g.form["new_variabile"]] = eval(g.form["formula"], {'data': data})
            dataset = g.form["dataset"]
            data.to_excel("./static/uploads/" + dataset)
            # return "<h> nuova variabile </h>" + data[g.form["new_variabile"]].to_frame().to_html()
            output = pd.concat([data[g.form["new_variabile"]], data], axis=1)

            output = output.to_html(table_id="result_data")
            return render_template("calc_output.html", data=output)

    def profiling_output(self, obj_elab):
        data = obj_elab.dataset
        # profile = data.profile_report(title=flask.session["selected_file"])
        profile = pandas_profiling.ProfileReport(data)
        print(dir(profile))
        profile.title = obj_elab.selected_file
        profile.to_file(output_file="./templates/profiling.html")
        return render_template("profiling.html")


class Operation():
    def __init__(self):
        pass

    recode_session = {}
    def load(self, request, obj_elab):
        g = request
        dataset = obj_elab.load(g)
        html_data = dataset.head(500).to_html(table_id="head_data",
                                              classes="table table-striped table-bordered display nowrap")
        return render_template("select_action.html",
                               selected_file=obj_elab.selected_file,
                               html_data=html_data)

    def recode_operation(self, request, dataset):
        g = request.form.getlist('recode_var')
        self.recode_session["recode_var"] = g
        flask.session["recode_var"] = g

        dataset = pd.read_excel("./static/uploads/" + flask.session["selected_file"])
        unique_values = dataset[g[0]].unique()

        data = table.dist_frequenza(dataset,
                                    g[0],
                                    save=False,
                                    tipo="categoriale")

        return render_template("recode/recode_operation.html",
                               operation_form=g,
                               data=data.to_html(classes="table table-striped"),
                               unique_values=unique_values,

                               )

    def post_arrive(request, obj_elab):
        posted = request.get_json()['category_order']
        recode = posted
        try:
            data = obj_elab.dataframe
            import numpy as np
            data["type_" + recode['vary'] + "_" + recode['varx']] = np.nan

            def set_typo(row, recode):
                for item in recode['dataframe']:
                    if (row[recode['varx']] == item['categoryx']) & (row[recode['vary']] == item['categoryy']):
                        print(row[recode['varx']] == item['categoryx'], row[recode['varx']], item['categoryx'],
                              row[recode['vary']], item['categoryy'], item["value"])
                        return item["value"]
                    else:
                        pass

            data["type_" + recode['vary'] + "_" + recode['varx']] = data.apply(lambda row: set_typo(row, recode),
                                                                               axis=1)
            obj_elab.dataset = data
            data.to_excel(obj_elab.selected_file)
            return "executed: you can find the new variabile in the last columns of dataframe"
        except:
            return "error.. somethings wrong"

    def create_subset(self, dataset):
        selection = request.values.to_dict()
        new_filename = selection['new_filename']
        del selection['new_filename']
        new_filename = str(new_filename) + ".xlsx"
        columns = selection.keys()
        dataset_subset = dataset[columns]
        dataset_subset.to_excel("./static/uploads/" + new_filename, index = False)
        files = os.listdir("./static/uploads/")
        return render_template("index.html", files=files, upload="true")


class Elab():
    """
    Main class

    """

    def __init__(self):
        pass
    #variabile
    selected_file = "no_file"
    action_to_file = "no_action"
    variable_name_type = OrderedDict()
    variable_name_type_obj = OrderedDict()
    dataset = ""
    option_categorical_list = ""
    monovariate_plot_session = ""
    selected_file_link = ""
    #inner classes
    output = Output()
    operation = Operation()

    def load(self, request):
        g = request
        self.selected_file = g.form["load"]
        self.action_to_file = g.form["file_config"]
        self.selected_file_link = "./static/uploads/" + self.selected_file
        self.variable_name_type = {}
        self.variable_name_type_obj = {}
        self.variable_name_type_only_obj = {}

        if g.form["file_config"] == "remove":
            os.remove("./static/uploads/" + g.form["load"])
            files = os.listdir("./static/uploads/")
            return render_template("index.html", files=files, upload="removed")
        else:
            if g.form["file_config"] == "standard_excel":
                flask.session["selected_file"] = g.form["load"]
                dataset = pd.read_excel("./static/uploads/" + g.form["load"])
            elif g.form["file_config"] == "excel_google_form":
                dataset = pd.read_excel("./static/uploads/" + g.form["load"])
                dataset = dataset.applymap(lambda x: tools.google_form_likert(x))
                dataset.to_excel("./static/uploads/" + "__gform__" + g.form["load"])
                flask.session["selected_file"] = "__gform__" + g.form["load"]
            elif g.form["file_config"] == "csv1":
                dataset = pd.read_csv("./static/uploads/" + g.form["load"], sep=";")
                dataset.to_excel("./static/uploads/" + g.form["load"] + ".xlsx")
                flask.session["selected_file"] = g.form["load"] + ".xlsx"
            elif g.form["file_config"] == "csv2":
                dataset = pd.read_csv("./static/uploads/" + g.form["load"], sep=",")
                dataset.to_excel("./static/uploads/" + g.form["load"] + ".xlsx")
                flask.session["selected_file"] = g.form["load"] + ".xlsx"
            elif g.form["file_config"] == "create_subset":
                flask.session["selected_file"] = g.form["load"]
                dataset = pd.read_excel("./static/uploads/" + g.form["load"])
                self.variable_name_type.update(dataset.dtypes.to_dict(into=OrderedDict))
                self.dataset = dataset
                return render_template("create_subset.html", columns=self.variable_name_type)
            elif g.form["file_config"] == "join_dataset":
                pass
            else:
                pass

            self.variable_name_type.update(dataset.dtypes.to_dict(into=OrderedDict))
            self.variable_name_type_obj.update(dataset.loc[:, (dataset.dtypes != "object").values].dtypes.to_dict(into=OrderedDict))
            self.variable_name_type_only_obj.update(dataset.loc[:, (dataset.dtypes == "object").values].dtypes.to_dict(into=OrderedDict))
            self.dataset = dataset
            html_data = dataset.head(500).to_html(table_id="head_data",
                                                  classes="table table-striped table-bordered display nowrap")
            self.html_data = html_data
            return render_template("select_action.html",
                                   selected_file=self.selected_file,
                                   html_data=html_data)





