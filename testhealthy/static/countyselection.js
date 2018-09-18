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

    // function to populate county data based on dynamic selection of state

    populatecounty(statedata);

    Plotly.d3.select('#countyselect').on('change',(function(){
    countydata = this.options[this.selectedIndex].value;
    
    // function to populate county ranking  based on dynamic selection of state and county

    populatecountydetails(statedata,countydata)
    })
  )
});

// populatechart()

// begin function populatecounty(statename) 

function populatecounty(statename) {

    var countyurl = `/countynames/${statename}`
    
    Plotly.d3.json(countyurl, function(error, selectcounty) { 
  
    if (error) {
      return console.warn(error);
    }
  
  
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
  console.log(countydata)
  console.log(statedata)
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

        console.log(data_list)

    })

}

