import base64
import sys


def safe_base64_decode(data):
    """
    尝试解码 Base64，自动处理 Padding 缺失问题。
    """
    # 移除行末换行符和空格
    data = data.strip()
    if not data:
        return None

    # 自动补全 Padding ('=')
    missing_padding = len(data) % 4
    if missing_padding:
        data += '=' * (4 - missing_padding)

    try:
        # 尝试解码
        decoded_bytes = base64.b64decode(data)

        # 尝试转为 UTF-8 字符串，如果失败（比如是二进制文件）则返回原始 bytes 的 repr
        try:
            return decoded_bytes.decode('utf-8')
        except UnicodeDecodeError:
            return f"[Binary Data]: {decoded_bytes}"

    except Exception as e:
        return f"[Error]: {str(e)}"


def batch_decode(input_file, output_file):
    print(f"[*] 开始从 {input_file} 读取...")

    try:
        with open(input_file, 'r', encoding='utf-8') as f_in, \
                open(output_file, 'w', encoding='utf-8') as f_out:

            lines = f_in.readlines()
            for i, line in enumerate(lines):
                line = line.strip()
                if not line: continue

                decoded = safe_base64_decode(line)

                # 格式化输出：原始 -> 解码
                result = f"Line {i + 1} | {line[:20]}... -> {decoded}\n"
                f_out.write(result)

                # 同时也打印到控制台
                print(f"[-] {result.strip()}")

        print(f"[*] 完成！结果已保存至 {output_file}")

    except FileNotFoundError:
        print(f"[!] 找不到文件: {input_file}")
    except Exception as e:
        print(f"[!] 发生意外错误: {e}")


if __name__ == "__main__":
    # 使用方法：在同目录下创建 encoded.txt 放入待解码内容
    input_filename = 'encoded.txt'
    output_filename = 'decoded.txt'

    # 你也可以直接在这里修改测试列表
    # temp_list = ["SGVsbG8=", "V29ybGQ", "InvalidData"]
    # ... (如果需要直接处理列表，可以简单改写上面的逻辑)

    batch_decode(input_filename, output_filename)
