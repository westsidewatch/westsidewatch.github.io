// Narrative chapters sample the existing timeline. They do not certify the
// within-period dates, ancient ground, or reuse of a predecessor's fabric.
export const SACRED_RIDGE_START=3.08;
export const SACRED_RIDGE_END=8.94;
export const SACRED_RIDGE_CHAPTERS=Object.freeze([
 {at:3.08,id:'david',title:'大衛城：南部山脊',text:'先看南部大衛城，再沿山脊看向北部高處；禾場位置為關聯區示意。',view:'ridge'},
 {at:3.45,id:'solomon',title:'所羅門：第一聖殿',text:'視線轉向北部聖殿與宮殿區，對照南部大衛城的高低差；建築與區位仍有推定。',view:'first'},
 {at:3.75,id:'first-near',title:'第一聖殿：建築群近看',text:'從山脊關係推近殿院與宮殿區；推定位置和建築細節不等於實測復原。',view:'first-near'},
 {at:4,id:'first-late',title:'第一聖殿晚期：城市擴展',text:'保留聖殿山脊方向，觀察城市擴展；不把示意模型視為考古定案。',view:'first-near'},
 {at:5,id:'destruction',title:'巴比倫毀城：延續中的斷裂',text:'在同一觀察區域看毀壞；不跳過第一聖殿與第二聖殿之間的斷裂。',view:'first-near'},
 {at:6,id:'second',title:'重建：早期第二聖殿',text:'同一山脊上的重建，不代表沿用第一聖殿的原牆或地基。',view:'second'},
 {at:6.55,id:'second-near',title:'第二聖殿：重建後的殿院',text:'推近早期第二聖殿的主殿、院落與入口，與其後希律擴建作比較。',view:'second-near'},
 {at:7,id:'hasmonean',title:'第二聖殿：希臘化與哈斯蒙尼',text:'第二聖殿時期仍在發展；希律工程是其後的大規模改建與擴建。',view:'second-near'},
 {at:8,id:'herodian',title:'希律：第二聖殿的擴建',text:'拉開至整個聖殿建築群，觀看院落、柱廊與南西側通道；希律聖殿屬第二聖殿的改建階段。',view:'herodian'},
]);
export function sacredRidgeChapter(position){return [...SACRED_RIDGE_CHAPTERS].reverse().find(c=>position>=c.at)||SACRED_RIDGE_CHAPTERS[0];}
