hideSeries = function($series) {
    for (i = 1; i < $series.length; i++) {
        s = $series[i];
        s["visible"] = false;
    }

    return $series;
};

formatTopCompaniesSeries = function($series, $companies_total_count) {
    for (i = 0; i < $series.length; i++) {
        s = $series[i];
        s.total = $companies_total_count[s.name];
        s.name += " (" + s.total + ")";
    }

    return hideSeries($series.sort(function(a,b) { return b.total - a.total }));
};

chartTopCompanies = function($data, $companies_total_count) {
    $series = formatTopCompaniesSeries(seriesFromData($data), $companies_total_count);

    $('#top-companies').highcharts({
        title: {
            text: 'Nombre de stages par entreprise par semestre',
            x: -20 //center
        },
        xAxis: {
            categories: categoriesFromData($data)
        },
        yAxis: {
            title: {
                text: 'Nombre de stages'
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }],
            min: 0,
            allowDecimals: false
        },
        tooltip: {
            valueSuffix: ' stages'
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        series: $series
    });
};