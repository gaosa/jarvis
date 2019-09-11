var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        command: '> ',
        records: [
            ['Q', 'How you doing?'],
            ['A', 'I am quite well'],
            ['E']
        ]
    },
    watch: {
        'command': function(val, oldVal) {
            val = val.trimLeft();
            if (val.length == 0) {
                this.command = '> ';
            } else if (val.length == 1) {
                if (val[0] === '>') this.command = '> ';
                else this.command = '> ' + val;
            } else {
                if (val[0] !== '>') this.command = '> ' + val;
                else if (val[1] === ' ') this.command = val;
                else this.command = '> ' + val.substr(1);
            }
        }
    }
});

// function draw(id, jsonUrl) {
//     vegaEmbed(id, jsonUrl).then(function(result) {
//         // Access the Vega view instance (https://vega.github.io/vega/docs/api/view/) as result.view
//     }).catch(console.error);
// }

// var spec = "data.json";
// vegaEmbed('#vis', spec).then(function(result) {
//     // Access the Vega view instance (https://vega.github.io/vega/docs/api/view/) as result.view
// }).catch(console.error);