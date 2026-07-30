// GROUPED BAR CHART CONFIGURATION (HEDPERF Per Fakultas dalam %)
const ctxBar = document.getElementById('barChart').getContext('2d');
new Chart(ctxBar, {
    type: 'bar',
    data: {
        labels: categoryLabels,
        datasets: [
            {
                label: 'FAST (%)',
                data: dataFast,
                backgroundColor: '#0284c7', // Sky Blue
                borderRadius: 4,
                barPercentage: 0.7,
                categoryPercentage: 0.6
            },
            {
                label: 'FEB (%)',
                data: dataFeb,
                backgroundColor: '#16a34a', // Emerald Green
                borderRadius: 4,
                barPercentage: 0.7,
                categoryPercentage: 0.6
            }
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            x: {
                grid: { display: false },
                ticks: {
                    font: { size: 11, family: 'system-ui' },
                    color: '#475569'
                }
            },
            y: {
                beginAtZero: true,
                min: 0,
                max: 100, // Skala Sumbu Y 0 - 100%
                ticks: {
                    precision: 0,
                    font: { size: 11, family: 'system-ui' },
                    color: '#475569',
                    callback: function (value) {
                        return value + "%";
                    }
                },
                grid: { color: '#f1f5f9' }
            }
        },
        plugins: {
            legend: {
                position: 'top',
                labels: {
                    padding: 12,
                    font: { size: 12, weight: '500', family: 'system-ui' },
                    usePointStyle: true
                }
            },
            tooltip: {
                callbacks: {
                    label: function (context) {
                        return context.dataset.label + ': ' + context.parsed.y + '%';
                    }
                }
            }
        }
    }
});

// 3. PIE CHART CONFIGURATION (Tingkat Kepuasan Ordinal)
document.addEventListener('DOMContentLoaded', function () {
    // 🟢 Ambil data dari window (HTML) atau default ke array 0
    const rawData = window.pieRawData || [0, 0, 0, 0];
    const baseLabels = window.pieBaseLabels || ['Sangat Puas', 'Puas', 'Tidak Puas', 'Sangat Tidak Puas'];

    const total = rawData.reduce((a, b) => a + b, 0);

    // Format Label Persentase
    const formattedLabels = baseLabels.map((label, index) => {
        const value = rawData[index];
        const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : 0;
        return `${percentage}% ${label}`;
    });

    const pieElement = document.getElementById('pieChart');

    if (pieElement) {
        const ctxPie = pieElement.getContext('2d');

        new Chart(ctxPie, { // 🟢 Disamakan menjadi ctxPie
            type: 'pie',
            data: {
                labels: formattedLabels,
                datasets: [{
                    data: rawData,
                    backgroundColor: ['#10b981', '#0284c7', '#eab308', '#ef4444']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 16,
                            usePointStyle: true,
                            font: {
                                size: 13,
                                weight: '500'
                            }
                        }
                    }
                }
            }
        });
    }
});