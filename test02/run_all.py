import os
import sys
import time
from google import genai
from google.genai import types

def get_prompt(filename):
    path = os.path.join(os.environ["HOME"], ".openclaw/workspace/skills/skill-edu/shared-prompts", filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def main():
    api_key = os.environ.get("GEMINI_API_KEY", "REDACTED_API_KEY")
    client = genai.Client(api_key=api_key)
    model = "gemini-2.5-pro" # or gemini-1.5-pro, let's use gemini-1.5-pro as it's stable for files
    # Actually google-genai uses gemini-2.5-pro or gemini-1.5-pro. Let's use gemini-1.5-pro
    model = "gemini-2.5-pro"
    
    video_path = "/Users/ptd/Desktop/test02.mp4"
    out_dir = "/Users/ptd/.openclaw/workspace/outputs/test02"
    os.makedirs(out_dir, exist_ok=True)
    
    # 1. Upload Video
    print("Uploading video...")
    video_file = client.files.upload(file=video_path)
    
    while True:
        video_file = client.files.get(name=video_file.name)
        if video_file.state.name == "ACTIVE":
            break
        if video_file.state.name == "FAILED":
            print("Video processing failed.")
            sys.exit(1)
        print("Waiting for video processing...")
        time.sleep(5)
    
    print("Video ready.")
    
    # 2. Generate VFD
    print("Generating VFD...")
    vfd_prompt = "请观看并仔细聆听这个教学视频。请你提供一份完整的结构化源文档（VFD）。\n要求：\n1. 完整转录视频中的所有语音内容，不删减、不总结，修正识别错误。\n2. 根据内容逻辑分段，并加上二级标题。\n3. 在每个段落中，如果画面上有重要的PPT、板书、图表或教师演示动作，请在段落适当位置用 `[图：详细描述画面内容]` 的格式穿插视觉信息。\n4. 直接输出Markdown格式的正文，不要包含多余的客套话。"
    vfd_res = client.models.generate_content(
        model=model,
        contents=[video_file, vfd_prompt]
    )
    vfd_content = vfd_res.text
    with open(os.path.join(out_dir, "test02_VFD源文档.md"), "w", encoding="utf-8") as f:
        f.write(vfd_content)
        
    # 3. Generate IOD
    print("Generating IOD...")
    iod_prompt_base = get_prompt("教学目标prompt.md")
    iod_res = client.models.generate_content(
        model=model,
        contents=[iod_prompt_base + "\n\n以下是VFD输入：\n" + vfd_content]
    )
    iod_content = iod_res.text
    with open(os.path.join(out_dir, "test02_IOD教学目标文档.md"), "w", encoding="utf-8") as f:
        f.write(iod_content)
        
    # 4. Generate PD
    print("Generating PD...")
    pd_prompt_base = get_prompt("教学法 prompt.md")
    pd_res = client.models.generate_content(
        model=model,
        contents=[pd_prompt_base + "\n\n以下是VFD：\n" + vfd_content + "\n\n以下是IOD：\n" + iod_content]
    )
    pd_content = pd_res.text
    with open(os.path.join(out_dir, "test02_PD教学法文档.md"), "w", encoding="utf-8") as f:
        f.write(pd_content)
        
    # 5. Generate TXD
    print("Generating TXD...")
    txd_prompt_base = get_prompt("图文教材文本 prompt.md")
    txd_res = client.models.generate_content(
        model=model,
        contents=[txd_prompt_base + "\n\n【类型A输入】\n以下是VFD：\n" + vfd_content + "\n\n以下是IOD：\n" + iod_content + "\n\n以下是PD：\n" + pd_content]
    )
    txd_content = txd_res.text
    with open(os.path.join(out_dir, "test02_TXD图文教材文档.md"), "w", encoding="utf-8") as f:
        f.write(txd_content)
        
    # 6. Generate HTML
    print("Generating HTML...")
    html_prompt_base = get_prompt("图文渲染html prompt.md")
    html_res = client.models.generate_content(
        model=model,
        contents=[html_prompt_base + "\n\n【输入 Markdown】：\n" + txd_content]
    )
    html_content = html_res.text
    if html_content.startswith("```html"):
        html_content = html_content[7:-3]
    with open(os.path.join(out_dir, "test02_TXD图文教材.html"), "w", encoding="utf-8") as f:
        f.write(html_content)
        
    # 7. Generate Mind Map Markdown
    print("Generating Mind Map MD...")
    mm_prompt_base = get_prompt("思维导图prompt.md")
    mm_res = client.models.generate_content(
        model=model,
        contents=[mm_prompt_base + "\n\n【IOD 输入】：\n" + iod_content]
    )
    mm_content = mm_res.text
    if mm_content.startswith("```markdown"):
        mm_content = mm_content[11:-3]
        
    # 8. Generate Mind Map HTML
    print("Generating Mind Map HTML...")
    mm_html_template = get_prompt("思维导图转html prompt.md")
    # extract the HTML part from the template
    start_idx = mm_html_template.find("```html") + 7
    end_idx = mm_html_template.rfind("```")
    if start_idx > 6 and end_idx > start_idx:
        template = mm_html_template[start_idx:end_idx]
        final_mm_html = template.replace("{MMD内容原样嵌入，保留完整 Markdown 层级}", mm_content)
        final_mm_html = final_mm_html.replace("{课程名称}", "课程思维导图")
        with open(os.path.join(out_dir, "test02_思维导图.html"), "w", encoding="utf-8") as f:
            f.write(final_mm_html)
    else:
        print("Failed to parse Mind Map HTML template")

    print("Cleaning up...")
    client.files.delete(name=video_file.name)
    print("Done!")

if __name__ == "__main__":
    main()