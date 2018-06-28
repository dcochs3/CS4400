var allFilters = document.getElementsByClassName("panel");
var prop = "(all prop types); ";
var costume = "(all costume types); ";
var timePeriod = "(all time periods); ";
var region = "(all regions); ";
var sex = "(all sexes); ";
var color = "(all colors); ";
var size = "(all sizes); ";
var condition = "(all conditions); ";
var availability = "(all availabilities); ";

// Update the homepage's text representing the current filters
function updateFiltersList() {
    // Loop through all the filters and check the checked checkboxess
    for (var i = 0; i < allFilters.length; i++) {
        updateFilterSelection(i);
    }
    // Update the homepage text
    document.getElementById("current-filters").innerHTML = "Filtering by: " + prop + costume + timePeriod + region + sex + color + size + condition + availability;
}

// Update a specific filter section (e.g. color, size, condition) based on the currently selected checkboxes
function updateFilterSection(i) {
    var resultingString = "";
    
    var currFilters = "";
    var currType = document.getElementById(allFilters[i].id).getElementsByTagName('input');
    
    var allFiltersString;
    switch (i) {
        case 0:
            allFiltersString = "(all prop types)";
            break;
        case 1:
            allFiltersString = "(all costume types)";
            break;
        case 2: 
            allFiltersString = "(all time periods)";
            break;
        case 3:
            allFiltersString = "(all regions)";
            break;
        case 4:
            allFiltersString = "(all sexes)";
            break;
        case 5:
            allFiltersString = "(all colors)";
            break;
        case 6:
            allFiltersString = "(all sizes)";
            break;
        case 7:
            allFiltersString = "(all conditions)";
            break;
        case 8:
            allFiltersString = "(all availabilities)";
            break;
    }
    
    var count = 0;
    for (var j = 0; j < currType.length; j++) {
        if (currType[j].checked) {
            if (count == 0) {
                currFilters += currType[j].nextSibling.nodeValue.trim();
            } else {
                currFilters += ", " + currType[j].nextSibling.nodeValue.trim();
            }
            count++;
        }
    }
    if (count != 0) {
        if (count == currType.length) {
            resultingString += allFiltersString + "; ";
        } else {
            resultingString += currFilters + "; ";
        }
    }
    
    switch (i) {
        case 0:
            prop = resultingString;
            break;
        case 1:
            costume = resultingString;
            break;
        case 2: 
            timePeriod = resultingString;
            break;
        case 3:
            region = resultingString;
            break;
        case 4:
            sex = resultingString;
            break;
        case 5:
            color = resultingString;
            break;
        case 6:
            size = resultingString;
            break;
        case 7:
            condition = resultingString;
            break;
        case 8:
            availability = resultingString;
            break;
    }
}
