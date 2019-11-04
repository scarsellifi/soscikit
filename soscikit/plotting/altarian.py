import altair as alt
import pandas as pd
import numpy as np


def altair_monovariate(data, options_tipo_var, lista_ordinale):
    datatest = data
    if options_tipo_var == "cardinale":
        bars = alt.Chart(datatest).mark_bar().encode(
            x="X:N",
            y="Frequency"
        ).encode(
            tooltip=['X', 'Frequency']
        )
        text = bars.mark_text(
            align='left',
            baseline='middle',
            color="blue",
            fontSize=20,
            dx=0,  # Nudges text to right so it doesn't appear on top of the bar
            dy=-7
        ).encode(
            text='Frequency:Q',
            tooltip=['X', 'Frequency']
        )
        chart = (bars + text).properties(width=800, height=400).interactive()
    elif options_tipo_var == "categoriale":
        bars = alt.Chart(datatest).mark_bar().encode(
            x=alt.X("X:N",
                    sort=alt.EncodingSortField(
                        field="frequency",  # The field to use for the sort
                        order="descending"  # The order to sort in
                    )),
            y=alt.Y("Frequency")

        ).encode(
            tooltip=['X', 'Frequency']
        )
        text = bars.mark_text(
            align='left',
            baseline='middle',
            color="blue",
            fontSize=20,
            dx=0,  # Nudges text to right so it doesn't appear on top of the bar
            dy=-7
        ).encode(
            text='Frequency:Q',
            tooltip=['X', 'Frequency']
        )
        chart = (bars + text).properties(width=800, height=400).interactive()

    elif lista_ordinale == True:
        bars = alt.Chart(datatest).mark_bar().encode(
            x=alt.X('X:N', sort=lista_ordinale),
            y=alt.Y('Frequency')
        ).encode(
            tooltip=['X', 'Frequency']
        )
        text = bars.mark_text(
            align='left',
            baseline='middle',
            color="blue",
            fontSize=20,
            dx=0,  # Nudges text to right so it doesn't appear on top of the bar
            dy=-7
        ).encode(
            text='Frequency:Q',
            tooltip=['X', 'Frequency']
        )
        chart = (bars + text).properties(width=500, height=300).interactive()

    return chart

def altair_bivariate(dataset, g_x, g_y):


    dataset = dataset.dropna(subset=[g_x, g_y])
    datatest = pd.DataFrame({"X": dataset[g_x],
                             "Y": dataset[g_y]})

    # Build a dataframe with the fitted data
    degree_list = [1, 3, 5]
    poly_data = pd.DataFrame({'xfit': np.linspace(datatest['X'].min(), datatest['X'].max(), 500)})
    for degree in degree_list:
        poly_data[str(degree)] = np.poly1d(np.polyfit(datatest['X'], datatest['Y'], degree))(poly_data['xfit'])

    points = alt.Chart(datatest).mark_point().encode(
        x="X",
        y="Y"
    ).encode(
        tooltip=['X', 'Y']
    )
    # Plot the best fit polynomials
    polynomial_fit = alt.Chart(poly_data).transform_fold(
        ['1', '3', '5'],
        as_=['degree', 'yfit']
    ).mark_line().encode(
        x='xfit:Q',
        y='yfit:Q',
        color='degree:N'
    )

    chart = (points + polynomial_fit).properties(width=500, height=300).interactive()
    return chart
