import collections

class Description:

    template = '''<div class = "bd-card">
                        <div class="card">
                            <h1 class="card-header">{}</h1>
                            <div class="card-body" >
                            {}
                            </div>
                        </div>
                    </div>'''

    def render(template, description):
        description_rendered = collections.OrderedDict()
        for key in description:
            name = description[key][0]
            text = description[key][1]
            description_rendered[key] = template.format(name, text)
        return description_rendered


    description = collections.OrderedDict()

    description["monovariate"] = ["monovariate",  '''
                            <p>Monovariate or Univariate analysis is the simplest form of analyzing data. “Uni” means “one”,
                                    so in other words your data has only one variable. It doesn’t deal with causes or relationships
                                    (unlike regression) and it’s major purpose is to describe; it takes data, summarizes that data and finds patterns
                                    in the data. </p>
                                    <ul>
                                    <li> Frequency Distribution Tables.</li>
                                    <li> Bar Charts </li>
                                    <li> characteristic values </li>
                                    <ul>
                                    <li>Mode</li>
                                    <li>Mean</li>
                                    <li>Total equilibrium</li>
                                    <li>Sqilibrium </li>
                                    <li>Sqilibrium norm</li>
                                    <li>Equilibrium norm</li>
                                    <li>Standard deviation</li>
                                    <li>Gini Index</li>
                                    </ul></p>
                ''']
    description["bivariate"] = ["bivariate and regression", '''
        <p> Bivariate analysis involves the analysis of two variables for the purpose of determining the empirical relationship between them.</p>
                                <ul>
                                <li> scatterplot with regression line </li>
                                </ul>
    
         ''']

    description["crosstab"] = ["crosstab and typological classification", "<p>A crosstab is a table showing the relationship between two or more variables. Where the table only shows the relationship between two categorical variables. </P>"]

    description["pandas_profiling"] = ["profiling", """<p> For each column the following statistics - if relevant for the column type - are presented in an interactive HTML report:</p>

    <ul>
    <li>Essentials: type, unique values, missing values </li>
    <li>Quantile statistics like minimum value, Q1, median, Q3, maximum, range, interquartile range </li>
    <li>Descriptive statistics like mean, mode, standard deviation, sum, median absolute deviation, coefficient of variation, kurtosis, skewness </li>
    <li>Most frequent values </li>
    <li>Histogram </li>
    <li>Correlations highlighting of highly correlated variables, Spearman, Pearson and Kendall matrices </li>
    <li>Missing values matrix, count, heatmap and dendrogram of missing values </li>
    </ul>
    <p> imported from pandas-profiling library </p>"""]

    description["kmeans"] = ["k-means","<p> k-means clustering aims to partition n observations into k clusters in which each observation belongs to the cluster with the nearest mean. </p>"]

    description["compute"] = ["compute", "<p> compute a new variable based on existing information (from other variables) </p>"]

    description["recode"] = ["recode", "<p> transform a variable by grouping its categories together. </p>"]

    guide = render(template, description)