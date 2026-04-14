const fs = require('fs');
const path = require('path');

const folders = [
  'C:\\Users\\Administrator\\Desktop\\666产品图',
  'C:\\Users\\Administrator\\Desktop\\666产品宣传图', 
  'C:\\Users\\Administrator\\Desktop\\666用户分享照',
  'C:\\Users\\Administrator\\Desktop\\666素材',
  'C:\\Users\\Administrator\\Desktop\\椒麻牛肉',
];

for (const folder of folders) {
  try {
    const files = fs.readdirSync(folder).filter(f => /\.(jpg|jpeg|png|webp)$/i.test(f));
    console.log(`\n📁 ${folder} (${files.length} images)`);
    for (const f of files) {
      const fp = path.join(folder, f);
      const stat = fs.statSync(fp);
      console.log(`  ${f} (${(stat.size/1024).toFixed(0)}KB)`);
    }
  } catch(e) {
    console.log(`\n📁 ${folder} - ERROR: ${e.message}`);
  }
}
