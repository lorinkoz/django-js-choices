{{ js_global_object_name }}.{{ js_var_name }} = (function () {
    var rawChoices = [{% for choice in raw_choices_list %}{% if not forloop.first %},{% endif %}{{ choice|safe }}{% endfor %}];
    var namedChoices = {{ named_choices|safe }};
    return {
        pairs: function(name) {
            var choices = rawChoices[namedChoices[name]];
            return choices && choices.map(pair => ({value: pair[0], label: pair[1]}));
        },
        display: function(name, choice) {
            var choices = rawChoices[namedChoices[name]],
                finder = choice !== Object(choice) ? (pair => pair[0] == choice) : (pair => pair[0] == choice[name]),
                pair = choices && choices.find(finder);
            return pair && pair[1];
        }
    };
})();
