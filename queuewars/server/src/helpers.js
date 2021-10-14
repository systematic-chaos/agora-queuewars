function computeSolutions(grid) {
    const solutions = grid.reduce((a, c) => {
        a[c.parent] = a[c.parent] || [];
        a[c.parent].push(c.id);
        return a;
    }, {});
    Object.values(solutions).forEach(v => v.sort());
    return solutions;
}

function arrayEquals(a, b) {
    return a && b && a.length === b.length
            && a.sort().join(',') === b.sort().join(',');
}

function fail(res, code=400, message) {
    res
        .status(code)
        .type("text/plain")
        .send(message);
}

module.exports = {
    arrayEquals,
    computeSolutions,
    fail
};
