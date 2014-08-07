$(document).ready(function () {
    addThemeDialog();
    console.log("loaded");
    $('#add-theme').bind('click', function () {
        $('#add-theme-dlg').dialog('open');
        console.log('fire!!');
    });
});

function addThemeDialog() {
    dlg = $('<form id="add-theme-dlg"></form>')
        .append($('<table></table>')
                .append($('<tr></tr>'))
                .append($('<input></input>')));
    $(document)
        .find('#dialogs')
        .append(dlg)
        .end();
    $('#add-theme-dlg').dialog({
        autoOpen: false,
    })
}
