 
function init() {

    // Use the list of sample names to populate the select options
    d3.json("/states").then((data) => {
  
    // Use d3 to select the panel with id of `#sample-metadata`
    var selector = d3.select("#stateselect");
      
    // Use `.html("") to clear any existing metadata
    // document.querySelector("#stateselect").innerHTML = "";


  // console.log(data[0].States);
    console.log("For each state")
    data[0].States.forEach((state) => {
      console.log(state);
      // return state;
      selector
      .append("option")
      .text(state)
      .property("value", state);
  })
});

}
// Initialize the dashboard

init();