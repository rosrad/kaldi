/*global require: false, module: false, Buffer: false */
module.exports = (function () {
    "use strict";

    var crypto, Signer, Express;

    crypto = require('crypto');

    Signer = function (secret) {
        this.secret = secret;
    };

    Signer.prototype = {
        // Sign a piece of data.
        // Return a hex string.
        sign: function (data) {
            return crypto.createHmac('sha256', this.secret)
                         .update(data).digest('hex');
        },

        // Verify the signature of data.
        // Return true or false.
        verify: function (data, signature) {
            return this.sign(data) === signature;
        }
    };

    Express = {};

    // Authorization middleware for the express framework.
    // getSecret is a callback for querying secret of a request.
    // getSecret(req, callback(secret));
    Express.Authorizer = function (getSecret) {
        return function (req, res, next) {
            var policy, signature, decodedPolicy;

            // fetch policy and signature
            if (req.query && req.query.policy) {
                policy = req.query.policy;
                signature = req.query.signature || '';
            } else if (req.body && req.body.policy) {
                policy = req.body.policy;
                signature = req.body.signature || '';
            } else {
                res.send(403, {result: 'Permission denied'});
                return;
            }

            // decode policy
            try {
                decodedPolicy = new Buffer(policy, 'base64').toString('ascii');
                req.policy = JSON.parse(decodedPolicy);
            } catch (e) {
                res.send(403, {result: 'Permission denied'});
                return;
            }

            // ask for a secret for this request
            getSecret(req, function (err, secret) {
                var signer;

                if (err) {
                    res.send(500, {result: err});
                    return;
                }

                if (!secret) {
                    res.send(403, {result: 'Permission denied'});
                    return;
                }

                signer = new Signer(secret);

                if (!signer.verify(policy, signature)) {
                    res.send(403, {result: 'Permission denied'});
                    return;
                }

                req.policy_secret = secret;

                next();
            });
        };
    };

    return {
        Signer: Signer,
        Express: Express
    };
}());
