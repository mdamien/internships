var FilterTable = React.createClass({
    getInitialState: function(){
        return {
            filters: {},
        }
    },
    handleFilterUpdate: function(filters){
        this.handleUnselect();
        console.log('filter updated', filters)
        this.setState({filters:filters});
    },
    handleSelected: function(selected){
        this.setState({selected:selected});
    },
    handleUnselect: function(){
        this.setState({selected:null});
    },
    filtered_data: function(){
        var filters = this.state.filters;
        var data = this.props.data;
        if(filters){
            var text = false;
            if(filters.text && filters.text != ''){
                text = filters.text.toLowerCase();
            }
            var type = false;
            if(filters.type && filters.type != 'all'){
                type = filters.type;
            }
            var branch = false;
            if(filters.branch && filters.branch != 'all'){
                branch = filters.branch;
            }
            var hide_not_real = false;
            if(filters.hide_not_real != undefined && filters.hide_not_real == true){
                hide_not_real = true;
            }
            var from_sem = false;
            var from_year = false;
            if(filters.from != undefined){
                from_sem = filters.from[0]
                from_year = parseInt(filters.from.slice(1))
            }
            var to_sem = false;
            var to_year = false;
            if(filters.to != undefined){
                to_sem = filters.to[0]
                to_year = parseInt(filters.to.slice(1))
            }
            if(text || type || branch || hide_not_real || from_year || to_year){
                return jQuery.grep(data,function(line){
                    if( from_year && line.semestre_annee < from_year){
                        return false;
                    }
                    if( to_year && line.semestre_annee > to_year){
                        return false;
                    }
                    if(hide_not_real && !line.done){
                        return false;
                    }
                    if(type && line.niveau_abbrev != type){
                        return false;
                    }
                    if(branch && line.branche_abbrev != branch){
                        return false;
                    }
                    if(text && line.all.indexOf(text) == -1){
                        return false;
                    }
                    return true;
                })
            }
        }
        return data;
    },
    render: function(){
        var data_filtered = this.filtered_data();
        var content = "";
        var counter = "";
        if(this.props.data.length != data_filtered.length){
            counter = (<span className="label label-success pull-right">
                    Affiche {data_filtered.length} / {this.props.data.length} stages
                </span>)
        }
        var table = (<div className="col-md-12">
                <Table data={data_filtered} selected={this.state.selected} onSelected={this.handleSelected} />
            </div>);
        if(data_filtered.length == 0){
            table = <h5 className="text-center">Aucune donnée à afficher</h5>;
        }
        if(this.state.selected){
            content = (<div>
                {table}
                <div className="col-md-10">
                    <InternshipPanel selected={this.state.selected} onClose={this.handleUnselect} />
                </div>
                </div>);
        }else{
            content = table;
        }
        return (<div>
            <Filters onUpdate={this.handleFilterUpdate} filters={this.state.filters}/>
            <br/>
            {counter}
            <div className="row">
                {content}
            </div>
        </div>)
    }
})