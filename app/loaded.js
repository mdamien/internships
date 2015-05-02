var Loaded = React.createClass({
    render: function(){
        return (<div>
                <h4>Stages UTC <small>{this.props.data.length} stages</small></h4>
                <hr/>
                <FilterTable data={this.props.data}/>
        </div>)
    }
})