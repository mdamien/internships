Filters = React.createClass({
  handleTextFilterChange: function(){
    var filters = this.props.filters;
    filters.text = this.refs.text.getDOMNode().value;
    this.props.onUpdate(filters);
  },
  handleTypeChange: function(){
    var filters = this.props.filters;
    filters.type = this.refs.type.getDOMNode().value;
    this.props.onUpdate(filters);
  },
  handleBranchChange: function(){
    var filters = this.props.filters;
    filters.branch = this.refs.branch.getDOMNode().value;
    this.props.onUpdate(filters);
  },
  handleDisplayNotRealChange: function(evt){
    var filters = this.props.filters;
    filters.hide_not_real = evt.target.checked;
    this.props.onUpdate(filters);
  },
  handleFromChange: function(evt){
    var filters = this.props.filters;
    filters.from = this.refs.from.getDOMNode().value;
    this.props.onUpdate(filters);
  },
  handleToChange: function(evt){
    var filters = this.props.filters;
    filters.to = this.refs.to.getDOMNode().value;
    this.props.onUpdate(filters);
  },
  render:function() {
    var date_min = "A2002";
    var date_max = "A2015";
    var dates = []
    for(var year = 2002; year <= 2015; year++){
      dates.push('P'+year);
      dates.push('A'+year);
    }
    var options = dates.map(function(d,i){
        return <option value={d} key={i}>{d}</option>
    })
    return (
      <div className="form-inline row">
      <div className="form-group col-md-2">
        <input className="form-control" name="text" type="text" ref="text"
          onChange={this.handleTextFilterChange}
          placeholder="Rechercher..." value={this.props.filters.text}/>
      </div>
      <div className="form-group col-md-2">
      <label htmlFor="internship_type">type</label>
      <select name="internship_type" className="form-control" defaultValue="all" ref="type"
        onChange={this.handleTypeChange} >
        <option value="all">Tous</option>
        <option value="TN05">TN05</option>
        <option value="TN09">TN09</option>
        <option value="TN10">TN10</option>
        <option value="apprentissage">Apprentissage</option>
        <option value="interculturel">Interculturel</option>
      </select>
      </div>
      <div className="form-group col-md-2">
      <label htmlFor="branch">Branche</label>
      <select name="branch" className="form-control" defaultValue="all"
        onChange={this.handleBranchChange} ref="branch">
        <option value="all">Toutes</option>
        <option value="GB">GB</option>
        <option value="GI">GI</option>
        <option value="GM/GSM">GM/GSM</option>
        <option value="GP">GP</option>
        <option value="GSU">GSU</option>
      </select>
      </div>
      <div className="checkbox checkbox-inline col-md-2">
        <label>
          <input type="checkbox" defaultChecked={false}
            onChange={this.handleDisplayNotRealChange} /> Cacher stages non fait
        </label>
      </div>
      <div className="form-group col-md-2">
      <label htmlFor="from">De</label>
      <select name="from" className="form-control" defaultValue={date_min} ref="from"
        onChange={this.handleFromChange}>
        {options}
      </select>
      </div>
      <div className="form-group col-md-2">
      <label htmlFor="to">A</label>
      <select name="to" className="form-control" defaultValue={date_max} ref="to"
        onChange={this.handleToChange}>
        {options}
      </select>
      </div>
      </div>
      );
}
})