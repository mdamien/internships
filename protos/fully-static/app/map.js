var Map = React.createClass({
    componentDidMount: function() {
        var map = this.map = L.map(this.getDOMNode(), {
            minZoom: 2,
            maxZoom: 20,
            layers: [
                L.tileLayer(
                    'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
                    {attribution: ''})
            ],
            attributionControl: false,
        });

        var markers = L.markerClusterGroup({});
        var count_bad = 0,count_good = 0;
        this.props.data.forEach(function(x){
            if(x.lat == ""){
                count_bad += 1;
            }else{
                var m = L.marker(L.latLng(x.lat, x.lng))
                    .bindPopup(x.sujet);
                markers.addLayer(m);
                count_good += 1
            }
        });
        map.addLayer(markers);

        map.on('click', this.onMapClick);
        map.fitWorld();
    },
    componentWillUnmount: function() {
        this.map.off('click', this.onMapClick);
        this.map = null;
    },
    onMapClick: function() {
        // Do some wonderful map things...
    },
    render: function() {
        var style = {
            height:"400px",
            width:"100%",
        }
        return (
            <div style={style}></div>
        );
    }
});