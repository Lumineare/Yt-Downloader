from flask import Flask, render_template, request, jsonify
from yt_dlp import YoutubeDL
import os

app = Flask(__name__)

# Tambahkan cookies langsung sebagai string
COOKIES = """
.youtube.com	TRUE	/	FALSE	1771288115	SID	g.a000sQhsNXbdZ5aRfgNLOl21LpRPmBfxoOyuCTuJUmXaALs6wwrveah1fDPm9A7MvHPE9-NHewACgYKAeUSARUSFQHGX2Mie1FZsPtv5O44GvNrFVMT4hoVAUF8yKqZAvN5u332gOaAI_NLMHOK0076
.youtube.com	TRUE	/	TRUE	1771288115	__Secure-1PSID	g.a000sQhsNXbdZ5aRfgNLOl21LpRPmBfxoOyuCTuJUmXaALs6wwrv-6Hn7bjPMp3UCA4v7SRKswACgYKAeYSARUSFQHGX2MiLPPaZkBPGSeZZxAhz-NI7hoVAUF8yKpF3khEH3vXlUY0bOzAe3xl0076
.youtube.com	TRUE	/	TRUE	1771288115	__Secure-3PSID	g.a000sQhsNXbdZ5aRfgNLOl21LpRPmBfxoOyuCTuJUmXaALs6wwrv14J5nuFGm-ldy8bS616ungACgYKAWISARUSFQHGX2MiwfZQUBa5PR7al0LXxLU8jxoVAUF8yKrtkHG6tFgfObqtl_Et_B0-0076
.youtube.com	TRUE	/	FALSE	1771288115	HSID	AaOEZeGYOqmKHpvA2
.youtube.com	TRUE	/	TRUE	1771288115	SSID	ADl39Fd_CTnXhnI2B
.youtube.com	TRUE	/	FALSE	1771288115	APISID	NlmJDOIVp_klfr-b/AS0miY8ingj-BSZDX
.youtube.com	TRUE	/	TRUE	1771288115	SAPISID	EMloDuui35Nwg2AS/AX05MAbOgLV6t4E1b
.youtube.com	TRUE	/	TRUE	1771288115	__Secure-1PAPISID	EMloDuui35Nwg2AS/AX05MAbOgLV6t4E1b
.youtube.com	TRUE	/	TRUE	1771288115	__Secure-3PAPISID	EMloDuui35Nwg2AS/AX05MAbOgLV6t4E1b
.youtube.com	TRUE	/	TRUE	1771288280	LOGIN_INFO	AFmmF2swRQIgFonGGjIorex7Qxtkh4Na9t5JEEpNoq6vqY9IybYE3lcCIQDkSRaXi-tnh0DSn1Q8-Em0BCBbnTKFruE_pp6q0k-R0Q:QUQ3MjNmdzBWU2h3em5tak42Q0RiYmlESzZ2djRZQ3M0Q1I2QWIzYzM1VE8yYWZSQjJST09lUTlyRDNyakVUMEpVYU5HUmR3V05rMWpHeUFtMG5EMGFFNWN5VUNmSWFoR3VnNDg2NmFZSXYxdkxZLUdPRnYyaXZHMzMxaVl2VGNUalZfQVNtSkhBWFp1ekVhby1aeVZ2RXZXZDRBR3NzRXBn
.youtube.com	TRUE	/	TRUE	1771288526	PREF	tz=Asia.Bangkok&f7=100&f4=4000000
.youtube.com	TRUE	/	TRUE	1768264531	__Secure-1PSIDTS	sidts-CjIBmiPuTVgz2KkoJlA4o_E8ra4R-3mZonLsO8yQcmdu1l77BiQrc8WuWMzXYhUwMplqbhAA
.youtube.com	TRUE	/	TRUE	1768264531	__Secure-3PSIDTS	sidts-CjIBmiPuTVgz2KkoJlA4o_E8ra4R-3mZonLsO8yQcmdu1l77BiQrc8WuWMzXYhUwMplqbhAA
"""

def get_video_formats(url):
    """Retrieve available formats for a given video URL."""
    ydl_opts = {
        'quiet': True,
        'noplaylist': True,
        'cookiefile': '-',  # Gunakan '-' untuk menggunakan string cookies
        'cookie_data': COOKIES.strip()  # Tambahkan cookies ke dalam opsi
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = [
            {
                'format_id': f['format_id'],
                'resolution': f.get('resolution', 'audio only'),
                'ext': f['ext'],
                'filesize': f.get('filesize', 'Unknown')
            }
            for f in info['formats'] if 'filesize' in f
        ]
        return formats

@app.route('/get_formats', methods=['POST'])
def get_formats():
    url = request.form['url']
    try:
        formats = get_video_formats(url)
        return jsonify({'success': True, 'formats': formats})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True)
