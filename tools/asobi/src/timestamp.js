(function () {
    "use strict";

    Date.prototype.getUnixTime = function () {
        return parseInt(this.getTime() / 1000, 10);
    };

    Date.prototype.getTimestamp = function () {
        var year, month, day, hour, min, sec;

        year = this.getFullYear();
        month = this.getMonth() + 1;
        day = this.getDate();

        hour = this.getHours();
        if (hour < 10) {
            hour = '0' + hour;
        }

        min = this.getMinutes();
        if (min < 10) {
            min = '0' + min;
        }

        sec = this.getSeconds();
        if (sec < 10) {
            sec = '0' + sec;
        }

        return year + '-' + month + '-' + day + ' ' + hour + ':' + min + ':' + sec;
    };

    Date.prototype.getUTCTimestamp = function () {
        var year, month, day, hour, min, sec;

        year = this.getUTCFullYear();
        month = this.getUTCMonth() + 1;
        day = this.getUTCDate();

        hour = this.getUTCHours();
        if (hour < 10) {
            hour = '0' + hour;
        }

        min = this.getUTCMinutes();
        if (min < 10) {
            min = '0' + min;
        }

        sec = this.getUTCSeconds();
        if (sec < 10) {
            sec = '0' + sec;
        }

        return year + '-' + month + '-' + day + ' ' + hour + ':' + min + ':' + sec;
    };
}());
