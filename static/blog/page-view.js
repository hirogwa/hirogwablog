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
            $('.tag-cloud ul').css('font-size', '100%');
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
    if (totalOccurrence < 7) {
        return 1;
    }
    maxSize = 4;
    minSize = 0.7;
    baseVal = (tag.occurrence / totalOccurrence);
    return baseVal * (maxSize - minSize) + minSize;
}
