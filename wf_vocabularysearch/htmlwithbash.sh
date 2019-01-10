# @Author: pmz
# @Date:   2018-12-27 14:57:30
# @Last Modified by:   pmz
# @Last Modified time: 2018-12-27 18:07:56

query=$1
HOST="https://www.vocabulary.com/dictionary"
query_url="$HOST/$query"
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
html_data=`/usr/local/bin/wget -qO- $query_url`
sho_defi=`echo "$html_data" | /usr/local/bin/pup 'div[class="section blurb"] p[class="short"] text{}' | tr -d '\n'`

# short_defini=`cat "$DIR/$query.html" | pup 'div[class="section blurb"] p[class="short"] text{}'`
# cat << EOF
# $(echo $sho_defi | tr -d '\n')
# EOF

json_itms="{
    \"items\": [{
        \"uid\": \"desktop\",
        \"type\": \"file\",
        \"title\": \"Desktop\",
        \"subtitle\": \"~/Desktop\",
        \"arg\": \"~/Desktop\",
        \"autocomplete\": \"Desktop\",
        \"icon\": {
            \"type\": \"fileicon\",
            \"path\": \"~/Desktop\"
        }
    }]
}"
wf_items=`echo $json_itms | /usr/local/bin/jq '.'`
cat << EOF
$(echo $wf_items)
EOF