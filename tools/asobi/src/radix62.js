/*global require: false, module: false */
// Convert a Number between base 10 and base 62.
// Refer to: https://github.com/substack/node-bigint
module.exports = (function () {
    "use strict";

    var bigint, encode, decode;

    // yum install gmp-devel
    // npm install bigint
    bigint = require("bigint");

    encode = function (num) {
        return bigint(num).toString(62);
    };

    decode = function (num) {
        return bigint(num, 62).toString();
    };

    return {
        encode: encode,
        decode: decode
    };
}());
