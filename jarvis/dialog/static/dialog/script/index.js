var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        url: "",
        msg: ""
    },
    mounted: function () {
        let data = JSON.parse(document.currentScript.getAttribute('data'));
        this.url = data.url;
    },
    methods: {
        upload: function (name, files) {
            const formData = new FormData();
            formData.append(name, files[0], files[0].name);
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
