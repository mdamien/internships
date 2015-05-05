var Loader = React.createClass({
    getInitialState: function(){
        return {
            loading: false,
            data_url: this.props.data_url,
            data: [],
        }
    },
    componentDidMount: function(){
        this.load();
    },
    start_load: function(){
        this.setState({
            data_url:this.refs.data_url.getDOMNode().value,
            data:[],
        },this.load);
    },
    load: function(){
        this.setState({loading:true})
        Papa.parse(window.location.pathname+this.state.data_url, {
            download: true,
            header: true,
            skipEmptyLines: true,
            cache: false, //TODO add debug mode for this
            worker: true,
            error: function(err){
                console.log(err)
                this.setState({
                    loading:false,
                    error:" "+err,
                })
            }.bind(this),
            complete: function(results) {
                results.data.map(function(x,i){
                    x.done = x.done == "x";
                    x.confidentiel = x.confidentiel == "x";
                    if(x.semestre == undefined){
                        console.log(x)
                    }
                    x.semestre_annee = parseInt(x.semestre.slice(1));
                    x.semestre = x.semestre[0];
                    x.all = _.values(x).join(' ').toLowerCase();
                    x.id = i;
                    var branche_abbrev = ""
                    var bl = x.branche.toLowerCase();
                    if(bl == ""){
                        x.branche_abbrev = "";
                    }
                    else if(bl.startsWith('inform')
                        || bl.startsWith('Ingénierie des Services et des Systèmes'.toLowerCase())
                        || bl.startsWith("Sciences et Technologies de l'Information".toLowerCase()))
                    {
                        branche_abbrev = "GI";
                    }
                    else if(bl.startsWith('mécan')){
                        branche_abbrev = "GM/GSM"
                    }
                    else if( bl.startsWith('tronc')){
                        branche_abbrev = "TC"
                    }
                    else if( bl.startsWith('génie biologique')){
                        branche_abbrev = "GB"
                    }
                    else if( bl.startsWith('génie des procédés')){
                        branche_abbrev = "GP"
                    }
                    else if(bl.startsWith('systèmes urbains')){
                        branche_abbrev = "GSU"
                    }
                    else if(bl.startsWith('Humanités et Technologie'.toLowerCase())){
                        branche_abbrev = "HuTech"
                    }else{
                        branche_abbrev = "autre"
                        //console.log("branche inconnue:", x.num, x.id,x.branche.slice(0,50), "done:",x.done)
                    }
                    x.branche_abbrev = branche_abbrev;

                    var niveau_abbrev = ""
                    var nl = x.niveau.toLowerCase()
                    if(nl == ""){
                        niveau_abbrev = "";
                    }
                    else if(nl.indexOf("assistant") >= 0){
                        niveau_abbrev = "TN09"
                    }
                    else if(nl.indexOf('ouvrier') >= 0){
                        niveau_abbrev = "TN05"
                    }
                    else if(nl.indexOf('projet') >= 0){
                        niveau_abbrev = "TN10"
                    }
                    else if(nl.indexOf('master') >= 0){
                        niveau_abbrev = "master"
                    }
                    else if(nl.indexOf('apprenti') >= 0){
                        niveau_abbrev = "apprentissage"
                    }
                    else if(nl.indexOf('intercul') >= 0){
                        niveau_abbrev = "interculturel"
                    }
                    else if(nl.indexOf('licence') >= 0){
                        niveau_abbrev = "licence"
                    }
                    else{
                        niveau_abbrev = "autre"
                        //console.log("niveau inconnu:", x.id, x.num,x.niveau.slice(0,30), "done:",x.done)
                    }
                    x.niveau_abbrev = niveau_abbrev;
                })
                results.data.sort(function(x,y){
                    var comp = function(x,y){return x > y ? 1 : (x < y ? -1 : 0)}
                    var c = comp(y.semestre_annee, x.semestre_annee);
                    if(c != 0){return c};
                    c = comp(x.semestre, y.semestre);
                    if(c != 0){return c};
                    c = comp(x.sujet, y.sujet);
                    if(c != 0){return c};
                    return 0;
                })
                console.log("loaded",results.data.length,"elements")
                this.setState({
                    loading:false,
                    data:results.data,
                })
            }.bind(this)
        });
    },
    render: function(){
        var content = "";
        if(this.state.loading){
            content = <strong>chargement...{this.state.data_url}</strong>;
        }
        else if(this.state.data.length > 0){
            content = (<Loaded data={this.state.data} />);
        }
        if(this.state.error){
            content =  <p>Error lors du chargement de <b>{this.state.data_url}</b>: {this.state.error}</p>;
        }
        return (<div>
            {content}
        </div>);
    },
})