const jurusan =
    document.getElementById("jurusan");

const fakultas =
    document.getElementById("fakultas");

const semester =
    document.getElementById("semester");

jurusan.addEventListener(
    "change",
    function () {
        if (this.value === "Ekonomi") {
            fakultas.value =
                "Fakultas Ekonomi dan Bisnis";
            semester.value =
                "2";
        }
        else if (
            this.value ===
            "Teknik Informatika"
        ) {
            fakultas.value =
                "Fakultas Sains danTeknik";
            semester.value =
                "6";
        }
        else {
            fakultas.value = "";
            semester.value = "";
        }
    }
);