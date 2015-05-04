Chart.defaults.global.animation = false;
Chart.defaults.global.responsive = true;

var Stats = React.createClass({
    addRandomColor: function(d, seed){
        var a = function(rgb,a){
            return 'rgba(' + rgb.join(', ') + ',' + a + ')';
        }
        var colors = randomColor({count:2,seed:seed,format:'rgbArray',luminosity:'light'})
        d.fillColor = a(colors[0],0.1)
        d.strokeColor = a(colors[1],1)
        d.pointColor = a(colors[1],1)
        d.pointStrokeColor = "#fff"
        d.pointHighlightFill = "#fff"
        d.pointHighlightStroke = a(colors[1],1)
        return d
    },
    render: function(){
        var years = {}
        this.props.data.reverse().map(function(s){
            var sem = s.semestre+s.semestre_annee
            if(!(sem in years)){
                years[sem] = {done:0,all:0,confidentiel:0,
                        gi:0,gm:0,gb:0,gp:0,gsu:0}
            }
            var y = years[sem];
            if(s.confidentiel){
                y.confidentiel += 1
            }
            if(s.done){
                y.done += 1;
                switch(s.branche_abbrev){
                    case 'GI':y.gi+=1;break;
                    case 'GM/GSM':y.gm+=1;break;
                    case 'GB':y.gb+=1;break;
                    case 'GP':y.gp+=1;break;
                    case 'GSU':y.gsu+=1;break;
                }
            }
            y.all += 1;
        })
        var by_year_done_data = {
            labels: _.keys(years),
            datasets: [
                this.addRandomColor({
                    label: "My First dataset",
                    data: _.values(years).map(function(x){return x.done})
                },123),
            ]
        };
        var by_year_data = {
            labels: _.keys(years),
            datasets: [
                this.addRandomColor({
                    data: _.values(years).map(function(x){return x.done})
                },23),
                this.addRandomColor({
                    data: _.values(years).map(function(x){return x.confidentiel})
                },12),
                this.addRandomColor({
                    data: _.values(years).map(function(x){return x.all})
                },11),
            ]
        };
        var by_year_branche_data = {
            labels: _.keys(years),
            datasets: [
                this.addRandomColor({
                    data: _.values(years).map(function(x){return x.gi})
                },11),
                this.addRandomColor({
                    data: _.values(years).map(function(x){return x.gm})
                },4),
                this.addRandomColor({
                    data: _.values(years).map(function(x){return x.gb})
                },55),
            ]
        };
        var by_year = <Chart.React.Line data={by_year_data}/>
        var by_year2 = <Chart.React.Line data={by_year_branche_data}/>
        var by_year3 = <Chart.React.Bar data={by_year_done_data}/>
        return <div>
            <div className="row">
                <div className="col-md-4">
                    {by_year}
                </div>
                <div className="col-md-4">
                    {by_year2}
                </div>
                <div className="col-md-4">
                    {by_year3}
                </div>
            </div>
            <hr/>
            <div className="row">
            </div>
        </div>;
    }
})