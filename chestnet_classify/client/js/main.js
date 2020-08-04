let img_result = document.querySelector(".img-result");
let save = document.querySelector(".save");
let cropped = document.querySelector(".cropped");
let cropper = null;

const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    legend: {
        position: 'top',
    },
    title: {
        display: true,
        text: 'Kết quả dự đoán của 3 mô hình'
    },
    scales: {
        yAxes: [{
            ticks: {
                min: 0,
                max: 100
            }
        }],
        xAxes: [{
            ticks: {
                autoSkip: false,
                maxRotation: 90,
                minRotation: 90
            }
        }]
    }
};

function displayImages(labels, heatmaps, container) {
    for (let i = 0; i < labels.length; i++) {
        $('#' + container + ' div.row').append(`
            <div class="pred-img col-3">
                <img src="${heatmaps[i]}" />
                <p>${labels[i]}</p>
            </div>
        `);
    }
}

const reader = new FileReader();
reader.onload = e => {
    if (e.target.result) {
        let img = $("#source-img");
        img.attr('src', e.target.result);
        cropper = new Cropper(img.get(0));
    }
};

$('#choose-image').click(() => $('#file-input').click());

$('#file-input').on("change", e => {
    if (e.target.files.length) {
        reader.readAsDataURL(e.target.files[0]);
    }
});

$('#analyse').on("click", () => {
    let imgSrc = cropper.getCroppedCanvas({ width: 300 }).toDataURL();
    $('#source-img').attr('src', imgSrc);
    cropper.destroy();
    $.post("http://127.0.0.1:5000/classify", JSON.stringify({ image: imgSrc }), (resp) => {
        console.log(resp);
        if (!resp.data.success) {
            console.log("Fail to predict image");
            return;
        }

        let predDensenet121 = resp.data.prediction['predictions_densenet121'];
        let predMobilenet = resp.data.prediction['predictions_mobilenet'];
        let predVgg16 = resp.data.prediction['predictions_vgg16'];
        let thDensenet121 = resp.data.prediction.thresholds['densenet121'];
        let thMobilenet = resp.data.prediction.thresholds['mobilenet'];
        let thVgg16 = resp.data.prediction.thresholds['vgg16'];
        // let computedPred = resp.data.prediction['predictions_compute'];

        let dataDensenet = Object.values(predDensenet121);
        let dataMobilenet = Object.values(predMobilenet);
        let dataVgg16 = Object.values(predVgg16);
        // let dataCompute = Object.values(computedPred);
        let labels = Object.keys(predDensenet121);

        if (window.chartPred) {
            window.chartPred.data.datasets[0].data = dataDensenet;
            window.chartPred.data.datasets[1].data = dataMobilenet;
            window.chartPred.data.datasets[2].data = dataVgg16;

            window.chartPred.update();
        } else {
            let chartData = {
                labels: labels,
                datasets: [{
                    label: 'Densenet121',
                    backgroundColor: 'rgb(254, 118, 122)',
                    data: dataDensenet
                }, {
                    label: 'Mobilenet',
                    backgroundColor: 'rgb(255, 206, 86)',
                    data: dataMobilenet
                }, {
                    label: 'VGG16',
                    backgroundColor: 'rgb(54, 162, 235)',
                    data: dataVgg16
                }]
            };
        
            window.chartPred = new Chart('chart-pred', {
                type: 'bar',
                data: chartData,
                options: chartOptions
            });
        }

        for (let i = 0; i < labels.length; i++) {
            $('#thresholds').append(`
                <tr>
                    <th>${labels[i]}</th>
                    <td class="table-danger">${thDensenet121[i]}</td>
                    <td class="table-warning">${thMobilenet[i]}</td>
                    <td class="table-primary">${thVgg16[i]}</td>
                </tr>
            `);
        };

        // Hình ảnh chẩn đoán
        // densenet121
        let densenet121Labels = resp.data.prediction.predictions_labels['densenet121']
        let densenet121Heatmaps = resp.data.prediction.heatmaps['densenet121']
        displayImages(densenet121Labels, densenet121Heatmaps, 'densenet-pred-images');

        // mobilenet
        let mobilenetLabels = resp.data.prediction.predictions_labels['mobilenet']
        let mobilenetHeatmaps = resp.data.prediction.heatmaps['mobilenet']
        displayImages(mobilenetLabels, mobilenetHeatmaps, 'mobile-pred-images');

        // vgg16
        // let vgg16Labels = resp.data.prediction.predictions_labels['vgg16']
        // let vgg16Heatmaps = resp.data.prediction.heatmaps['vgg16']
        // displayImages(vgg16Labels, vgg16Heatmaps, 'vgg-pred-images');
    });
});