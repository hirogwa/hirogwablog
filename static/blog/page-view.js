$(document).ready(function () {
    setTagCloud();
});

function setTagCloud() {
    $.ajax({
        type: "GET",
        url: '/blog/api/entry/list',
        // data: parameters,
        // contentType: "application/json; charset=utf-8",
        // dataType: "json",
        success: function(data, stat, xhr) {
            console.log(data);
            console.log(stat);
            console.log(xhr);
        },
        error: function(e){
                   console.log(e);
               }
    });
    /*
       alert(count);
       console.log(count);
       tag_element = $(document).find('.tag-cloud li');
       tag_element.css({'color': 'aqua'});
       */
}
