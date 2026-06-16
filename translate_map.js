// 英译中映射表 - 独立配置文件
const remarkTranslateMap = {
    "No longer needed": "不再需要",
    "Too small": "尺码太小",
    "Too big": "尺码太大",
    "Don't like the material": "不喜欢材质",
    "Don't like the color": "不喜欢颜色",
    "Don't want it": "不想要",
    "Missed expected delivery time": "错过预计送达时间",
    "Ordered wrong item": "订购了错误的商品",
    "Style doesn't match": "风格不符",
    "Need exchange": "需要换货",
    "Can't be delivered / rejected": "无法送达/被拒绝",
    "No reason": "无理由",
    "Not as described": "与描述不符",
    "Poor quality": "质量差",
    "Too large":"太大",
    "Too tight":"太紧",
    "Too long":"太长",
    "Small":"太小",
    "Too short":"太短",
    "Too thin":"太薄",
    "Not needed":"不需要",
    "Big":"太大",
    "Don't need":"不需要",
    "Na":"不适用或无",
    "All over":"到处都是",
    "Changed Mind":"改变主意",
    "Large":"大的",
    "Chest":"箱子/胸部/资金",
    "Overall":"总体",
    "Too wide":"太宽了",
    "no longer needed":"不再需要",
    "Bust":"破碎",
    "Style not as expected":"风格不符预期",
    "Not as expected":"与预期不符",
    "Long":"长",
    "Short":"短",
    "Arrived too late":"来的太迟",
    "Everywhere":"到处",
    "To small":"太小了",
    "No":"不",
    "Did not like":"不喜欢",
    "Did not want":"不想要",
    "To large":"太大",
    "Too tight":"太紧",
    "Too small in waist":"腰围太小",
    "Too late":"来的太迟",
    "Shoulders":"肩膀",
    "Too thin":"太薄",
    "Too loose":"太松",
    "Overall too small":"整体太小",
    "Didn't like":"没有喜欢",
    "Don't like":"不喜欢",
    "Didn't use":"未使用",
    "Not needed":"不需要",
    "Does not fit":"不符合预期",
    "Didn't like fabric":"不喜欢面料",
    "Length":"长度",
    "Overall too big":"整体太大",
    "Way too big":"太大了",
    "To big":"太大",
    "No longer need":"不再需要",
    "Don't need":"不需要",
    "Too big overall":"整体太大",
    "Too big all over":"到处都太大了",
    "Do not need":"不需要",
    "No need":"不需要",
    "Chose another option":"选择了另一个选项",
    "Stomach":"肚子",
    "Too small.":"太小",
    "Too small overall":"整体太小",
    "Too large all over":"到处都太大了",
    "Runs small":"太小了",
    "Arrived to late":"来的太迟",
    "Changed my mind":"改变主意",
    "Never was a tag.":"没有标签",
    "Never was a tag":"没有标签",
    "Too boxy":"太方正了",
    "Wrong size":"尺码错误",
    "Too large overall":"整体太大",
    "To tight":"太紧",
    "Overall too large":"整体太大",
    "Doesn't fit":"不合适",
    "Tight":"太紧",
    "Don't want":"不想",
   };

// 提前把映射表 key 全部转小写，提升匹配效率
const lowerTranslateMap = {};
for (const key in remarkTranslateMap) {
    lowerTranslateMap[key.toLowerCase()] = remarkTranslateMap[key];
}

// 翻译方法 - 无视大小写匹配
function translateRemark(text) {
    if (!text) return "无";
    const trimmed = text.trim();
    const lowerText = trimmed.toLowerCase();
    
    // 小写匹配
    if (lowerTranslateMap[lowerText]) {
        return `${trimmed}<br><span style="color:#F3D77C">${lowerTranslateMap[lowerText]}</span>`;
    }
    return trimmed;
}