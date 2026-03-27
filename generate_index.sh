#!/bin/bash
cat << 'HTML' > index.html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scholai 教材库</title>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; 
            line-height: 1.6; 
            padding: 2rem; 
            max-width: 1000px; 
            margin: 0 auto; 
            background-color: #f4f7f6; 
            color: #333; 
        }
        h1 { 
            text-align: center;
            color: #2c3e50; 
            margin-bottom: 2rem;
        }
        .grid-container {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 1.5rem;
        }
        .course-card { 
            background: white; 
            border-radius: 10px; 
            padding: 1.5rem; 
            box-shadow: 0 4px 6px rgba(0,0,0,0.05); 
            transition: transform 0.2s, box-shadow 0.2s;
            display: flex;
            flex-direction: column;
        }
        .course-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 15px rgba(0,0,0,0.1);
        }
        .course-card h2 { 
            margin-top: 0; 
            color: #2980b9; 
            font-size: 1.25rem; 
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 0.5rem;
            word-break: break-word;
        }
        .doc-group {
            margin-top: 1rem;
            flex-grow: 1;
        }
        .doc-group h3 {
            font-size: 0.95rem;
            color: #7f8c8d;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        ul { 
            list-style-type: none; 
            padding-left: 0; 
            margin: 0 0 1rem 0;
        }
        li { 
            margin-bottom: 0.5rem; 
        }
        a { 
            color: #34495e; 
            text-decoration: none; 
            font-weight: 500; 
            display: flex; 
            align-items: center;
            padding: 0.4rem 0.5rem; 
            border-radius: 6px; 
            background: #fdfdfd; 
            border: 1px solid #eee; 
            transition: all 0.2s;
            font-size: 0.95rem;
            word-break: break-word;
        }
        a:hover { 
            background: #f0f7fb; 
            border-color: #d0e6f5; 
            color: #2980b9;
        }
        .icon {
            margin-right: 0.5rem;
            font-size: 1.1rem;
        }
        .tag {
            font-size: 0.75rem;
            padding: 2px 6px;
            border-radius: 12px;
            background: #ecf0f1;
            color: #7f8c8d;
            margin-left: auto;
        }
    </style>
</head>
<body>
    <h1>📚 Scholai 教材导航</h1>
    <div class="grid-container">
HTML

# 遍历所有顶层子目录作为项目
for proj_dir in */ ; do
    if [ ! -d "$proj_dir" ]; then continue; fi
    proj_name=$(basename "$proj_dir")
    
    echo "        <div class=\"course-card\">" >> index.html
    echo "            <h2>📁 $proj_name</h2>" >> index.html
    echo "            <div class=\"doc-group\">" >> index.html
    
    # 查找 HTML 文件 (教材和思维导图)
    html_files=$(find "$proj_dir" -maxdepth 1 -type f -name "*.html")
    if [ -n "$html_files" ]; then
        echo "                <h3>网页内容</h3>" >> index.html
        echo "                <ul>" >> index.html
        echo "$html_files" | sort | while read -r file; do
            filename=$(basename "$file" .html)
            icon="📄"
            if [[ "$filename" == *"图文教材"* ]]; then icon="📖"; fi
            if [[ "$filename" == *"思维导图"* ]]; then icon="🧠"; fi
            echo "                    <li><a href=\"$file\"><span class=\"icon\">$icon</span> $filename <span class=\"tag\">HTML</span></a></li>" >> index.html
        done
        echo "                </ul>" >> index.html
    fi
    
    # 查找 MD 文件 (IOD, PD, VFD 等)
    md_files=$(find "$proj_dir" -maxdepth 1 -type f -name "*.md")
    if [ -n "$md_files" ]; then
        echo "                <h3>源文档</h3>" >> index.html
        echo "                <ul>" >> index.html
        echo "$md_files" | sort | while read -r file; do
            filename=$(basename "$file" .md)
            icon="📝"
            if [[ "$filename" == *"IOD"* ]]; then icon="🎯"; fi
            if [[ "$filename" == *"PD"* ]]; then icon="🛠"; fi
            if [[ "$filename" == *"VFD"* ]]; then icon="🎞"; fi
            echo "                    <li><a href=\"$file\"><span class=\"icon\">$icon</span> $filename <span class=\"tag\">MD</span></a></li>" >> index.html
        done
        echo "                </ul>" >> index.html
    fi
    
    echo "            </div>" >> index.html
    echo "        </div>" >> index.html
done

cat << 'HTML' >> index.html
    </div>
</body>
</html>
HTML
