var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        command: '> ',
        records: [],
        to_render: []
    },
    mounted: function () {
        let records = JSON.parse(document.currentScript.getAttribute('records'));
        for (let i = 0; i < records.length; ++i) {
            this.add_record(i, records[i]);
        }
    },
    updated: function() {
        for (let i = 0; i < this.to_render.length; ++i) {
            vegaEmbed('#'+this.to_render[i][0], this.to_render[i][1]);
        }
        this.to_render = [];
    },
    methods: {
        add_record: function (i, record) {
            if (record[0] === 'G') {
                record.push('vis' + i);
            } else if (record[0] === 'A') {
                record[1] = '> ' + record[1];
            }
            this.records.push(record);
            if (record[0] === 'G') {
                this.to_render.push([record[2], record[1]]);
            }
        }
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
