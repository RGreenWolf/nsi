function generateTruthTable(expression) {
    const variables = [...new Set(expression.match(/[A-Z]/g))];
    const numVariables = variables.length;
    const numRows = Math.pow(2, numVariables);
    const truthTable = [];
    function evaluateExpression(expression, values) {
        const replacedExpr = expression.replace(/[A-Z]/g, variable => values[variable]);
        return eval(replacedExpr.replace(/\+/g, '||').replace(/\./g, '&&')) ? 1 : 0;
    }
    for (let i = 0; i < numRows; i++) {
        const values = {};
        variables.forEach((variable, index) => {
            values[variable] = (i >> (numVariables - index - 1)) & 1;
        });
        const result = evaluateExpression(expression, values);
        truthTable.push({ ...values, Result: result });
    }
    console.table(truthTable);
}

generateTruthTable("(A+B).C");