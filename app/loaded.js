var Loaded = React.createClass({
    getInitialState: function(){
        return {
            page:'table',
        }
    },
    render: function(){
        return (<div>
                <h4>Stages UTC <small>{this.props.data.length} stages</small></h4>
                <hr/>
                <FilterTable data={this.props.data}/>
        </div>)
    }
})