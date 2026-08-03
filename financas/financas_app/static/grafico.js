function criarGraficoCategorias(labels, valores) {
    const ctx = document.getElementById('graficoCategorias');
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                label: 'Gastos por categoria',
                data: valores,
                backgroundColor: ['#1B3A2B', '#2F7A5C', '#C1554D', '#C9A227', '#6B7268', '#8FA998']
            }]
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('graficoCategorias');
    const labels = JSON.parse(canvas.dataset.categorias);
    const valores = JSON.parse(canvas.dataset.valores);
    criarGraficoCategorias(labels, valores);
});