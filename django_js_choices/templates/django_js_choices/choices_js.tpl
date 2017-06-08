{{ js_global_object_name }}.{{ js_var_name }} = (function () {
    var rawChoices = [{% for choice in raw_choices_list %}{% if not forloop.first %},{% endif %}{{ choice|safe }}{% endfor %}];
    var namedChoices = {{ named_choices|safe }};
    return {
        pairs: function(name) {
            return rawChoices[namedChoices[name]].map(pair => ({value: pair[0], label: pair[1]}));
        },
        display: function(name, choice) {
            var pair = rawChoices[namedChoices[name]].find(pair => pair[0] == choice);
            return pair && pair[1];
        }
    };
})();
