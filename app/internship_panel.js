var InternshipPanel = React.createClass({

    render: function(){
      var style = {
        position: 'fixed',
        top:'30',
        right:'40',
        width: '30%',
        minWidth: '300',
        maxWidth: '700',
        maxHeight: '80%',
        overflow: 'auto',
      }
      var content_style = {
      }
      var content = {__html:this.props.selected.description.replace('\n','<br/>')}
      return (<div className="panel panel-success" style={style}>
                    <div className="panel-heading">
                      <h3 className="panel-title">{this.props.selected.sujet}</h3>
                      <button className="btn btn-default pull-right"
                        onClick={this.props.onClose}>fermer</button>
                    </div>
                    <div className="panel-body">
                      <br/>
                      <div style={content_style} dangerouslySetInnerHTML={content}></div>
                      <hr/>
                      <pre>
                      {JSON.stringify(this.props.selected, null, 2)}
                      </pre>
                    </div>
                </div>);
    }
})