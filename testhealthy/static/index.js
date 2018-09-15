function add_dropdown(){ 
    

    Plotly.d3.json("/names",function(error,response){
        if(error) console.warn(error);

        var dropdown_select = Plotly.d3.select("#selDataset");

       for(var i=0;i<response.length;i++){
           dropdown_select.append("option").attr("value",response[i]).text(response[i]);
       }
       optionChanged(response[0]);
    })

    
}

function optionChanged(selectedValue){
  
    Plotly.d3.json("/metadata/"+selectedValue,function(error,response){
        if(error) console.warn(error);

        var metadata_Sample= Plotly.d3.select(".metadata");

        // Remove Old metadata 
        metadata_Sample.selectAll("p").remove();

        for(var key in response){
            if(response.hasOwnProperty(key)){
                metadata_Sample.append("p").text(key + ":   " + response[key]);
            }
        }
    })

};

add_dropdown()