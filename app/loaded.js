var Loaded = React.createClass({
    getInitialState: function(){
        return {
            page:'stats',
        }
    },
    changePage: function(page){
        this.setState({page:page})
    },
    render: function(){
        var pages = [['table','Données'],['stats','Stats']];
        var pages_btns = pages.map(function(x,i){
            var klass = "btn " + (this.state.page == x[0] ? 'btn-primary': 'btn-default');
            return (<span key={i}>
                    &nbsp;&nbsp;
                    <button className={klass} onClick={this.changePage.bind(null,x[0])}>{x[1]}</button>
                </span>)
        }.bind(this)) 
        var content = <FilterTable data={this.props.data}/>
        if(this.state.page == 'stats'){
            content = <Stats data={this.props.data} />
        }
        return (<div>
                <h4>Stages UTC <small>{this.props.data.length} stages</small>
                {pages_btns}
                </h4>
                <hr/>
                {content}
        </div>)
    }
})