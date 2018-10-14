function drawInfoWindow(property) {
    let id = '';
    if (property.id) {
        id = property.id
    }

    let image = '/static/img/logo.png';
    if (property.image) {
        image = property.image
    }

    let name = '-';
    if (property.name) {
        name = property.name
    }

    let address = '-';
    if (property.address) {
        address = property.address
    }

    let licence = '';
    if (property.licence) {
        licence = '<span><i class="flaticon-building"></i>' + property.licence + '</span>'
    }

    let school_type = '';
    if (property.school_type) {
        school_type = '<span><i class="flaticon-security"></i>' + property.school_type + '</span>'
    }

    let station_info = '';
    if (property.station_info) {
        station_info = property.station_info
    }

    let free_num_not_one = '';
    if (property.free_num_not_one > 0) {
        free_num_not_one = '<span><i class="flaticon-people-1"></i> 0歳空き有 </span>'
    }

    let free_num_one_year_old = '';
    if (property.free_num_one_year_old > 0) {
        free_num_one_year_old = '<span><i class="flaticon-people-1"></i> 1歳空き有 </span>'
    }

    let free_num_two_year_old = '';
    if (property.free_num_two_year_old > 0) {
        free_num_two_year_old = '<span><i class="flaticon-people-1"></i> 2歳空き有 </span>'
    }

    let free_num_three_year_old = '';
    if (property.free_num_three_year_old > 0) {
        free_num_three_year_old = '<span><i class="flaticon-people-1"></i> 3歳空き有 </span>'
    }

    let free_num_four_year_old = '';
    if (property.free_num_four_year_old > 0) {
        free_num_four_year_old = '<span><i class="flaticon-people-1"></i> 4歳空き有 </span>'
    }

    let free_num_extent = '';
    if (property.free_num_extent) {
        free_num_extent = '<span><i class="flaticon-people-1"></i> 延長空き有 </span>'
    }

    let stable_food = '';
    if (property.stable_food) {
        stable_food = '<span><i class="flaticon-park"></i> 主食有 </span>'
    }

    let temporary_childcare = '';
    if (property.temporary_childcare) {
        temporary_childcare = '<span><i class="flaticon-summer"></i> 一時受け入れ有 </span>'
    }

    let overnight_childcare = '';
    if (property.overnight_childcare) {
        overnight_childcare = '<span><i class="flaticon-clock"></i> 夜間受け入れ有 </span>'
    }

    let allday_childcare = '';
    if (property.allday_childcare) {
        allday_childcare = '<span><i class="flaticon-holidays"></i> 日中受け入れ有 </span>'
    }

    let evaluation = '';
    if (property.evaluation) {
        evaluation = '<span><i class="flaticon-people"></i> 第三者評価認証済 </span>'
    }

    let ibContent = '';
    ibContent =
        "<div class='map-properties'>" +
        "<div class='map-img'>" +
        "<img src='" + image + "'/>" +
        "</div>" +
        "<div class='map-content'>" +
        "<h4><a href='#'>" + name + "</a></h4>" +
        "<p class='address'> <i class='fa fa-map-marker'></i>" + address + "</p>" +
        "<p class='description'>最寄り " + station_info + "</p>" +
        "<div class='map-properties-fetures'> " +
        licence +
        school_type +
        free_num_not_one +
        free_num_one_year_old +
        free_num_two_year_old +
        free_num_three_year_old +
        free_num_four_year_old +
        free_num_extent +
    "</div>" +
    "<div class='map-properties-fetures'> " +
    stable_food +
    temporary_childcare +
    overnight_childcare +
    allday_childcare +
    evaluation +
    "</div>" +
    "<div class='map-properties-btns'><a href='/nursery/" + id + "' class='button-sm button-theme' target='_blank'>詳細情報</a></div>" +
    "</div>";
    return ibContent;
}

function insertPropertyToArray(property, layout) {
    let id = '';
    if (property.id) {
        id = property.id
    }

    let image = '/static/img/logo.png';
    if (property.image) {
        image = property.image
    }

    let name = '-';
    if (property.name) {
        name = property.name
    }

    let address = '-';
    if (property.address) {
        address = property.address
    }

    let licence = '';
    if (property.licence) {
        licence = '<li><i class="flaticon-building"></i><span>' + property.licence + '</span></li>'
    }

    let school_type = '';
    if (property.school_type) {
        school_type = '<li><i class="flaticon-security"></i><span>' + property.school_type + '</span></li>'
    }

    let station_info = '';
    if (property.station_info) {
        station_info = property.station_info
    }

    let free_num_not_one = '';
    if (property.free_num_not_one > 0) {
        free_num_not_one = '<li><i class="flaticon-people-1"></i><span> 0歳空き有 </span></li>'
    }

    let free_num_one_year_old = '';
    if (property.free_num_one_year_old > 0) {
        free_num_one_year_old = '<li><i class="flaticon-people-1"></i><span>1歳空き有 </span></li>'
    }

    let free_num_two_year_old = '';
    if (property.free_num_two_year_old > 0) {
        free_num_two_year_old = '<li><i class="flaticon-people-1"></i><span>2歳空き有</span> </li>'
    }

    let free_num_three_year_old = '';
    if (property.free_num_three_year_old > 0) {
        free_num_three_year_old = '<li><i class="flaticon-people-1"></i><span>3歳空き有</span> </li>'
    }

    let free_num_four_year_old = '';
    if (property.free_num_four_year_old > 0) {
        free_num_four_year_old = '<li><i class="flaticon-people-1"></i><span>4歳空き有 </span></li>'
    }

    let free_num_extent = '';
    if (property.free_num_extent) {
        free_num_extent = '<li><i class="flaticon-people-1"></i><span>延長空き有</span></li>'
    }

    let stable_food = '';
    if (property.stable_food) {
        stable_food = '<li><i class="flaticon-park"></i><span>主食有</span></li>'
    }

    let temporary_childcare = '';
    if (property.temporary_childcare) {
        temporary_childcare = '<li><i class="flaticon-summer"></i><span>一時預かり有</span></li>'
    }

    let overnight_childcare = '';
    if (property.overnight_childcare) {
        overnight_childcare = '<li><i class="flaticon-clock"></i><span>夜間預かり有</span></li>'
    }

    let allday_childcare = '';
    if (property.allday_childcare) {
        allday_childcare = '<li><i class="flaticon-holidays"></i><span>日中預かり有</span></li>'
    }

    let evaluation = '';
    if (property.evaluation) {
        evaluation = '<li><i class="flaticon-people"></i><span>認証済</span></li>'
    }

    let free_num_updated_at = '';
    if (property.free_num_updated_at) {
        free_num_updated_at = property.free_num_updated_at
    }

    var element = '';

    if (layout == 'grid_layout') {
        element = '<div class="col-lg-6 col-md-6 col-sm-6 col-xs-12"><div class="property">' +
            '<!-- Property img --> ' +
            '<a href="/nursery/' + id + '" class="property-img" target="_blank">' +
            '<div class="property-tag button sale">' + image + '</div> ' +
            '<img src="' + image + '" alt="properties-3" class="img-responsive"> ' +
            '</a>' +
            '<!-- Property content --> ' +
            '<div class="property-content"> ' +
            '<!-- title --> ' +
            '<h1 class="title">' +
            '<a href="/nursery/' + id + '" target="_blank">' + name + '</a> ' +
            '</h1> ' +
            '<!-- Property address --> ' +
            '<h3 class="property-address"> ' +
            '<a href=""> ' +
            '<i class="fa fa-map-marker"></i>' + address + ' ' +
            '</a> ' +
            '</h3> ' +
            '<!-- Property description --> ' +
            "<p>最寄り駅: " + station_info + "</p>" +
            '<!-- Facilities List --> ' +
            '<ul class="facilities-list clearfix"> ' +
            licence +
            school_type +
            free_num_not_one +
            free_num_one_year_old +
            free_num_two_year_old +
            free_num_three_year_old +
            free_num_four_year_old +
            free_num_extent +
            stable_food +
            temporary_childcare +
            overnight_childcare +
            allday_childcare +
            evaluation +
            '</ul> ' +
            '<!-- Property footer --> ' +
            '<div class="property-footer"> ' +
            '<span class="right"> ' +
            '<i class="fa fa-calendar"></i>' + free_num_updated_at +
            '</span> ' +
            '</div>' +
            '</div>' +
            '</div>';
    }
    else {
        element = '' +
            '<div class="property map-properties-list clearfix"> ' +
            '<div class="col-lg-5 col-md-5 col-sm-5 col-xs-12 col-pad"> ' +
            '<a href="properties-details.html" class="property-img height"> ' +
            '<div class="property-tag button sale">' + image + '</div> ' +
            '<img src="' + image + '" alt="properties" class="img-responsive img-inside-map"> ' +
            '</a> ' +
            '</div> ' +
            '<div class="col-lg-7 col-md-7 col-sm-7 col-xs-12 property-content "> ' +
            '<!-- title --> ' +
            '<h1 class="title"> ' +
            '<a href="">' + name + '</a> </h1> ' +
            '<!-- Property address --> ' +
            '<h3 class="property-address"> ' +
            '<a href=""> ' +
            '<i class="fa fa-map-marker"></i>' + address + ', ' +
            '</a>' +
            '</h3>' +
            '<!-- Property description --> ' +
            "<p>最寄り " + station_info + "</p>" +
            '<!-- Facilities List --> ' +
            '<ul class="facilities-list clearfix"> ' +
            licence +
            school_type +
            free_num_not_one +
            free_num_one_year_old +
            free_num_two_year_old +
            free_num_three_year_old +
            free_num_four_year_old +
            free_num_extent +
            stable_food +
            temporary_childcare +
            overnight_childcare +
            allday_childcare +
            evaluation +
            '</ul> ' +
            '<!-- Property footer --> ' +
            '<div class="property-footer"> ' +
            '<span class="right"> ' +
            '<i class="fa fa-calendar"></i>' + free_num_updated_at +
            '</span> ' +
            '</div> ' +
            '</div> ' +
            '</div>';
    }
    return element;
}

function animatedMarkers(map, propertiesMarkers, properties, layout) {
    var bounds = map.getBounds();
    var propertiesArray = [];
    $.each(propertiesMarkers, function (key, value) {
        if (bounds.contains(propertiesMarkers[key].getLatLng())) {
            propertiesArray.push(insertPropertyToArray(properties.data[key], layout));
            setTimeout(function () {
                if (propertiesMarkers[key]._icon != null) {
                    propertiesMarkers[key]._icon.className = 'leaflet-marker-icon leaflet-zoom-animated leaflet-clickable bounce-animation marker-loaded';
                }
            }, key * 50);
        }
        else {
            if (propertiesMarkers[key]._icon != null) {
                propertiesMarkers[key]._icon.className = 'leaflet-marker-icon leaflet-zoom-animated leaflet-clickable';
            }
        }
    });
    $('.fetching-properties').html(propertiesArray);
}

function generateMap(latitude, longitude, mapProvider, layout, properties, zoom) {

    var map = L.map('map', {
        center: [latitude, longitude],
        zoom: zoom,
        scrollWheelZoom: false
    });

    L.tileLayer.provider(mapProvider).addTo(map);
    var markers = L.markerClusterGroup({
        showCoverageOnHover: false,
        disableClusteringAtZoom: 17,
        zoomToBoundsOnClick: true
    });
    var propertiesMarkers = [];

    $.each(properties.data, function (index, property) {
        var icon = '<img src="/static/img/logos/school.png">';
        if (property.type_icon) {
            icon = '<img src="' + property.type_icon + '">';
        }
        var color = '';
        var markerContent =
            '<div class="map-marker ' + color + '">' +
            '<div class="icon">' +
            icon +
            '</div>' +
            '</div>';

        var _icon = L.divIcon({
            html: markerContent,
            iconSize: [36, 46],
            iconAnchor: [18, 32],
            popupAnchor: [130, -28],
            className: ''
        });

        var marker = L.marker(new L.LatLng(property.latitude, property.longitude), {
            title: property.title,
            icon: _icon
        });

        propertiesMarkers.push(marker);
        marker.bindPopup(drawInfoWindow(property));
        markers.addLayer(marker);
        marker.on('popupopen', function () {
            this._icon.className += ' marker-active';
        });
        marker.on('popupclose', function () {
            this._icon.className = 'leaflet-marker-icon leaflet-zoom-animated leaflet-clickable marker-loaded';
        });
    });

    map.addLayer(markers);
    animatedMarkers(map, propertiesMarkers, properties, layout);
    map.on('moveend', function () {
        animatedMarkers(map, propertiesMarkers, properties, layout);
    });

    $('.fetching-properties .item').hover(
        function () {
            propertiesMarkers[$(this).attr('id') - 1]._icon.className = 'leaflet-marker-icon leaflet-zoom-animated leaflet-clickable marker-loaded marker-active';
        },
        function () {
            propertiesMarkers[$(this).attr('id') - 1]._icon.className = 'leaflet-marker-icon leaflet-zoom-animated leaflet-clickable marker-loaded';
        }
    );

    $('.geolocation').on("click", function () {
        map.locate({setView: true})
    });
    $('#map').removeClass('fade-map');
}