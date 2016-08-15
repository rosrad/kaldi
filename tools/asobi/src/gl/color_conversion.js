function Clamp(min, max, val) {
    if (val < min) {
        return min;
    } else if (val > max) {
        return max;
    } else {
        return val;
    }
}

// Does a conversion from RGB to HSV (Hue, Saturation, Value) colorspace
// r = [0, 1], g = [0, 1], b = [0, 1]
// h = [0, 1], s = [0, 1], v = [0, 1]
function RGBToHSV(r, g, b) {
    var max, min, chroma, h, s, v;

    max = Math.max(r, g, b);
    min = Math.min(r, g, b);
    chroma = max - min;

    v = max;

    if (chroma > 1e-6) {
        s = chroma / max;

        if (r === max) {
            h = (g - b) / chroma;
            if (h < 0) {
                h += 6;
            }
        } else if (g === max) {
            h = (b - r) / chroma + 2;
        } else {
            h = (r - g) / chroma + 4;
        }

        h /= 6;
    } else {
        s = 0;
        h = 0;
    }

    return [h, s, v];
}

// Convert a color value from HSV to RGB colorspace
// r = [0, 1], g = [0, 1], b = [0, 1]
// h = [0, 1], s = [0, 1], v = [0, 1]
function HSVToRGB(h, s, v) {
    var chroma, min, bias, r, g, b;

    chroma = v * s;
    min = v - chroma;

    h *= 6;  // [0.0, 6.0]
    if (h === 6) {
        h = 0;
    }

    bias = chroma * (1 - Math.abs(h % 2 - 1));

    r = g = b = min;
    switch (Math.floor(h)) {
        case 0:  // red to green
            r += chroma;
            g += bias;
            break;
        case 1:  // green to red
            g += chroma;
            r += bias;
            break;
        case 2:  // gree to blue
            g += chroma;
            b += bias;
            break;
        case 3:  // blue to green
            b += chroma;
            g += bias;
            break;
        case 4:  // blue to red
            b += chroma;
            r += bias;
            break;
        case 5:  // red to blue
            r += chroma;
            b += bias;
            break;
    }

    return [r, g, b];
}

// Convert an RGB color value to HSL (Hue, Saturation, Lightness)
// color value.
// r = [0, 1], g = [0, 1], b = [0, 1]
// h = [0, 1], s = [0, 1], l = [0, 1]
function RGBToHSL(r, g, b) {
    var max, min, chroma, h, s, l;

    max = Math.max(r, g, b);
    min = Math.min(r, g, b);
    chroma = max - min;

    l = (max + min) / 2;

    if (chroma > 1e-6) {
        s = chroma / (1 - Math.abs(2 * l - 1));

        if (r === max) {
            h = (g - b) / chroma;
            if (h < 0) {
                h += 6;
            }
        } else if (g === max) {
            h = (b - r) / chroma + 2;
        } else {
            h = (r - g) / chroma + 4;
        }

        h /= 6;
    } else {
        s = 0;
        h = 0;
    }

    return [h, s, l];
}

// Convert a HSL color value to an RGB color value.
// r = [0, 1], g = [0, 1], b = [0, 1]
// h = [0, 1], s = [0, 1], l = [0, 1]
function HSLToRGB(h, s, l) {
    var chroma, min, bias, r, g, b;

    chroma = (1 - Math.abs(2 * l - 1)) * s;
    min = l - chroma / 2;

    h *= 6;  // [0.0, 6.0]
    if (h === 6) {
        h = 0;
    }

    bias = chroma * (1 - Math.abs(h % 2 - 1));

    r = g = b = min;
    switch (Math.floor(h)) {
        case 0:  // red to green
            r += chroma;
            g += bias;
            break;
        case 1:  // green to red
            g += chroma;
            r += bias;
            break;
        case 2:  // gree to blue
            g += chroma;
            b += bias;
            break;
        case 3:  // blue to green
            b += chroma;
            g += bias;
            break;
        case 4:  // blue to red
            b += chroma;
            r += bias;
            break;
        case 5:  // red to blue
            r += chroma;
            b += bias;
            break;
    }

    return [r, g, b];
}

// Convert an HSV triplet to HSL colorspace
// h = [0, 1], s = [0, 1], v = [0, 1]
// h = [0, 1], s = [0, 1], l = [0, 1]
function HSVToHSL(h, s, v) {
    var hh, ss, ll;

    hh = h;

    ll = (2 - s) * v;

    ss = s * v;
    ss /= (ll <= 1) ? ll : (2 - ll);

    ll /= 2;

    return [hh, ss, ll];
}

// Convert an HSL triplet to HSV colorspace
// h = [0, 1], s = [0, 1], l = [0, 1]
// h = [0, 1], s = [0, 1], v = [0, 1]
function HSLToHSV(hh, ss, ll) {
    var h, s, v;

    h = hh;

    ll *= 2;
    ss *= (ll <= 1) ? ll : (2 - ll);

    s = 2 * ss / (ll + ss);

    v = (ll + ss) / 2;

    return [h, s, v];
}

// Convert an RGB triplet to HSI Intensity
// r = [0, 1], g = [0, 1], b = [0, 1]
// i = [0, 1]
function RGBToIntensity(r, g, b) {
    return (r + g + b) / 3;
}

// Convert an RGB triplet to HSV Value
// r = [0, 1], g = [0, 1], b = [0, 1]
// v = [0, 1]
function RGBToValue(r, g, b) {
    return Math.max(r, g, b);
}

// Convert an RGB triplet to HSL Lightness
// r = [0, 1], g = [0, 1], b = [0, 1]
// l = [0, 1]
function RGBToLightness(r, g, b) {
    return (Math.max(r, g, b) + Math.min(r, g, b)) / 2;
}

// Convert an RGB triplet to Rec.601 luminance
// r = [0, 1], g = [0, 1], b = [0, 1]
// y = [0, 1]
function RGBToY601(r, g, b) {
    return 0.299 * r + 0.587 * g + 0.114 * b;
}

// Convert an RGB triplet to Rec.709 luminance
// r = [0, 1], g = [0, 1], b = [0, 1]
// y = [0, 1]
function RGBToY709(r, g, b) {
    return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

// Convert an RGB triplet to a hex string (e.g. fffe00)
// r, g, b = [0, 255]
function RGBToHex(r, g, b) {
    var rs, gs, bs;

    rs = r.toString(16);
    if (r < 16) {
        rs = '0' + rs;
    }

    gs = g.toString(16);
    if (g < 16) {
        gs = '0' + gs;
    }

    bs = b.toString(16);
    if (b < 16) {
        bs = '0' + bs;
    }

    return rs + gs + bs;
}

// Convert a hex string (e.g. fffe00) to an RGB triplet
// r, g, b = [0, 255]
function HexToRGB(hex) {
    var rs, gs, bs, r, g, b;

    rs = hex.substring(0, 2);
    gs = hex.substring(2, 4);
    bs = hex.substring(4, 6);

    r = parseInt(rs, 16);
    g = parseInt(gs, 16);
    b = parseInt(bs, 16);

    return [r, g, b];
}

// Refer to:
// http://en.wikipedia.org/wiki/HSL_and_HSV
// http://www.rapidtables.com/convert/color/rgb-to-hsv.htm
// http://ariya.ofilabs.com/2008/07/converting-between-hsl-and-hsv.html
// https://gist.github.com/xpansive/1337890
