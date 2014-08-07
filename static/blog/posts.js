$(document).ready(function () {
    $("#new-post").dialog({
        autoOpen: false
    });
    console.log("loaded");
    // $('#add-post').bind('click', addPost);
    $('#add-post').bind('click', function () {
        $('#new-post').dialog('open');
    });
});

function initdlg() {
    $("#add-post").dialog({
        modal: true,
        draggable: true,
        resizable: false,
        position: ['center', 'top'],
        show: 'blind',
        hide: 'blind',
        width: 400,
        dialogClass: 'ui-dialog-osx',
        buttons: {
            "I've read and understand this": function() {
                $(this).dialog("close");
            }
        }
    });
}

function addPost() {
    $(document)
        .find('#theme')
        .append(
                $('<form></form>')
                .css('margin', '10px 10px')
                .append(
                    $('<input></input>')
                    .css('display', 'block')
                    )
                .append(
                    $('<textarea></textarea>')
                    .css('width', '100%')
                    .css('display', 'block')
                    )
               )
        .end();
}
