(function () {
    var ddOriginalReferrer = document.referrer;
    var ddFpHashes = ['C992DCAFEE25FA95C6492C61EB3328'];
    var popUpAllowedClientKeys = [
        'F45F521D9622089B5E33C18031FB8E',
        '10D43DA6B79A5089E1A7846864D6BD',
        '34C213C44735CBC8D9C08B65110F96',
        'D428D51E28968797BC27FB9153435D',
        '87B024B36133DBAA93E054371373E7',
    ];
    try {
        if (!ddOriginalReferrer && dd.rr) {
            ddOriginalReferrer = decodeURIComponent(dd.rr);
        }
    } catch (_) {
        /* Silent failure if decodeURIComponent throws */
    }

    /**
     * Saves actual referrer to session storage
     * @return {void}
     */
    function saveReferrer() {
        try {
            window.sessionStorage.setItem('ddOriginalReferrer', ddOriginalReferrer);
        } catch (error) {
            // Silently fails
        }
    }
    saveReferrer();

    var noScriptMessageElement = document.getElementById('cmsg');
    var noScriptMessageText = noScriptMessageElement ? noScriptMessageElement.innerText : '';
    var getRefererQueryParamString = function () {
        try {
            var prefix = '&referer=';
            if (window.location !== window.parent.location) {
                // Nested Iframe
                return prefix + encodeURIComponent(window.location.href);
            }
            return prefix + encodeURIComponent(window.parent.location.href);
        } catch (e) {
            return '';
        }
    };

    var isSafari = window.navigator
        ? /^((?!chrome|android).)*safari/i.test(navigator.userAgent)
        : false;
    var stretchHeightRule = isSafari ? 'height: -webkit-fill-available;' : '';

    var getDDCookie = function (value) {
        var r = new RegExp('datadome=([^;]+)');
        var v = r.exec(value);
        if (v != null) {
            try {
                return decodeURIComponent(v[1]);
            } catch (e) {
                return v[1];
            }
        }
        return null;
    };

    function getHostname(url) {
        var scheme = 'https://';

        if (typeof url !== 'string' || url.indexOf(scheme) !== 0) {
            return '';
        }

        return url.replace(scheme, '').split('/')[0];
    }

    // Check if a URL is coming from a DataDome origin.
    function isDatadomeOrigin(url) {
        var ddHosts = ['.datado.me', '.captcha-delivery.com'];
        var hostname = getHostname(url);

        if (!hostname) {
            return false;
        }

        for (var i = 0; i < ddHosts.length; i++) {
            var ddHost = ddHosts[i];
            if (hostname.indexOf(ddHost, hostname.length - ddHost.length) !== -1) {
                return true;
            }
        }

        return false;
    }

    function shouldCheckFpOrigin(hash) {
        return ddFpHashes.indexOf(hash) > -1;
    }

    function isAuthorizedThirdPartyDomain(currentHostname, hostname) {
        if (!currentHostname || !hostname) {
            return false;
        }
        var hostParts = hostname.split('.').reverse();
        var currParts = currentHostname.split('.').reverse();
        // bail out if we don't have at least “label” + “tld”
        if (hostParts.length < 2 || currParts.length < 2) {
            return false;
        }
        var isPaypalCom = hostParts[0] === 'com' && hostParts[1] === 'paypal';
        var isVenmoCom = currParts[0] === 'com' && currParts[1] === 'venmo';

        return isPaypalCom && isVenmoCom;
    }

    function isFpOrigin(url) {
        var hostname = getHostname(url);
        var currentHostname = getHostname(window.location.href);

        if (!hostname || !currentHostname) {
            return false;
        }

        if (isAuthorizedThirdPartyDomain(currentHostname, hostname)) {
            return true;
        }

        var hostnameParts = hostname.split('.').reverse();
        var currentHostnameParts = currentHostname.split('.').reverse();
        var matchCount = 0;

        for (var i = 0; i < currentHostnameParts.length; ++i) {
            if (hostnameParts[i] === currentHostnameParts[i]) {
                ++matchCount;
            } else {
                break;
            }
        }

        return matchCount >= 2 && hostnameParts[matchCount] === 'ddc';
    }

    function isTrustedOrigin(url) {
        return isDatadomeOrigin(url) || (shouldCheckFpOrigin(dd.hsh) && isFpOrigin(url));
    }

    function getQueryParamFromURL(sourceURL, paramName) {
        if (!window.URL) {
            return '';
        }
        try {
            var extendedURL = new URL(sourceURL);
            return extendedURL.searchParams.get(paramName) || '';
        } catch (error) {
            return '';
        }
    }

    function replaceCookieDomain(cookie, newDomain) {
        try {
            cookie = cookie.replace(/Domain=.*?;/, 'Domain=' + newDomain + ';');
        } catch (_) {
            // Fail silently.
        }

        return cookie;
    }

    function setCookieWithFallback(cookie) {
        var expectedValue = getDDCookie(cookie);

        if (expectedValue === null) {
            return false;
        }

        document.cookie = cookie;

        if (getDDCookie(document.cookie) === expectedValue) {
            return true;
        }

        var tryCandidate = function (candidate) {
            var candidateCookie = replaceCookieDomain(cookie, candidate);
            document.cookie = candidateCookie;

            var actualValue = getDDCookie(document.cookie);
            return { candidateCookie: candidateCookie, actualValue: actualValue };
        };

        var generateCandidates = function (hostname) {
            var parts = hostname.split('.');
            var candidates = [];
            var min = 2,
                max = parts.length < 8 ? parts.length : 8;
            for (var i = min; i <= max; ++i) {
                if (parts.length >= i) {
                    candidates.push('.' + parts.slice(-1 * i).join('.'));
                }
            }
            if (candidates.length === 0) {
                candidates.push(hostname);
            }
            return candidates;
        };

        var hostname = window.location.hostname;
        var candidates = generateCandidates(hostname);

        // Try each candidate until the cookie is saved correctly.
        for (var i = 0; i < candidates.length; ++i) {
            var candidate = candidates[i];
            var res = tryCandidate(candidate);
            if (res.actualValue === expectedValue) {
                return true;
            }
        }

        return false;
    }

    function generateIframe(dd, noScriptMessageText, volatile, stretchHeightRule) {
        var targetOrigin = 'https://' + dd.host.replace(new RegExp('&#x2d;', 'g'), '-');
        if (!isTrustedOrigin(targetOrigin)) {
            console.error(
                '%c Invalid CAPTCHA origin: ' + targetOrigin,
                'background: red; color: #fff'
            );
            return;
        }
        var isIframeLoaded = false;
        var maxTimeoutMs = 5000;

        function iframeOnload() {
            isIframeLoaded = true;
            var noIframeElem = document.getElementById('noiframe');
            if (noIframeElem) {
                noIframeElem.parentNode.removeChild(noIframeElem);
            }
        }

        if (
            typeof navigator.userAgent === 'string' &&
            navigator.userAgent.indexOf('Firefox') > -1
        ) {
            var initialTime = new Date().getTime();
            setTimeout(function () {
                if (!isIframeLoaded && new Date().getTime() - initialTime > maxTimeoutMs) {
                    document.body.innerHTML =
                        '<div id="noiframe">' +
                        noScriptMessageText +
                        '</div>' +
                        document.body.innerHTML;
                }
            }, maxTimeoutMs);
        }

        /** @type {('json' | 'html' | null)} - Holds the format of the additional challenge */
        var ddMessageFormat = getQueryParamFromURL(window.location.href, 'ddMessageFormat');

        var iframeSrc =
            'https://' +
            dd.host +
            '/captcha/?initialCid=' +
            encodeURIComponent(dd.cid) +
            '&hash=' +
            encodeURIComponent(dd.hsh) +
            '&cid=' +
            encodeURIComponent(
                volatile ? window.ddcid : dd.cookie || getDDCookie(document.cookie)
            ) +
            (ddMessageFormat ? '&ddMessageFormat=' + encodeURIComponent(ddMessageFormat) : '') +
            '&t=' +
            encodeURIComponent(dd.t) +
            getRefererQueryParamString() +
            '&s=' +
            dd.s +
            '&e=' +
            dd.e +
            '&dm=cd' +
            (dd.cp && dd.cp.name && dd.cp.value
                ? '&' + encodeURIComponent(dd.cp.name) + '=' + encodeURIComponent(dd.cp.value)
                : '');

        var iframeSandbox =
            'allow-scripts allow-same-origin allow-forms' +
            (popUpAllowedClientKeys.indexOf(dd.hsh) > -1 ? ' allow-popups' : '');
        var iframePermissions = 'accelerometer; gyroscope; magnetometer';
        var iframeTitle = 'DataDome CAPTCHA';
        var iframeHTML =
            '<iframe src="' +
            iframeSrc +
            '" sandbox="' +
            iframeSandbox +
            '" allow="' +
            iframePermissions +
            '" title="' +
            iframeTitle +
            '" width="100%" height="100%" style="height:100vh;' +
            stretchHeightRule +
            '" FRAMEBORDER="0" border="0" scrolling="yes"' +
            '></iframe>';

        return { iframeHTML: iframeHTML, iframeOnload: iframeOnload };
    }
    var volatile = document.cookie === '' && window.ddcid != null;

    var iframeResult = generateIframe(dd, noScriptMessageText, volatile, stretchHeightRule);
    var iframeWrapper = document.createElement('div');
    iframeWrapper.innerHTML = iframeResult.iframeHTML;
    var iframeElem = iframeWrapper.firstChild;

    if (iframeElem) {
        iframeElem.addEventListener('load', iframeResult.iframeOnload);
    }

    document.body.appendChild(iframeElem);

    if (noScriptMessageElement) {
        noScriptMessageElement.parentNode.removeChild(noScriptMessageElement);
    }

    var canGoBack =
        window.history && typeof window.history.back === 'function' && window.history.length > 1;
    // `ddShouldGoBack` is an option that can be set by a code snippet in a customer's page customization.
    var shouldGoBack = (dd.r && dd.r === 'b' && canGoBack) || (window.ddShouldGoBack && canGoBack);
    var shouldReplay = typeof dd.p === 'string' && dd.p !== '';

    var viewPortTag = document.createElement('meta');
    viewPortTag.name = 'viewport';
    viewPortTag.content = 'width=device-width, initial-scale=1.0';

    var headTag = document.querySelector('head');
    if (headTag != null) {
        headTag.appendChild(viewPortTag);
    }

    var onMessageCallback = function (event) {
        function addSearchParam(url, name, value) {
            if (typeof window.URL === 'function') {
                var extendedURL = new URL(url);
                extendedURL.searchParams.set(name, value);

                return extendedURL.href;
            }

            return url;
        }

        if (event.isTrusted && isTrustedOrigin(event.origin)) {
            if (typeof event.data !== 'string') {
                return false;
            }

            try {
                var data = JSON.parse(event.data);

                if (data.eventType == 'load') {
                    return false;
                }

                if (data.cookie) {
                    setCookieWithFallback(data.cookie);
                }

                if (data.url) {
                    setTimeout(function () {
                        if (shouldReplay) {
                            var replayForm = document.createElement('form');
                            replayForm.method = 'POST';
                            replayForm.action = window.location.href;
                            var payloadInput = document.createElement('input');
                            payloadInput.type = 'text';
                            payloadInput.name = 'payload';
                            payloadInput.value = dd.p;
                            replayForm.appendChild(payloadInput);
                            document.body.appendChild(replayForm);
                            replayForm.submit();
                        } else if (shouldGoBack) {
                            if (volatile && document.referrer.length > 0) {
                                window.location = addSearchParam(
                                    document.referrer,
                                    'ddcid',
                                    getDDCookie(data.cookie)
                                );
                            } else {
                                history.back();
                            }
                        } else {
                            if (volatile && typeof window.URL === 'function') {
                                window.location = addSearchParam(
                                    window.location.href,
                                    'ddcid',
                                    getDDCookie(data.cookie)
                                );
                            } else if (dd.rr != null) {
                                // Due to referrer loss on post challenge resolution,
                                // instead of reloading the page we load the current URL
                                // with the referrer appended as a query parameter.
                                var currentBaseUrl =
                                    window.location.origin + window.location.pathname;
                                var referrerBaseUrl = document.referrer.split('?')[0].split('#')[0];

                                if (referrerBaseUrl !== currentBaseUrl) {
                                    var newURL = new URL(window.location.href);
                                    if (window.location.search === '' && dd.qp != null) {
                                        var queryParams = new URLSearchParams(
                                            decodeURIComponent(dd.qp)
                                        );
                                        queryParams.set('dd_referrer', ddOriginalReferrer);
                                        newURL.search = queryParams.toString();
                                    } else {
                                        newURL = addSearchParam(
                                            newURL,
                                            'dd_referrer',
                                            ddOriginalReferrer
                                        );
                                    }
                                    window.location.href = newURL.toString();
                                } else {
                                    window.location.reload();
                                }
                            } else {
                                window.location.reload();
                            }
                        }
                    }, 500);
                }
            } catch (_) {
                /* Silent failure if JSON.parse is used on invalid data */
            }
        }
    };

    if (window.addEventListener) {
        window.addEventListener('message', onMessageCallback, false);
    } else if (window.attachEvent) {
        window.attachEvent('onmessage', onMessageCallback);
    }
})();
