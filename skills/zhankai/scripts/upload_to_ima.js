/**
 * upload_to_ima.js
 * ================
 * 将"展开说说"长帖内容上传到 IMA 笔记 + 同步到知识库。
 *
 * 用法（从项目根或任意目录执行）：
 *   node <skill-path>/scripts/upload_to_ima.js "<笔记标题>" "<markdown文件路径>"
 *
 * 参数：
 *   argv[2] = 笔记标题（含时间戳，如 "指尖上的形式主义_20260722_153000"）
 *   argv[3] = Markdown 文件路径（临时生成的 md 文件）
 *
 * 流程：
 *   1. 读取 Markdown 文件内容
 *   2. 创建 IMA 笔记（folder: "展开说说"）
 *   3. 搜索"总分总"知识库
 *   4. 搜索"00_结构化考官思维"文件夹
 *   5. 将笔记添加到知识库对应文件夹
 *
 * 注意：笔记创建或知识库同步失败均不阻断主流程，在 stderr 输出警告即可。
 */
const fs = require('fs');
const { imaApi } = require('../../ima-skill/ima_api.cjs');

async function main() {
  const noteTitle = process.argv[2];
  const mdFilePath = process.argv[3];

  if (!noteTitle || !mdFilePath) {
    console.error('Usage: node upload_to_ima.js "<noteTitle>" "<mdFilePath>"');
    process.exit(1);
  }

  const markdownContent = fs.readFileSync(mdFilePath, 'utf-8');

  // ── 1. 创建 IMA 笔记 ──
  const noteResp = await imaApi('openapi/note/v1/import_doc', {
    content_format: 1,
    content: markdownContent,
    folder_name: '展开说说'
  });
  const noteData = JSON.parse(noteResp);
  if (noteData.code !== 0) {
    console.error('⚠️ IMA笔记创建失败:', noteData.msg);
    return;
  }
  const noteId = noteData.data.note_id;
  console.log('✅ IMA笔记 note_id:', noteId);

  // ── 2. 搜索"总分总"知识库 ──
  const kbResp = await imaApi('openapi/wiki/v1/search_knowledge_base', {
    query: '总分总', cursor: '', limit: 20
  });
  const kbData = JSON.parse(kbResp);
  const kbList = (kbData.data && kbData.data.info_list) || [];
  const targetKB = kbList.find(k => k.name.includes('总分总'));
  if (!targetKB) {
    console.error('⚠️ 未找到"总分总"知识库，跳过知识库同步');
    return;
  }
  console.log('✅ 知识库:', targetKB.name, targetKB.id);

  // ── 3. 在知识库中搜索目标文件夹 ──
  const folderResp = await imaApi('openapi/wiki/v1/search_knowledge', {
    query: '00_结构化考官思维',
    knowledge_base_id: targetKB.id,
    cursor: ''
  });
  const folderData = JSON.parse(folderResp);
  const folderList = (folderData.data && folderData.data.info_list) || [];
  const targetFolder = folderList.find(f => f.title && f.title.includes('00_结构化考官思维'));
  const folderId = targetFolder ? targetFolder.media_id : null;
  if (!folderId) {
    console.error('⚠️ 未找到"00_结构化考官思维"文件夹，将添加到知识库根目录');
  } else {
    console.log('✅ 文件夹 folder_id:', folderId);
  }

  // ── 4. 将笔记添加到知识库 ──
  const addBody = {
    media_type: 11,
    note_info: { content_id: noteId },
    title: noteTitle,
    knowledge_base_id: targetKB.id
  };
  if (folderId) addBody.folder_id = folderId;
  const addResp = await imaApi('openapi/wiki/v1/add_knowledge', addBody);
  const addData = JSON.parse(addResp);
  if (addData.code === 0) console.log('✅ 知识库同步成功 media_id:', addData.data.media_id);
  else console.error('⚠️ 知识库同步失败:', addData.msg);
}

main().catch(err => console.error('⚠️ upload_to_ima.js 异常:', err.message));
