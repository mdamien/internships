Table = React.createClass({
  handleSelected: function(x){
      this.props.onSelected(x);
  },
  render: function(){
    var LIMIT = 200;
    var tr_style = {
        cursor:'pointer',
    }
    var rows = this.props.data.slice(0,LIMIT).map(function(x){
        var klass = "";
        if(!x.done){
            klass = "warning"
        }
        if(this.props.selected && this.props.selected.id == x.id){
            klass = "success"
        }
        if(x.confidentiel){
            klass = "danger"
        }
        infos =  (<tr style={tr_style} key={x.id} onClick={this.handleSelected.bind(null,x)} className={klass}>
            <td>{x.semestre}{x.semestre_annee} {x.niveau_abbrev} {x.branche_abbrev}</td>
            <td>{x.sujet}</td>
            <td><b>{x.company}</b></td>
            <td>{x.city} {x.country
            }</td>
            </tr>)
        return infos;
    }.bind(this))
    return (
        <table className="table table-condensed table-hover table-striped">
        <thead>
        <tr>
            <th className="col-md-1"></th>
            <th className="col-md-4">Sujet</th>
            <th className="col-md-3">Entreprise</th>
            <th className="col-md-3">Addresse</th>
        </tr>
        </thead>
        <tbody>
        {rows}
        <tr><th colSpan="4">{this.props.data.length > LIMIT ?  "..." : ''}</th></tr>

        </tbody>
        </table>
        )
}
})