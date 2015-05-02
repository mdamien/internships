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
        Papa.parse(this.state.data_url, {
            download: true,
            header: true,
            skipEmptyLines: true,
            cache: false, //TODO add debug mode for this
            complete: function(results) {
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
                results.data.map(function(x,i){
                    x.stage_reel = x.stage_reel == undefined || x.stage_reel == "True";
                    x.semestre_annee = parseInt(x.semestre_annee);
                    x.all = _.values(x).join(' ').toLowerCase();
                    x.id = i;
                    var addrs = x.addresse.split('\n')
                    x.pays = addrs[addrs.length-1]
                    x.ville = addrs[addrs.length-2].split(' ').slice(1).join(' ')
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
            content = <strong>loading...{this.state.data_url}</strong>;
        }
        else if(this.state.data.length > 0){
            content = (<Loaded data={this.state.data} />);
        }
        return (<div>
            {content}
        </div>);
    },
})