Chart.defaults.global.animation = false;
Chart.defaults.global.responsive = true;

var Stats = React.createClass({
    render: function(){
        var years = {}
        var years_all = {}
        this.props.data.map(function(s){
            var sem = s.semestre+s.semestre_annee
            if(s.done){
                if(sem in years){
                    years[sem] += 1;
                }else{
                    years[sem] = 1;
                }
            }

            if(sem in years_all){
                years_all[sem] += 1;
            }else{
                years_all[sem] = 1;
            }
        })
        var by_year_data = {
            labels: _.keys(years),
            datasets: [
                {
                    label: "My First dataset",
                    fillColor: "rgba(220,220,220,0.2)",
                    strokeColor: "rgba(220,220,220,1)",
                    pointColor: "rgba(220,220,220,1)",
                    pointStrokeColor: "#fff",
                    pointHighlightFill: "#fff",
                    pointHighlightStroke: "rgba(220,220,220,1)",
                    data: _.values(years)
                },
                {
                    label: "My Second dataset",
                    fillColor: "rgba(151,187,205,0.2)",
                    strokeColor: "rgba(151,187,205,1)",
                    pointColor: "rgba(151,187,205,1)",
                    pointStrokeColor: "#fff",
                    pointHighlightFill: "#fff",
                    pointHighlightStroke: "rgba(151,187,205,1)",
                    data: _.values(years_all)
                }
            ]
        };
        var by_year = <Chart.React.Bar data={by_year_data}/>
        var by_year2 = <Chart.React.Line data={by_year_data}/>
        return <div className="row">
            <div className="col-md-6">
                {by_year}
            </div>
            <div className="col-md-6">
                {by_year2}
            </div>
        </div>;
    }
})