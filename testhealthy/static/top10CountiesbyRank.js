// A javascript to get the top 10 counties based on the health factors mentioned
// in the County Health Rankings Model by UWPHI.
var stateselector = d3.select('#stateselect2');

d3.json("/states").then((Data) => {
    Object.entries(Data).forEach(([key,value])=>{
        Object.entries(value).forEach(([key,value])=>{
            value.forEach((data)=>{
                stateselector.append("option").text(data).property("value",data)
            })
        });   
    });
});  

$('#stateselect2').change(function(){
    var statedata2 = $(this).val()
    populatetable(statedata2)
});

function populatetable(statedata2){
    var table = d3.select("#county-background2");
    var tbody = table.select("tbody")
    tbody.html(" ");
    var rankurl = `/countyrankszscores/${statedata2}`
    var Countyrank={}
    var countylist = []
    d3.json(rankurl).then((Data) =>{
        Data.forEach((data)=>{
            Object.entries(data).forEach(([key,value])=>{
                value.forEach((item)=>{
                    CountyName = item['County']
                    CountyRank = item['Rank']
                    if (CountyRank <= 10){
                        Countyrank[CountyName] = CountyRank
                    }       
                })
                var orderedarray = [1,2,3,4,5,6,7,8,9,10]
                orderedarray.forEach((data)=>{
                    Object.entries(Countyrank).forEach(([key,value])=>{
                        if (data == value){
                            countylist.push(key)
                        }
                    })
                })
            })
        })
//Inserting rows in the table for top 10 counties
        $.each(countylist, function (index, value) {
            var row = tbody.append("tr")
            row.append("td").text(value)
            row.append("td").text(index+1)   
        }) 
//Inserting plot for top 10 counties        
        // var Rank = [1,2,3,4,5,6,7,8,9,10]
        
        // console.log(d3.max(Rank))
        // var revRank = []
        // Rank.forEach((data)=>{
        //   revRank.push((d3.max(Rank)-data)+1)
        // })
        // console.log(revRank)
        // // svg container
        // var svgHeight = 400;
        // var svgWidth = 1000;
        
        // // margins
        // var margin = {
        //   top: 50,
        //   right: 50,
        //   bottom: 50,
        //   left: 50
        // };
        
        // // chart area minus margins
        // var chartHeight = svgHeight - margin.top - margin.bottom;
        // var chartWidth = svgWidth - margin.left - margin.right;
        
        // // create svg container
        // var svg = d3.select("#top10counties").append("svg")
        //   .attr("height", svgHeight)
        //   .attr("width", svgWidth);
        
        // // shift everything over by the margins
        // var chartGroup = svg.append("g")
        //   .attr("transform", `translate(${margin.left}, ${margin.top})`);
        
        // // scale y to chart height
        // var yScale = d3.scaleLinear()
        //   .domain([(d3.max(Rank)+1),1])
        //   .range([chartHeight, 0]);
        
        // // scale x to chart width
        // var xScale = d3.scaleBand()
        //   .domain(countylist)
        //   .range([0, chartWidth])
        //   .padding(0.05);
        
        // // create axes
        // var yAxis = d3.axisLeft(yScale);
        // var xAxis = d3.axisBottom(xScale);
        
        // // set x to the bottom of the chart
        // chartGroup.append("g")
        //   .attr("transform", `translate(0, ${chartHeight})`)
        //   .call(xAxis);
        
        // // set y to the y axis
        // // This syntax allows us to call the axis function
        // // and pass in the selector without breaking the chaining
        // chartGroup.append("g")
        //   .call(yAxis);
        
        // /* Note: The above code is equivalent to this:
        //     var g = chartGroup.append("g");
        
        //     yAxis(g);
        // */
        // // Append Data to chartGroup
        // chartGroup.selectAll(".bar")
        //   .data(Rank)
        //   .enter()
        //   .append("rect")
        //   .classed("bar", true)
        //   .attr("x", (d, i) => xScale(countylist[i]))
        //   .attr("y", d => yScale(d))
        //   .attr("width", xScale.bandwidth())
        //   .attr("height", d => chartHeight - yScale(d));   
    })  
};
