import urllib.request
import re

playlists = [
    ("Desi Channel", "https://raw.githubusercontent.com/abrarpro/iptv.m3u/refs/heads/main/Desi%20Channel.m3u8"),
    ("Cartoon TV", "https://raw.githubusercontent.com/abrarpro/iptv.m3u/refs/heads/main/cartoon.m3u"),
    ("Channel X", "https://raw.githubusercontent.com/ahan443/FreeHunter/refs/heads/main/otherseller.m3u"),
    ("Channel X2", "https://raw.githubusercontent.com/ahan443/FreeHunter/refs/heads/main/uyycbr.m3u"),
    ("Channel X3", "https://raw.githubusercontent.com/ahan443/FreeHunter/refs/heads/main/171126.m3u"),
    ("Channel X4", "https://raw.githubusercontent.com/ahan443/FreeHunter/refs/heads/main/161126.m3u"),
    ("OTT TV", "https://raw.githubusercontent.com/ahan443/FreeHunter/refs/heads/main/12112026.m3u"),
    ("OPTV", "https://raw.githubusercontent.com/ahan443/FreeHunter/refs/heads/main/0611261.m3u"),
]

output_lines = ["#EXTM3U\n"]

for group_name, url in playlists:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as response:
            content = response.read().decode("utf-8", errors="ignore")
        
        lines = [line.strip() for line in content.splitlines() if line.strip()]
        for line in lines:
            if line.startswith("#EXTM3U"):
                continue
            if line.startswith("#EXTINF:"):
                if 'group-title="' in line:
                    line = re.sub(r'group-title="[^"]*"', f'group-title="{group_name}"', line)
                else:
                    line = line.replace("#EXTINF:-1", f'#EXTINF:-1 group-title="{group_name}"', 1)
                output_lines.append(line + "\n")
            else:
                output_lines.append(line + "\n")
    except Exception as e:
        print(f"Error fetching {group_name}: {e}")

with open("combined.m3u", "w", encoding="utf-8") as f:
    f.writelines(output_lines)
