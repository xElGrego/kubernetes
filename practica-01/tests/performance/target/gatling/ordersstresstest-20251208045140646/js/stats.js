var stats = {
    type: "GROUP",
name: "All Requests",
path: "",
pathFormatted: "group_missing-name-b06d1",
stats: {
    "name": "All Requests",
    "numberOfRequests": {
        "total": "45780",
        "ok": "28364",
        "ko": "17416"
    },
    "minResponseTime": {
        "total": "0",
        "ok": "1",
        "ko": "0"
    },
    "maxResponseTime": {
        "total": "136",
        "ok": "136",
        "ko": "45"
    },
    "meanResponseTime": {
        "total": "4",
        "ok": "5",
        "ko": "3"
    },
    "standardDeviation": {
        "total": "6",
        "ok": "8",
        "ko": "3"
    },
    "percentiles1": {
        "total": "3",
        "ok": "3",
        "ko": "3"
    },
    "percentiles2": {
        "total": "4",
        "ok": "5",
        "ko": "3"
    },
    "percentiles3": {
        "total": "9",
        "ok": "10",
        "ko": "5"
    },
    "percentiles4": {
        "total": "27",
        "ok": "36",
        "ko": "15"
    },
    "group1": {
    "name": "t < 800 ms",
    "htmlName": "t < 800 ms",
    "count": 28364,
    "percentage": 62
},
    "group2": {
    "name": "800 ms <= t < 1200 ms",
    "htmlName": "t ≥ 800 ms <br> t < 1200 ms",
    "count": 0,
    "percentage": 0
},
    "group3": {
    "name": "t ≥ 1200 ms",
    "htmlName": "t ≥ 1200 ms",
    "count": 0,
    "percentage": 0
},
    "group4": {
    "name": "failed",
    "htmlName": "failed",
    "count": 17416,
    "percentage": 38
},
    "meanNumberOfRequestsPerSecond": {
        "total": "169.556",
        "ok": "105.052",
        "ko": "64.504"
    }
},
contents: {
"req_get--orders-052c3": {
        type: "REQUEST",
        name: "GET /orders",
path: "GET /orders",
pathFormatted: "req_get--orders-052c3",
stats: {
    "name": "GET /orders",
    "numberOfRequests": {
        "total": "45780",
        "ok": "28364",
        "ko": "17416"
    },
    "minResponseTime": {
        "total": "0",
        "ok": "1",
        "ko": "0"
    },
    "maxResponseTime": {
        "total": "136",
        "ok": "136",
        "ko": "45"
    },
    "meanResponseTime": {
        "total": "4",
        "ok": "5",
        "ko": "3"
    },
    "standardDeviation": {
        "total": "6",
        "ok": "8",
        "ko": "3"
    },
    "percentiles1": {
        "total": "3",
        "ok": "3",
        "ko": "3"
    },
    "percentiles2": {
        "total": "4",
        "ok": "5",
        "ko": "3"
    },
    "percentiles3": {
        "total": "9",
        "ok": "10",
        "ko": "5"
    },
    "percentiles4": {
        "total": "27",
        "ok": "36",
        "ko": "15"
    },
    "group1": {
    "name": "t < 800 ms",
    "htmlName": "t < 800 ms",
    "count": 28364,
    "percentage": 62
},
    "group2": {
    "name": "800 ms <= t < 1200 ms",
    "htmlName": "t ≥ 800 ms <br> t < 1200 ms",
    "count": 0,
    "percentage": 0
},
    "group3": {
    "name": "t ≥ 1200 ms",
    "htmlName": "t ≥ 1200 ms",
    "count": 0,
    "percentage": 0
},
    "group4": {
    "name": "failed",
    "htmlName": "failed",
    "count": 17416,
    "percentage": 38
},
    "meanNumberOfRequestsPerSecond": {
        "total": "169.556",
        "ok": "105.052",
        "ko": "64.504"
    }
}
    }
}

}

function fillStats(stat){
    $("#numberOfRequests").append(stat.numberOfRequests.total);
    $("#numberOfRequestsOK").append(stat.numberOfRequests.ok);
    $("#numberOfRequestsKO").append(stat.numberOfRequests.ko);

    $("#minResponseTime").append(stat.minResponseTime.total);
    $("#minResponseTimeOK").append(stat.minResponseTime.ok);
    $("#minResponseTimeKO").append(stat.minResponseTime.ko);

    $("#maxResponseTime").append(stat.maxResponseTime.total);
    $("#maxResponseTimeOK").append(stat.maxResponseTime.ok);
    $("#maxResponseTimeKO").append(stat.maxResponseTime.ko);

    $("#meanResponseTime").append(stat.meanResponseTime.total);
    $("#meanResponseTimeOK").append(stat.meanResponseTime.ok);
    $("#meanResponseTimeKO").append(stat.meanResponseTime.ko);

    $("#standardDeviation").append(stat.standardDeviation.total);
    $("#standardDeviationOK").append(stat.standardDeviation.ok);
    $("#standardDeviationKO").append(stat.standardDeviation.ko);

    $("#percentiles1").append(stat.percentiles1.total);
    $("#percentiles1OK").append(stat.percentiles1.ok);
    $("#percentiles1KO").append(stat.percentiles1.ko);

    $("#percentiles2").append(stat.percentiles2.total);
    $("#percentiles2OK").append(stat.percentiles2.ok);
    $("#percentiles2KO").append(stat.percentiles2.ko);

    $("#percentiles3").append(stat.percentiles3.total);
    $("#percentiles3OK").append(stat.percentiles3.ok);
    $("#percentiles3KO").append(stat.percentiles3.ko);

    $("#percentiles4").append(stat.percentiles4.total);
    $("#percentiles4OK").append(stat.percentiles4.ok);
    $("#percentiles4KO").append(stat.percentiles4.ko);

    $("#meanNumberOfRequestsPerSecond").append(stat.meanNumberOfRequestsPerSecond.total);
    $("#meanNumberOfRequestsPerSecondOK").append(stat.meanNumberOfRequestsPerSecond.ok);
    $("#meanNumberOfRequestsPerSecondKO").append(stat.meanNumberOfRequestsPerSecond.ko);
}
