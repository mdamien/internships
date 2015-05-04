var Table = React.createClass({
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
        var indicator = "";
        if(!x.done){
            indicator = (<span className="glyphicon glyphicon-warning-sign" aria-hidden="true"
                    title="Sujet non pris"></span>)
        }
        if(x.confidentiel){
            indicator = (<span className="glyphicon glyphicon-eye-close" aria-hidden="true"
                title="Sujet confidentiel"></span>)
        }
        if(this.props.selected && this.props.selected.id == x.id){
            klass = "success"
        }
        infos =  (<tr style={tr_style} key={x.id} onClick={this.handleSelected.bind(null,x)} className={klass}>
            <td>{indicator} {x.semestre}{x.semestre_annee} {x.niveau_abbrev} {x.branche_abbrev}
            </td>
            <td>{x.sujet}</td>
            <td><b>{x.company}</b></td>
            <td>{x.city} {x.country
            }</td>
            </tr>)
        return infos;
    }.bind(this))
    var extra_row = "";
    if(this.props.data.length > LIMIT){
        extra_row = <tr><th colSpan="4">...</th></tr>
    }
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
        {extra_row}
        </tbody>
        </table>
        )
}
})