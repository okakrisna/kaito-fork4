# Kaito (salinan lokal)

Proyek ini adalah salinan statis yang di-branding menjadi `kaito.com`. Struktur `wp-admin`, `wp-content`, `wp-includes` bersifat referensi; halaman yang bisa dibuka secara lokal ada di folder `timeless`.

## Cara Menjalankan (Windows)

- Pastikan Python terpasang. Cek: `python --version`
- Jalankan server lokal dari folder: `c:\Users\okakr\Downloads\new 2\kaito.com\kaito.com`
- Perintah: `python -m http.server 8000`
- Buka di browser: `http://localhost:8000/` (otomatis redirect ke `timeless/`)

Alternatif jika memiliki Node.js:
- Dari folder yang sama: `npx serve@latest .`
- Buka URL yang ditampilkan (biasanya `http://localhost:3000`)

## Mengedit Konten

- File utama: `kaito.com/timeless/index.html`
- Banyak aset di halaman ini memakai URL absolut `https://groovepublic.com/...`. Itu artinya halaman lokal tetap akan memuat aset dari situs live.
- Anda bisa mengubah teks, gambar, atau gaya di `index.html` langsung. Simpan perubahan, lalu refresh browser.

## Catatan

- Fitur dinamis WordPress (PHP, admin, database) tidak aktif dalam salinan statis ini.
- Jika ingin migrasi ke proyek statis penuh, kita bisa menyesuaikan referensi aset menjadi lokal (butuh langkah tambahan).

## Panduan Penggantian Konten (Video, Foto, Tulisan, Font)

Berikut cara mengganti konten utama di halaman `timeless`.

### Mengganti Video Background

- Letakkan berkas video di folder: `kaito.com/kaito.com/timeless/assets/`
- Gunakan format yang didukung browser (disarankan `mp4`, H.264/AAC). Nama contoh: `backgroundvideo.test.mp4`.
- Edit `timeless/index.html` pada container yang memakai video background. Cari baris yang mengandung `background_video_link`:

  ```html
  <div ... data-settings="{... \"background_video_link\": \"/timeless/assets/backgroundvideo.test.mp4\", ...}">
      <video class="elementor-background-video-hosted elementor-html5-video" autoplay muted playsinline loop>
          <source src="/timeless/assets/backgroundvideo.test.mp4" type="video/mp4">
      </video>
  </div>
  ```

- Ganti kedua path ke nama file video baru Anda, misalnya `/timeless/assets/my-background.mp4`.
- Refresh browser di `http://localhost:8000/index.html`.

Tips:
- Ukuran optimal video background biasanya 10–30 MB, durasi pendek, loop halus.
- Jika video tidak tampil: cek nama file persis, codec kompatibel, dan pastikan file benar-benar berada di folder `assets`.

### Mengganti Foto / Gambar

- Banyak gambar saat ini direferensikan dari `/wp-content/uploads/...` (aset live). Anda bisa:
  - Tetap pakai URL live; atau
  - Pindahkan gambar lokal ke `timeless/assets/images/` (buat folder jika belum ada) dan pakai path lokal, misalnya `/timeless/assets/images/hero.jpg`.
- Edit `timeless/index.html` dan cari atribut seperti `data-dce-background-image-url` atau tag `<img src="...">`.
- Contoh penggantian:

  ```html
  <div data-dce-background-image-url="/timeless/assets/images/hero.jpg" ...>
  ```

### Mengganti Tulisan (Teks)

- Buka `timeless/index.html`, lalu cari elemen teks seperti `elementor-widget-heading` dan `elementor-widget-text-editor`.
- Anda bisa cari teks yang ingin diubah dengan fitur pencarian, lalu edit langsung isi di dalam tag heading/paragraph yang bersangkutan.
- Simpan, lalu refresh browser.

### Mengganti Video YouTube di Section Video

- Cari widget `elementor-widget-video` yang memiliki `youtube_url`.
- Ubah nilai `youtube_url` ke tautan YouTube baru Anda, atau ganti widget tersebut dengan `<video>` lokal seperti di bagian Video Background jika ingin memakai file `.mp4`.

### Mengganti Font

- Font eksternal ke domain `is3.cloudhost.id` sudah dihapus. Font yang aktif saat ini memuat dari `/wp-content/...` atau bisa Anda tambahkan lokal.
- Opsi lokal: simpan font ke `timeless/assets/fonts/`, lalu tambahkan deklarasi `@font-face` di berkas CSS yang relevan atau di `<style>` di `index.html`:

  ```css
  @font-face {
    font-family: 'NamaFontSaya';
    font-weight: 400;
    src: url('/timeless/assets/fonts/NamaFontSaya-Regular.woff2') format('woff2');
  }
  ```

- Setelah itu, terapkan dengan `font-family: 'NamaFontSaya';` di elemen yang diinginkan.

### Konvensi Path Aset Lokal

- Video: `/timeless/assets/<nama-file>.mp4`
- Gambar: `/timeless/assets/images/<nama-file>.<ext>`
- Font: `/timeless/assets/fonts/<nama-file>.<ext>`

### Troubleshooting

- Video tidak tampil: pastikan path benar, tipe file `mp4`, codec kompatibel (H.264/AAC), dan file benar-benar ada.
- Gambar tidak muncul: cek path dan case-sensitive nama file, serta cache browser (Ctrl+F5).
- Font tidak berubah: pastikan `@font-face` terpasang dan CSS diterapkan pada elemen yang tepat.

### Menjalankan Ulang Server Lokal

- Jika Anda menambah/mengubah banyak aset, cukup refresh browser. Jika server lokal mati, jalankan lagi:
  - Dari folder: `c:\Users\okakr\Downloads\new 2\groovepublic.com\groovepublic.com`
  - Perintah: `python -m http.server 8000`
  - Buka: `http://localhost:8000/index.html`