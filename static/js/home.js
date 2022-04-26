$(document).ready(function(){
    input_pattern = ''
    players_list.forEach(function (item, index) {
      input_pattern = input_pattern + '|' + item[0];
    });

    var player_field = document.getElementsByClassName("form_player")
    player_field[0].setAttribute("required", "required");
    player_field[0].setAttribute("pattern", input_pattern);

    player_field[0].oninvalid = function(event) {
        event.target.setCustomValidity('Player must be chosen among the list of players');
    }

    $('input[class="form_player"]').autoComplete({
        minChars: 2,
        delay: 100,
        source: function(term, suggest){
            term = term.toLowerCase();
            var choices = players_list;
            var suggestions = [];
            for (i=0;i<choices.length;i++)
                if (~(choices[i][0]+' '+choices[i][1]).toLowerCase().indexOf(term)) suggestions.push(choices[i]);
            suggest(suggestions);
        },
        renderItem: function (item, search){
            search = search.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&');
            var re = new RegExp("(" + search.split(' ').join('|') + ")", "gi");
            return '<div class="autocomplete-suggestion" data-langname="'+item[0]+'" data-lang="'+item[1]+'" data-val="'+search+'">'+item[0].replace(re, "<b>$1</b>")+'</div>';
        },
        onSelect: function(e, term, item){
            e.preventDefault();
            $('input[class="form_player"]').val(item.data('langname'));
        },
    });
});