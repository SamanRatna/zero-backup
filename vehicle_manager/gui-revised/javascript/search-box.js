// ARRAY FOR HEADER.
var arrHead = new Array();
arrHead = ['places'];      // SIMPLY ADD OR REMOVE VALUES IN THE ARRAY FOR TABLE HEADERS.

// FIRST CREATE A TABLE STRUCTURE BY ADDING A FEW HEADERS AND
// ADD THE TABLE TO YOUR WEB PAGE.
function createTable() {
    var empTable = document.createElement('table');
    empTable.setAttribute('id', 'empTable');            // SET THE TABLE ID.

    var tr = empTable.insertRow(-1);

    // for (var h = 0; h < arrHead.length; h++) {
    //     var th = document.createElement('th');          // TABLE HEADER.
    //     th.innerHTML = arrHead[h];
    //     tr.appendChild(th);
    // }

    var div = document.getElementById('search-suggestions');
    div.appendChild(empTable);    // ADD THE TABLE TO YOUR WEB PAGE.
}
let suggestionsField = document.getElementById('search-suggestions');
// ADD A NEW ROW TO THE TABLE.s
function addRow(data) {
    var empTab = document.getElementById('empTable');

    var rowCnt = empTab.rows.length;        // GET TABLE ROW COUNT.
    var tr = empTab.insertRow(rowCnt);      // TABLE ROW.
    tr = empTab.insertRow(rowCnt);

    for (var c = 0; c < arrHead.length; c++) {
        var td = document.createElement('td');          // TABLE DEFINITION.
        td = tr.insertCell(c);

            // CREATE AND ADD TEXTBOX IN EACH CELL.
            var ele = document.createElement('P');
            ele.innerText = data
            ele.setAttribute('style','font-size: 40px');
            ele.setAttribute('white-space', 'nowrap');
            td.appendChild(ele);
            console.log(suggestionsField.style.height);
            suggestionsField.style.height = (suggestionsField.style.height + 100) + 'px';
    }
}

// DELETE TABLE ROW.
function removeRow(oButton) {
    var empTab = document.getElementById('empTable');
    empTab.deleteRow(oButton.parentNode.parentNode.rowIndex);       // BUTTON -> TD -> TR.
}

// EXTRACT AND SUBMIT TABLE DATA.
function submit() {
    var myTab = document.getElementById('empTable');
    var values = new Array();

    // LOOP THROUGH EACH ROW OF THE TABLE.
    for (row = 1; row < myTab.rows.length - 1; row++) {
        for (c = 0; c < myTab.rows[row].cells.length; c++) {   // EACH CELL IN A ROW.

            var element = myTab.rows.item(row).cells[c];
            if (element.childNodes[0].getAttribute('type') == 'text') {
                values.push("'" + element.childNodes[0].value + "'");
            }
        }
    }
    
    // SHOW THE RESULT IN THE CONSOLE WINDOW.
    console.log(values);
}

function deleteTable(){
    let element = document.getElementById('empTable');
    if(element != null){
        element.parentNode.removeChild(element);
    }
}

/*
Function to clear the suggestion box
Removes the visible suggestion box div
and creates a new invisible one
*/
function clearSuggestionsPanel(){
    let element = document.getElementById('search-suggestions');
    let parent = document.getElementById('slide-map-container');
    if(element != null){
        parent.removeChild(element);
    }
    let newElement = document.createElement('div');
    newElement.setAttribute('id', 'search-suggestions');
    parent.appendChild(newElement);
}

/*
For the provided data,
create a div
Insert the div to the search-suggestions div
Create a click event listener to geocode the data
*/
function addSuggestion(data){
    let field = document.getElementById('search-suggestions');
    let newSuggestion = document.createElement('div');
    // let newSuggestionContent = document.createTextNode(data);
    newSuggestion.innerHTML = data;
    field.appendChild(newSuggestion);
    newSuggestion.addEventListener('click', function(){
        console.log(data);
        let geocodingParameters = {
            searchText: data,
            jsonattributes: 1
          };
        geocode(geocodingParameters);
        clearSuggestionsPanel();
        closeSearchBox();
    });
}