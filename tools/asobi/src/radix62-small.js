/*global require: false, module: false */
// Convert a Number between base 10 and base 62.
// Only works for small numbers due to precision limit.
module.exports = (function () {
    "use strict";

    var RADIX, ALPHABET, PRIMITIVES, encode, decode, i;

    RADIX = 62;

    ALPHABET = '0123456789' +
               'ABCDEFGHIJKLMNOPQRSTUVWXYZ' +
               'abcdefghijklmnopqrstuvwxyz';

    PRIMITIVES = {};
    for (i = ALPHABET.length - 1; i >= 0; i -= 1) {
        PRIMITIVES[ALPHABET[i]] = i;
    }

    encode = function (num) {
        var prefix, chars;

        if (num === 0) {
            return '0';
        }


        if (num < 0) {
            prefix = '-';
            num *= -1;
        } else {
            prefix = '';
        }

        chars = [];

        while (num > 0) {
            chars.unshift(ALPHABET[num % 62]);
            num = Math.floor(num / 62);
        }

        chars.unshift(prefix);
        return chars.join('');
    };

    decode = function (str) {
        var positive, result, i;

        positive = true;
        if (str[0] === '+') {
            str = str.substring(1);
        } else if (str[0] === '-') {
            positive = false;
            str = str.substring(1);
        }

        result = 0;
        for (i = 0; i < str.length; i += 1) {
            result *= RADIX;
            result += PRIMITIVES[str[i]];
        }

        return positive ? result : -1 * result;
    };

    return {
        RADIX: RADIX,
        ALPHABET: ALPHABET,
        PRIMITIVES: PRIMITIVES,
        encode: encode,
        decode: decode
    };
}());
