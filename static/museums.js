function toggleAccordion(clickedButton) {
    var panel = clickedButton.nextSibling;
    if (panel.style.maxHeight){
      panel.style.maxHeight = null;
    } else {
      panel.style.maxHeight = panel.scrollHeight + "px";
    }
}


var current_renamed_folder;

$(document).ready(function() {
    $('#delete-confirmed').click(function() {
        location.href = 'folders';
    });

    $('#create-folder-button').click(function() {
        //Reset the error message to empty string
        $( '.error-message' ).text('');
    });

    $('#save-name-button').click(function() {
        //remove trailing space and tab from the beginning and end of the name string
        var name_input = $('#input-new-foldername').val().trim();
        $('#input-new-foldername').val(name_input);

        //Check if input is empty or contains just white spaces only
        if ( name_input.length === 0) {
            $('#save-name-button').prop('type', 'button');
            $( '.error-message' ).text("* The name either is empty or contains only white spaces. Please input the eligible name for the folder. Example: Folder number 12");
            return;
        //Check if the name is unchanged. It just closes the modal.
        } else if (name_input === current_renamed_folder) {
            $('#save-name-button').prop('type', 'button');
            $('#rename-modal').modal('hide');
            return;
        } else {
            $('#save-name-button').prop('type', 'submit');
        }
    });

    $('#add-folder-button').click(function() {
        //Reset current renamed folder to pass the first if statement and take all folders into account.
        current_renamed_folder = '';

        //remove trailing space and tab from the beginning and end of the name string
        var name_input = $('#input-new-folder').val().trim();
        $('#input-new-folder').val(name_input);

        if ( name_input.length === 0) {
            $('#add-folder-button').prop('type', 'button');
            $( '.error-message' ).text("* The name either is empty or contains only white spaces. Please input the eligible name for the folder. Example: Folder number 12");
            return;
        } else {
            $('#add-folder-button').prop('type', 'submit');
        }
    });

    // Tooltip for the icon buttons
    $('[data-tooltip="tooltip"]').tooltip({trigger: "hover"});
});

function activate_rename_field(folder_name) {
    $('#rename-modal').on('show.bs.modal', function(e) {
        $(this).find("input").val(folder_name);
        $(this).find("#save-name-button").val(folder_name);
        current_renamed_folder = folder_name;
        //Reset the error message to empty string
        $( '.error-message' ).text('');
    });
}

function get_delete_name(folder_name) {
    $('#delete-modal').on('show.bs.modal', function(e) {
        $(this).find("input").val(folder_name);
        $(this).find("#delete-confirmed").val(folder_name);
    });
}