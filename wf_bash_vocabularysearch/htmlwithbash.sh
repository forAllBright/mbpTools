# @Author: pmz
# @Date:   2018-12-27 14:57:30
# @Last Modified by:   pmz
# @Last Modified time: 2018-12-29 15:33:17

########################################### Fetching definition #######################################################
query=$1
HOST="https://www.vocabulary.com/dictionary"
query_url="$HOST/$query"
# DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
html_data=`/usr/local/bin/wget -qO- $query_url`
short_defi_text=`echo "$html_data" | /usr/local/bin/pup 'div[class="section blurb"] p[class="short"] text{}' | tr -d '\n'`
# short_defi_text=`cat "$DIR/$query.html" | /usr/local/bin/pup 'div[class="section blurb"] p[class="short"] text{}'`
if [ -z "$short_defi_text"]; then
cat << EOF
$(echo "<?xml version=\"1.0\" encoding=\"utf-8\"?>
<items>
  <item valid=\"yes\">
    <title>Searching...</title>
  </item>
</items>")
EOF
exit 1
fi


############################################# init workflow items ######################################################
init_xml="<?xml version=\"1.0\" encoding=\"utf-8\"?>
<items>
  <item valid=\"yes\">
    <title></title>
    <subtitle></subtitle>
    <arg></arg>
    <text type=\"largetype\"></text>
  </item>
</items>"

########################################### Make workflow first item ###########################################
# Make workflow first item, with argumens: title, substitle, arg, text
make_title_item()
{
    echo $init_xml | /usr/local/bin/xmlstarlet ed -a "/items/item[last()]" -t elem -n item -v "" | /usr/local/bin/xmlstarlet ed -s "/items/item[2]" -t elem -n title -v "$1" \
    | /usr/local/bin/xmlstarlet ed -s "/items/item[2]" -t elem -n subtitle -v "$2" | /usr/local/bin/xmlstarlet ed -s "/items/item[2]" -t elem -n arg -v "$3" \
    | /usr/local/bin/xmlstarlet ed -s "/items/item[2]" -t elem -n text -v "$4" -i "/items/item[2]/text" -t attr -n type -v "largetype" | /usr/local/bin/xmlstarlet ed -d "/items/item[1]"
}

########################################### Make workflow following item ###########################################
# Make workflow following item, with argumens: title, substitle, arg, text
add_other_item()
{
    echo "$1" | /usr/local/bin/xmlstarlet ed -a "/items/item[last()]" -t elem -n item -v "" | /usr/local/bin/xmlstarlet ed -s "/items/item["$6"]" -t elem -n title -v "$2" \
    | /usr/local/bin/xmlstarlet ed -s "/items/item["$6"]" -t elem -n subtitle -v "$3" | /usr/local/bin/xmlstarlet ed -s "/items/item["$6"]" -t elem -n arg -v "$4" \
    | /usr/local/bin/xmlstarlet ed -s "/items/item["$6"]" -t elem -n text -v "$5"
}

########################################### Add items to workflow ###########################################
# First item: title, substitle, arg, text
tp=`make_title_item "$short_defi_text" "" "" "$short_defi_text"`
# # Following items: title, substitle, arg, text
# tmp=""
# index=2
# for i in "JK" "LP" "PP"; do
#     tmp=`add_other_item "$tp" "$i" "" "" "HERE" "$index"`
#     tp=$tmp
#     index=$(($index+1))
# done


cat << EOF
$(echo $tp)
EOF
