/**
 * upload_to_ima.js
 * ================
 * 将公考面试题 md 文件上传到 IMA 笔记。
 *
 * 用法：
 *   node <skill-path>/scripts/upload_to_ima.js "<md文件路径>" "<笔记标题>"
 *
 * 参数：
 *   argv[2] = md 文件路径（本地文件，读取内容后上传）
 *   argv[3] = 笔记标题（含时间戳，如 "综合分析_指尖形式主义_20260723_153000"）
 *
 * 流程：读取 md -> 在 H1 标题后追加时间戳 -> 调用 IMA import_doc 创建笔记
 * 上传失败不阻断主流程，在 stderr 输出警告即可。
 */
const fs = require('fs');
const path = require('path');
const { imaApi } = require(path.join(__dirname, '..', '..', 'ima-skill', 'ima_api.cjs'));

async function main() {
  const mdPath = process.argv[2];
  const noteTitle = process.argv[3];

  if (!mdPath || !noteTitle) {
    console.error('Usage: node upload_to_ima.js "<mdFilePath>" "<noteTitle>"');
    process.exit(1);
  }

  let md = fs.readFileSync(mdPath, 'utf8');
  // 在 H1 标题后追加时间戳
  md = md.replace(/^# (.+)$/m, `# $1_${noteTitle}`);

  const resp = await imaApi('openapi/note/v1/import_doc', {
    content_format: 1,
    content: md,
    folder_name: '公考面试题库'
  });
  const data = JSON.parse(resp);
  if (data.code === 0) console.log('✅ IMA note_id:', data.data.note_id);
  else console.error('⚠️ IMA上传失败:', data.msg);
}

main().catch(err => console.error('⚠️ upload_to_ima.js 异常:', err.message));
