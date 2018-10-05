// A function to collect information from the user interface and send it off
// to the Python backend to be saved in a data file
function submitData() {

    let data =
    {
        'team_number': parseInt(document.getElementById('team_number').value),
        'auto': document.getElementById('auto').value,
        'switch_cubes': parseInt(document.getElementById('switch_cubes').value),
        'scale_cubes': parseInt(document.getElementById('scale_cubes').value),
        'vault_cubes': parseInt(document.getElementById('vault_cubes').value),
        'can_climb': document.getElementById('can_climb').value,
        'notes': document.getElementById('notes').value
    };

    $(document).ready( function() {
        $.post( "/postmethod", {
            javascript_data: data
        });
        console.log("Hello World")
    } )
}
