// variables for drop down menu for state and county selection

var stateurl = '/states';
var statedata;
var countydata;

// load state drop down from Flask Route

Plotly.d3.json(stateurl,function(error,statedata){
  if (error) {
    return console.warn(error);
};

  statedata[0].States.forEach(function(name) {
  Plotly.d3
      .select("#stateselect")
      .append('option')
      .attr('value', name)
      .attr('class', 'dropdown')
      .text(name)
});

})

// action on event change on state drop down and county

 $("#stateselect").change( function(){
    statedata = $(this).val();
    $("#countyselect").empty();
    $("#count").empty();


    // function to populate county data based on dynamic selection of state

    populatecounty(statedata);

    Plotly.d3.select('#countyselect').on('change',(function(){
    countydata = this.options[this.selectedIndex].value;
    
    // function to populate county ranking  based on dynamic selection of state and county

    populatecountydetails(statedata,countydata)

    })
  )
});


// begin function populatecounty(statename) 

function populatecounty(statename) {

    var countyurl = `/countynames/${statename}`
    
    Plotly.d3.json(countyurl, function(error, selectcounty) { 
  
    if (error) {
      return console.warn(error);
    }
  
    document.getElementById("count").innerHTML+= "Total Number of Counties: " + selectcounty[0].CountyNames.length
   
    selectcounty[0].CountyNames.forEach(function(name) {
      Plotly.d3
          .select("#countyselect")
          .append('option')
          .attr('value', name)
          .attr('class', 'dropdown')
          .text(name)
    })
    
    })
}

// end function populatecounty(statename) 


// begin function populatecountydetails(statedata,countydata)

function  populatecountydetails(statedata,countydata){    
    var table = Plotly.d3.select("#county-background");
    var tbody = table.select("tbody");

    var data_list = [];

    var countyinfo = `/countyalldetails/${statedata}`

    Plotly.d3.json(countyinfo, function(error, county) {

      if (error) {
        return console.warn(error);
        
      }

      var countyattributerank = county[0].Counties.filter(function(name){
        return name.County.CountyName == countydata;
      })


      var attr_c = ["ClinicalCare","EconomicFactors","HealthBehaviours","PhysicalEnvironment","QualityofLife"]

      for(var i =0; i <attr_c.length;i++){

          var county_label = attr_c[i]
          var county_label_rank = countyattributerank[0].County[attr_c[i]]["Rank"]
          var county_row = [county_label,county_label_rank]
          data_list.push(county_row);
          $("tbody").empty();
          var rows = tbody.selectAll('tr')
          .data(data_list)
          .enter()
          .append('tr')
          .html(function(d){
              return `<td>${d[0]}</td><td>${d[1]}</td>`
          })  

        }

      // end function populatecountydetails(statedata,countydata)

    })

}


  // API key
  const API_KEY = "pk.eyJ1Ijoic3NhdHBhdGh5IiwiYSI6ImNqbGVjb2I2NzBrbmIzcXBtMDdsOHp5aDcifQ.HCxHkdXAzE7YAK_FCbdUXQ";





  // Creating our initial map object
  // We set the longitude, latitude, and the starting zoom level
  // This gets inserted into the div with an id of 'map'


  var myMap = L.map("map", {
    center: [40.7128, -74.0059],
    zoom: 6 })

  L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
      attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
      maxZoom: 18,
      id: "mapbox.streets",
      accessToken: API_KEY
    }).addTo(myMap);
  
      
    // click circle:

    var clickCircle;

    var RankMarkers = [];


    $(document).ready(function(){ 
        
              $('#stateselect').change(function(){ 
                var mapstate = $(this).val();
                populatemap(mapstate) 
              });

    });


    function markerSize(population) {
      return population / 40; 
    }


    var attr_choice

    console.log(attr_choice)

    $("#attributerank").change(function (){
      attr_choice = ""
      attr_choice = $(this).val()
      console.log(attr_choice)
      return attr_choice
    })

    // console.log(attr_choice)

    // var a1 = document.getElementById("attributerank");
    // var a_1 = a1.options[a1.selectedIndex].value;

    // var a2 = document.getElementById("attributerank");
    // var a_2 = a2.options[a2.selectedIndex].text;

    // var a3 = $("#attributerank :selected").text(); // The text content of the selected option
    // var a4 = $("#attributerank").val(); // The value of the selected option


    // console.log(a1)
    // console.log(a_1)
    // console.log(a2)
    // console.log(a_2)
    // console.log(a3)
    // console.log(a4)

    function populatemap(mapstate){  

      // An array which will be used to store created cityMarkers

      if (clickCircle != undefined || clickCircle != null) {
        myMap.removeLayer(clickCircle);
      };

      var mapurl = `/countyalldetails/${mapstate}`

      Plotly.d3.json(mapurl, function(error, response){

        if (error) {
          return console.warn(error);
        }

        var county_specs = response[0].Counties

        for (var i = 0; i < county_specs.length; i++) {


          // Conditionals for county population
          var color = "";
          
          var area = parseFloat(county_specs[i].County.TotalArea)
          var population = parseInt(county_specs[i].County.Population)
          var population_approx = population * 1000
          var latitude = (county_specs[i].County.Latitude).split("°")
          var longitude = (county_specs[i].County.Longitude).split("°")
          var longitude_1 = longitude[0].split("–");
          var lat = parseFloat(latitude[0])
          var lon = parseFloat(longitude_1[1])

          var location = [lat,-lon]

          if(attr_choice != undefined) 
          {
              var attr_rank_join = attr_choice.split(" ").join("")

              if( county_specs[i].County[attr_rank_join]["Rank"] == 1 || 
                  county_specs[i].County[attr_rank_join]["Rank"] == 2 || 
                  county_specs[i].County[attr_rank_join]["Rank"] == 3)
              {
                L.marker(location)
                .bindPopup(attr_choice + ":" + county_specs[i].County[attr_rank_join]["Rank"] 
                                + "<hr> <h6>" + "County Name: " + county_specs[i].County.CountyName + "</h6>")
                .addTo(myMap);
              }
          }

          // var rankLayer = L.layerGroup(RankMarkers);

          // Overlays that may be toggled on or off

          // var overlayMaps = {
          //   Top_3: rankLayer
          // };


          if (population_approx > 600000) {
            color = "red";
          } else if (population_approx < 500000 && population_approx > 300000 ){
            color = "green";
          }
          else {
            color = "yellow";
          }    
          
          // Add circles to map
          clickCircle = L.circle(location, {
            fillOpacity: 0.5,
            color: "white",
            fillColor: color,
            // Adjust radius
            radius: markerSize(population_approx)
          }).bindPopup("<h5> County Name: " + county_specs[i].County.CountyName + "</h5> <hr> <h6> Quality of Life: " + 
                                                        county_specs[i].County["QualityofLife"]["Rank"] + 
                                                        "<hr> Clinical Care: " + county_specs[i].County["ClinicalCare"]["Rank"] + 
                                                        "<hr> Economic Factors: " + county_specs[i].County["EconomicFactors"]["Rank"] +
                                                        "<hr> Health Behaviours: " + county_specs[i].County["HealthBehaviours"]["Rank"] +
                                                        "<hr> Physical Environment: " + county_specs[i].County["PhysicalEnvironment"]["Rank"] +"</h6")
            .addTo(myMap);

        }

      })

      if(mapstate == "California"){
        myMap.setView([36.7783,-119.4179],6)
      } else if(mapstate == "Alaska"){
        myMap.setView([64.2008,-149.4937],4)
      }
      else {
        myMap.setView([40.7128,-74.0060],6)
      }

      // Pass our map layers into our layer control
      // Add the layer control to the map
      // L.control.layers(overlayMaps).addTo(myMap);

    }

    




  
