$(document).ready(function () {
    setTagCloud();
});

function setTagCloud() {
    $.ajax({
        type: "GET",
        url: '/blog/api/tags',
        dataType: "json",
        success: function(data, stat, xhr) {
            $('.tag-cloud li').remove();
            $('.tag-cloud ul').css('font-size', '70%');
            totalOccurrence = 0;
            for (var idx in data.tags) {
                totalOccurrence += data.tags[idx].occurrence;
            }
            for (var idx in data.tags) {
                tagJ = data.tags[idx];
                listItem = $('<li><a href=' + tagJ.url + '>' + tagJ.name + '</a></li>')
                .css({'display': 'inline-block'
                     , 'margin': '1px'
                     , 'font-size': getFontSizeEm(tagJ) + 'em'});
                 $('.tag-cloud ul').append(listItem);
            }
        },
        error: function(e){
            console.error(e);
        }
    });
}

function getFontSizeEm(tag) {
    baseVal = (tag.occurrence / totalOccurrence) * 10;
    if (baseVal > 2.5) {
        return 2.5;
    } else {
        return Math.max(1, baseVal);
    }
}
