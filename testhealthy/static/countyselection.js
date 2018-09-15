console.log("this has loaded")
 
function init() {

    var selector = d3.select("#stateselect");
  
    // Use the list of sample names to populate the select options
    d3.json("/states").then((sampleNames) => {
    console.log(sampleNames);
   sampleNames.forEach((sample) => {
     selector
       .append("option")
       .text(sample)
       .property("value", sample);
   })
   
   })
};


// Initialize the dashboard

init();


