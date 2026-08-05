Chart.defaults.font.family = "'Inter', sans-serif";
Chart.defaults.color = '#6B7268';

function criarGraficoCategorias(labels, valores) {
    const ctx = document.getElementById('graficoCategorias');
    const total = valores.reduce((soma, v) => soma + v, 0);

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: valores,
                backgroundColor: ['#1B3A2B', '#2F7A5C', '#C1554D', '#C9A227', '#8FA998', '#6B7268'],
                borderColor: '#FFFFFF',
                borderWidth: 3,
                hoverOffset: 8
            }]
        },
        options: {
            cutout: '68%',
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { padding: 16, usePointStyle: true, pointStyle: 'circle' }
                },
                tooltip: {
                    backgroundColor: '#1B3A2B',
                    titleFont: { family: "'Fraunces', serif", size: 14 },
                    bodyFont: { size: 13 },
                    padding: 12,
                    cornerRadius: 8,
                    callbacks: {
                        label: (ctx) => {
                            const pct = ((ctx.parsed / total) * 100).toFixed(1);
                            return ` R$ ${ctx.parsed.toFixed(2)} (${pct}%)`;
                        }
                    }
                }
            }
        },
        plugins: [{
            id: 'totalCentro',
            beforeDraw(chart) {
                const { ctx, chartArea: { width, height, top, left } } = chart;
                ctx.save();
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.font = "600 1.3rem 'Fraunces', serif";
                ctx.fillStyle = '#1B3A2B';
                ctx.fillText(`R$ ${total.toFixed(0)}`, left + width / 2, top + height / 2 - 8);
                ctx.font = "0.75rem 'Inter', sans-serif";
                ctx.fillStyle = '#6B7268';
                ctx.fillText('total gasto', left + width / 2, top + height / 2 + 14);
                ctx.restore();
            }
        }]
    });
}


document.addEventListener('DOMContentLoaded', () => {
    const canvasCategorias = document.getElementById('graficoCategorias');
    const labels = JSON.parse(canvasCategorias.dataset.categorias);
    const valores = JSON.parse(canvasCategorias.dataset.valores);
    criarGraficoCategorias(labels, valores);

});