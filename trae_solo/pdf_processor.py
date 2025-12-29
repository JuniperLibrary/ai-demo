from typing import List
from PyPDF2 import PdfReader
from pdfminer.high_level import extract_text as pdfminer_extract
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import os

class PDFProcessor:
    """PDF 处理类，提供 PDF 文本提取和 OCR 功能"""
    
    @staticmethod
    def extract_text_from_pdf(pdf_path: str) -> str:
        """从 PDF 中提取文本，优先使用 PyPDF2，失败则使用 pdfminer.six
        
        Args:
            pdf_path: PDF 文件路径
            
        Returns:
            提取的文本内容
        """
        try:
            # 尝试使用 PyPDF2 提取
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            
            # 如果 PyPDF2 提取结果为空或质量差，使用 pdfminer.six
            if not text.strip():
                text = pdfminer_extract(pdf_path)
            
            return text
        except Exception as e:
            print(f"PDF 文本提取失败: {e}")
            return ""
    
    @staticmethod
    def ocr_from_image(image_path: str, lang: str = 'chi_sim+eng') -> str:
        """从图片中提取文本
        
        Args:
            image_path: 图片文件路径
            lang: OCR 语言，默认为中英文混合
            
        Returns:
            提取的文本内容
        """
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image, lang=lang)
            return text
        except Exception as e:
            print(f"OCR 失败: {e}")
            return ""
    
    @staticmethod
    def ocr_from_pdf(pdf_path: str, lang: str = 'chi_sim+eng') -> str:
        """从扫描版 PDF 中提取文本（先转换为图片，再进行 OCR）
        
        Args:
            pdf_path: PDF 文件路径
            lang: OCR 语言，默认为中英文混合
            
        Returns:
            提取的文本内容
        """
        try:
            # 将 PDF 转换为图片
            images = convert_from_path(pdf_path)
            text = ""
            
            # 对每张图片进行 OCR
            for i, image in enumerate(images):
                # 保存临时图片
                temp_image_path = f"temp_page_{i}.png"
                image.save(temp_image_path, 'PNG')
                
                # 进行 OCR
                page_text = PDFProcessor.ocr_from_image(temp_image_path, lang)
                text += page_text + "\n\n"
                
                # 删除临时图片
                os.remove(temp_image_path)
            
            return text
        except Exception as e:
            print(f"PDF OCR 失败: {e}")
            return ""
    
    @staticmethod
    def process_pdf(pdf_path: str, lang: str = 'chi_sim+eng', ocr_threshold: int = 100) -> str:
        """综合处理 PDF，先尝试直接提取文本，若结果不佳则使用 OCR
        
        Args:
            pdf_path: PDF 文件路径
            lang: OCR 语言，默认为中英文混合
            ocr_threshold: 直接提取文本长度阈值，低于此值则使用 OCR
            
        Returns:
            处理后的文本内容
        """
        # 先尝试直接提取文本
        text = PDFProcessor.extract_text_from_pdf(pdf_path)
        
        # 如果直接提取的文本质量差（太短），则使用 OCR
        if len(text.strip()) < ocr_threshold:
            print("直接提取文本质量不佳，尝试使用 OCR...")
            text = PDFProcessor.ocr_from_pdf(pdf_path, lang)
        
        return text
    
    @staticmethod
    def split_pdf_into_chunks(pdf_path: str, lang: str = 'chi_sim+eng', ocr_threshold: int = 100) -> List[str]:
        """将 PDF 处理后分块
        
        Args:
            pdf_path: PDF 文件路径
            lang: OCR 语言，默认为中英文混合
            ocr_threshold: 直接提取文本长度阈值，低于此值则使用 OCR
            
        Returns:
            分块后的文本列表
        """
        # 处理 PDF 获取文本
        text = PDFProcessor.process_pdf(pdf_path, lang, ocr_threshold)
        
        # 分块处理
        chunks = [chunk for chunk in text.split("\n\n") if chunk.strip()]
        
        # 进一步优化分块（如果块太长，按句子分割）
        optimized_chunks = []
        for chunk in chunks:
            if len(chunk) > 1000:  # 如果块太长，进一步分割
                sentences = chunk.split('。')
                temp_chunk = ""
                for sentence in sentences:
                    if len(temp_chunk) + len(sentence) < 800:
                        temp_chunk += sentence + "。"
                    else:
                        optimized_chunks.append(temp_chunk.strip())
                        temp_chunk = sentence + "。"
                if temp_chunk.strip():
                    optimized_chunks.append(temp_chunk.strip())
            else:
                optimized_chunks.append(chunk.strip())
        
        return optimized_chunks
    
    @staticmethod
    def process_image(image_path: str, lang: str = 'chi_sim+eng') -> str:
        """处理单张图片，提取文本
        
        Args:
            image_path: 图片文件路径
            lang: OCR 语言，默认为中英文混合
            
        Returns:
            提取的文本内容
        """
        return PDFProcessor.ocr_from_image(image_path, lang)

# 示例用法
if __name__ == "__main__":
    # 替换为实际的 PDF 文件路径
    # pdf_path = "example.pdf"
    # chunks = PDFProcessor.split_pdf_into_chunks(pdf_path)
    # 
    # print(f"共提取 {len(chunks)} 个块")
    # for i, chunk in enumerate(chunks[:5]):  # 只显示前 5 个块
    #     print(f"\n[{i+1}] {chunk[:200]}...")
    print("PDFProcessor 类已成功导入")
