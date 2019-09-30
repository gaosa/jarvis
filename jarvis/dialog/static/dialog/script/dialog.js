var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        command: '> ',
        records: [],
        to_render: [],
        dialog_id: -1,
        current_url: "",
        next_vis_idx: 0,
    },
    mounted: function () {
        let data = JSON.parse(document.currentScript.getAttribute('data'));
        let records = data.records;
        this.dialog_id = data.dialog_id;
        this.current_url = data.current_url;
        for (let i = 0; i < records.length; ++i) {
            this.add_record(records[i]);
        }
    },
    updated: function() {
        for (let i = 0; i < this.to_render.length; ++i) {
            vegaEmbed('#'+this.to_render[i][0], this.to_render[i][1]);
        }
        this.to_render = [];
    },
    methods: {
        add_record: function (record) {
            if (record[0] === 'G') {
                record.push('vis' + this.next_vis_idx);
                ++this.next_vis_idx;
            } else if (record[0] === 'A') {
                record[1] = '> ' + record[1];
            }
            this.records.push(record);
            if (record[0] === 'G') {
                this.to_render.push([record[2], record[1]]);
            }
        },
        sendCommand: function() {
            let that = this;
            axios.post(this.current_url, {
                'command': this.command.trimRight().substring(2)
            }).then(function (response) {
                for (let i = 0; i < response.data.new_records.length; ++i) {
                    that.add_record(response.data.new_records[i]);
                }
            });
            this.command = '';
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
