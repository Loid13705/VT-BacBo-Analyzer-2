from PIL import Image, ImageDraw, ImageFont
import os

def create_futuristic_logo():
    """Cria um logo futurista para o VT BacBo Analyzer"""
    
    # Criar imagem com fundo escuro
    width, height = 256, 256
    image = Image.new('RGB', (width, height), color='#0d0d0d')
    draw = ImageDraw.Draw(image)
    
    # Cores neon
    neon_blue = (0, 255, 234)  # #00ffea
    neon_green = (0, 255, 0)   # #00ff00
    
    # Desenhar círculo central com gradiente
    center_x, center_y = width // 2, height // 2
    radius = 100
    
    # Gradiente do círculo
    for r in range(radius, 0, -1):
        alpha = r / radius
        color = (
            int(neon_blue[0] * alpha),
            int(neon_blue[1] * alpha),
            int(neon_blue[2] * alpha)
        )
        draw.ellipse([
            center_x - r, center_y - r,
            center_x + r, center_y + r
        ], outline=color, width=2)
    
    # Desenhar dados dentro do círculo
    dice_size = 30
    dice1_pos = (center_x - 40, center_y - 15)
    dice2_pos = (center_x + 10, center_y - 15)
    
    # Dado 1
    draw.rectangle([
        dice1_pos[0], dice1_pos[1],
        dice1_pos[0] + dice_size, dice1_pos[1] + dice_size
    ], outline=neon_green, width=3)
    
    # Ponto central do dado 1
    dot_pos1 = (dice1_pos[0] + dice_size // 2, dice1_pos[1] + dice_size // 2)
    draw.ellipse([
        dot_pos1[0] - 3, dot_pos1[1] - 3,
        dot_pos1[0] + 3, dot_pos1[1] + 3
    ], fill=neon_green)
    
    # Dado 2
    draw.rectangle([
        dice2_pos[0], dice2_pos[1],
        dice2_pos[0] + dice_size, dice2_pos[1] + dice_size
    ], outline=neon_green, width=3)
    
    # Dois pontos para o dado 2
    dot1_pos = (dice2_pos[0] + 10, dice2_pos[1] + 10)
    dot2_pos = (dice2_pos[0] + 20, dice2_pos[1] + 20)
    
    draw.ellipse([
        dot1_pos[0] - 3, dot1_pos[1] - 3,
        dot1_pos[0] + 3, dot1_pos[1] + 3
    ], fill=neon_green)
    
    draw.ellipse([
        dot2_pos[0] - 3, dot2_pos[1] - 3,
        dot2_pos[0] + 3, dot2_pos[1] + 3
    ], fill=neon_green)
    
    # Texto "VT" acima
    try:
        # Tentar usar fonte professional
        font_large = ImageFont.truetype("arialbd.ttf", 32)
        font_small = ImageFont.truetype("arial.ttf", 18)
    except:
        # Fallback para fonte básica
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Texto "VT"
    draw.text((center_x - 20, center_y - 80), "VT", fill=neon_blue, font=font_large)
    
    # Texto "BACBO" abaixo
    draw.text((center_x - 40, center_y + 50), "BACBO", fill=neon_green, font=font_small)
    
    # Anel externo futurista
    draw.ellipse([
        center_x - 110, center_y - 110,
        center_x + 110, center_y + 110
    ], outline=neon_blue, width=2)
    
    # Salvar em múltiplos tamanhos para o ICO
    sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    ico_images = []
    
    for size in sizes:
        resized_img = image.resize(size, Image.Resampling.LANCZOS)
        ico_images.append(resized_img)
    
    # Criar pasta assets se não existir
    if not os.path.exists('assets'):
        os.makedirs('assets')
    
    # Salvar como ICO
    ico_images[0].save('assets/logo.ico', format='ICO', sizes=sizes)
    print("✅ Logo criado com sucesso: assets/logo.ico")
    
    # Salvar também como PNG para referência
    image.save('assets/logo.png', 'PNG')
    print("✅ Logo PNG criado: assets/logo.png")

if __name__ == "__main__":
    create_futuristic_logo()
