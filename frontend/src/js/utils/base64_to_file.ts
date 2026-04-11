/**
 * 将 Base64 Data URL 转换为 File 对象
 * @param base64 - 格式如 "data:image/png;base64,iVBOR..." 的字符串
 * @param filename - 文件名
 */
export function base64ToFile(base64: string, filename: string): File {
  // 1. 使用结构化解构，并为 header 和 data 提供初始值（空字符串）
  // 这样 TS 就会推断 header 和 data 永远是 string，而不是 string | undefined
  const [header = '', data = ''] = base64.split(',');

  // 2. 显式校验：如果 data 为空，说明 split 失败或 Base64 格式不对
  if (!header || !data) {
    throw new Error('Base64 字符串格式错误');
  }

  // 3. 提取 MIME 类型
  // 这里的 ?. 是可选链，如果 match 失败返回 null，?? 则提供默认值
  const mimeMatch = header.match(/:(.*?);/);
  const mime = mimeMatch?.[1] ?? 'image/jpeg';

  // 4. 解码数据
  // 由于上面判断了 !data，这里 TS 确定 data 是 string
  const bstr = atob(data);
  let n = bstr.length;
  const u8arr = new Uint8Array(n);

  while (n--) {
    u8arr[n] = bstr.charCodeAt(n);
  }

  return new File([u8arr], filename, { type: mime });
}