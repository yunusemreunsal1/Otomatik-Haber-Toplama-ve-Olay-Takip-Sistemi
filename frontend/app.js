const form = document.getElementById("filtre");
const liste = document.getElementById("liste");
const sayac = document.getElementById("sayac");

async function haberleriGetir() {
    const parametreler = new URLSearchParams(new FormData(form));
    const cevap = await fetch("/api/haberler?" + parametreler);
    const haberler = await cevap.json();

    liste.innerHTML = "";
    sayac.textContent = haberler.length + " haber bulundu";

    for (const haber of haberler) {
        const li = document.createElement("li");

        const baslik = document.createElement("a");
        baslik.href = haber.link;
        baslik.target = "_blank";
        baslik.textContent = haber.baslik;

        const bilgi = document.createElement("small");
        bilgi.textContent = haber.kaynak + " | " + haber.tarih + " | " + haber.kategori;
        if (haber.sehir) {
            bilgi.textContent += " | " + haber.sehir;
        }

        li.append(baslik, bilgi);
        liste.append(li);
    }
}

form.addEventListener("submit", function (olay) {
    olay.preventDefault();
    haberleriGetir();
});

haberleriGetir();
