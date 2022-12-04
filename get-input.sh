set -e -u
set -o noclobber

day=${1:?missing day}
outfile=input$(printf '%02d' $day).txt

curl 'https://adventofcode.com/2022/day/'$day'/input' \
-X 'GET' \
-H "$AOC_COOKIES" \
-H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' \
-H 'Accept-Encoding: gzip, deflate, br' \
-H 'Host: adventofcode.com' \
-H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15' \
-H 'Accept-Language: en-GB,en;q=0.9' \
-H 'Referer: https://adventofcode.com/2022/day/2' \
-H 'Connection: keep-alive' \
| zcat > $outfile
