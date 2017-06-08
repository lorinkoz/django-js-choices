{{ js_global_object_name }}.{{ js_var_name }} = (function () {
    return function(name) {
        var rawChoices = [{% for choice in raw_choices_list %}{% if not forloop.first %},{% endif %}{{ choice|safe }}{% endfor %}];
        var namedChoices = {{ named_choices|safe }};
        return rawChoices[namedChoices[name]];
    };
})();
