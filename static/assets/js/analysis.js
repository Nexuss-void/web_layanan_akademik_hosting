const analysisElement = document.getElementById('analysis-data');

if (analysisElement) {
    const analysis = JSON.parse(analysisElement.textContent);
    let index = 1;
    for (const category in analysis) {
        const ctx = document.getElementById("chart" + index);
        if (ctx) {
            const catData = analysis[category];
            const baseLabels = ['Sangat Puas', 'Puas', 'Tidak Puas', 'Sangat Tidak Puas'];
            const formattedLabels = baseLabels.map(label => {
                const val = catData[label] || 0;
                return `${val}% ${label}`;
            });
            new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: formattedLabels,
                    datasets: [{
                        data: [
                            catData['Sangat Puas'],
                            catData['Puas'],
                            catData['Tidak Puas'],
                            catData['Sangat Tidak Puas']
                        ],
                        backgroundColor: [
                            '#10b981',
                            '#0284c7',
                            '#eab308',
                            '#ef4444'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: {
                                padding: 12,
                                usePointStyle: true,
                                font: {
                                    size: 12,
                                    weight: '500'
                                }
                            }
                        }
                    }
                }
            });
        }
        index++;
    }
}