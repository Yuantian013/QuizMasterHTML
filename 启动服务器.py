#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
启动本地Web服务器，用于运行刷题系统
支持从手机等设备访问
"""
import http.server
import socketserver
import webbrowser
import os
import sys
import socket

PORT = 9000

def get_local_ip():
    """获取本机IP地址"""
    try:
        # 连接到一个远程地址来获取本机IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        try:
            # 备用方法
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            return ip
        except:
            return "127.0.0.1"

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # 允许跨域访问
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        # 禁用缓存：避免 index.html / 试题库.json 更新后浏览器仍使用旧缓存
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        super().end_headers()

def main():
    # 切换到脚本所在目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # 检查必要文件
    if not os.path.exists('试题库.json'):
        print("错误：找不到试题库.json文件！")
        sys.exit(1)
    
    if not os.path.exists('index.html'):
        print("错误：找不到index.html文件！")
        sys.exit(1)
    
    Handler = MyHTTPRequestHandler
    
    # 获取本机IP地址
    local_ip = get_local_ip()
    
    try:
        # 绑定到0.0.0.0，允许从其他设备访问
        with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
            local_url = f"http://localhost:{PORT}/index.html"
            network_url = f"http://{local_ip}:{PORT}/index.html"
            
            print("="*60)
            print("🚀 刷题系统服务器已启动！")
            print("="*60)
            print(f"💻 本机访问: {local_url}")
            print(f"📱 手机访问: {network_url}")
            print(f"📂 服务目录: {os.getcwd()}")
            print("="*60)
            print("📱 iPhone使用步骤：")
            print("   1. 确保iPhone和电脑连接同一WiFi")
            print(f"   2. 在iPhone浏览器中输入: {local_ip}:{PORT}")
            print(f"   3. 或直接访问: {network_url}")
            print("="*60)
            print("💡 提示：按 Ctrl+C 停止服务器")
            print("="*60)
            
            # 自动打开浏览器
            try:
                webbrowser.open(local_url)
            except:
                pass
            
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n服务器已停止。")
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"错误：端口 {PORT} 已被占用，请关闭其他服务或修改端口号。")
        else:
            print(f"错误：{e}")

if __name__ == "__main__":
    main()

