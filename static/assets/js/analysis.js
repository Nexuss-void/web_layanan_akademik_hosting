const analysis =
    JSON.parse(
        document.getElementById(
            'analysis-data'
        ).textContent
    );
let index = 1;

for (const category in analysis) {
    const ctx =
        document.getElementById(
            "chart" + index
        );
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: [
                'Sangat Puas',
                'Puas',
                'Tidak Puas',
                'Sangat Tidak Puas'
            ],
            datasets: [{
                data: [
                    analysis[category]['Sangat Puas'],
                    analysis[category]['Puas'],
                    analysis[category]['Tidak Puas'],
                    analysis[category]['Sangat Tidak Puas']
                ],
                backgroundColor: [
                    '#22c55e',
                    '#3b82f6',
                    '#f59e0b',
                    '#ef4444'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
    index++;
}