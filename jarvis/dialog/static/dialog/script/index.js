var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        url: "",
        msg: "",
        tests: ['test1-1', 'test1-2', 'test1-3', 'test2-1', 'test2-2', 'test2-3', 'test3-1', 'test3-2', 'test3-3'],
    },
    mounted: function () {
        let data = JSON.parse(document.currentScript.getAttribute('data'));
        this.url = data.url;
    },
    methods: {
        upload: function (name, files = null) {
            const formData = new FormData();
            if (files !== null) {
                formData.append(name, files[0], files[0].name);
            } else {
                formData.append(name, '');
            }
            axios.post(this.url, formData).then(response => {
                if ('url' in response.data) {
                    window.location.href = response.data.url;
                } else {
                    this.msg = response.data.msg;
                }
            });
        }
    }
});
