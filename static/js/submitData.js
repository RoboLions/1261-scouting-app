// A function to collect information from the user interface and send it off
// to the Python backend to be saved in a data file
function submitData() {

    var data =
    {
        'team_number': parseInt(document.getElementById('team_number').value),
        'balls_thrown': parseInt(document.getElementById('balls_thrown').value),
        'team_color': document.getElementById('team_color').value,
        'can_climb': document.getElementById('can_climb').checked,
        'notes': document.getElementById('notes').value
    };

    $(document).ready( function() {
        $.post( "/postmethod", {
            javascript_data: data
        });
        console.log("Hello World")
    } )
}
