{{ js_global_object_name }}.{{ js_var_name }} = (function () {
    var rawChoices = [{% for choice in raw_choices_list %}{% if not forloop.first %},{% endif %}{{ choice|safe }}{% endfor %}];
    var namedChoices = {{ named_choices|safe }};
    return {
        pairs: function(name) {
            var choices = rawChoices[namedChoices[name]];
            var mapper = function (pair) {
                return {
                    value: pair[0],
                    label: pair[1]
                };
            }
            return choices && choices.map(mapper);
        },
        display: function(name, choice) {
            var choices = rawChoices[namedChoices[name]];
            var finder = choice !== Object(choice)
                ? function (pair) { return pair[0] == choice; }
                : function (pair) { return pair[0] == choice[name]; };
            var pair = choices && choices.filter(finder)[0];
            return pair && pair[1];
        }
    };
})();
